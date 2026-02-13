"""
Fine-tuning Module for Career Transition Data
Creates training data and fine-tunes sentence transformer for career guidance.
"""

import json
import pandas as pd
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
import sqlite3


class CareerTransitionDataset:
    """
    Generates and manages career transition training data.
    """
    
    def __init__(self, db_path: str = 'genmentor.db'):
        self.db_path = db_path
        self.training_data = []
        
    def generate_training_pairs(self) -> List[InputExample]:
        """
        Generate training pairs from ESCO database.
        
        Creates positive and negative examples:
        - Positive: career goals that match specific occupations
        - Negative: unrelated career goals and occupations
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get occupations with descriptions
        cursor.execute("""
            SELECT concept_uri, preferred_label, description
            FROM occupations
            WHERE description IS NOT NULL
            LIMIT 1000
        """)
        
        occupations = cursor.fetchall()
        conn.close()
        
        training_examples = []
        
        # Generate synthetic career transition queries
        transition_templates = [
            "I want to become a {occupation}",
            "I am interested in transitioning to {occupation}",
            "My goal is to work as a {occupation}",
            "I want to pursue a career in {occupation}",
            "How can I become a {occupation}",
            "I am transitioning from my current role to {occupation}",
            "My career goal is {occupation}",
            "I want to specialize in {occupation_field}"
        ]
        
        for uri, label, description in occupations:
            # Create positive examples (query matches occupation)
            for template in transition_templates[:3]:  # Use subset
                query = template.format(
                    occupation=label.lower(),
                    occupation_field=label.lower().split()[0] if ' ' in label else label.lower()
                )
                
                # Combine label and description for target
                target_text = f"{label}. {description[:200] if description else ''}"
                
                # High similarity score (0.9-1.0) for direct matches
                training_examples.append(
                    InputExample(texts=[query, target_text], label=0.95)
                )
        
        # Generate negative examples (unrelated pairs)
        import random
        for i in range(min(len(occupations) // 2, 500)):
            idx1, idx2 = random.sample(range(len(occupations)), 2)
            uri1, label1, desc1 = occupations[idx1]
            uri2, label2, desc2 = occupations[idx2]
            
            query = f"I want to become a {label1.lower()}"
            wrong_target = f"{label2}. {desc2[:200] if desc2 else ''}"
            
            # Low similarity score (0.0-0.3) for mismatches
            training_examples.append(
                InputExample(texts=[query, wrong_target], label=0.1)
            )
        
        print(f"Generated {len(training_examples)} training examples")
        return training_examples
    
    def create_evaluation_set(self) -> List[InputExample]:
        """Create evaluation dataset for model performance testing."""
        eval_examples = [
            InputExample(texts=["I want to become a data scientist", 
                              "data scientist analyzing data"], label=0.95),
            InputExample(texts=["I want to work in machine learning",
                              "machine learning engineer"], label=0.90),
            InputExample(texts=["I want to be a web developer",
                              "software engineer web development"], label=0.85),
            InputExample(texts=["I want to transition to marketing",
                              "mechanical engineer"], label=0.15),
            InputExample(texts=["I am interested in finance",
                              "graphic designer"], label=0.10),
        ]
        return eval_examples
    
    def add_custom_transitions(self) -> List[InputExample]:
        """Add domain-specific career transition examples."""
        custom_transitions = [
            # Marketing to Data Science transitions
            {
                'query': "I am a marketing manager and want to transition to data science",
                'target': "data scientist marketing analytics machine learning",
                'score': 0.88
            },
            {
                'query': "I work in marketing and want to learn data analysis",
                'target': "data analyst marketing insights business intelligence",
                'score': 0.90
            },
            # Software to ML transitions
            {
                'query': "I am a software engineer interested in machine learning",
                'target': "machine learning engineer ai development",
                'score': 0.92
            },
            {
                'query': "I am a developer who wants to work with AI",
                'target': "artificial intelligence engineer deep learning",
                'score': 0.90
            },
            # Finance to Data
            {
                'query': "I am in finance and want to move to data engineering",
                'target': "data engineer financial analytics big data",
                'score': 0.87
            },
            # Teaching to Instructional Design
            {
                'query': "I am a teacher and want to become an instructional designer",
                'target': "instructional designer education technology e-learning",
                'score': 0.89
            },
            # Design transitions
            {
                'query': "I am a graphic designer wanting to do UX design",
                'target': "user experience designer interface design usability",
                'score': 0.91
            }
        ]
        
        examples = []
        for transition in custom_transitions:
            examples.append(
                InputExample(
                    texts=[transition['query'], transition['target']],
                    label=transition['score']
                )
            )
        
        return examples


class CareerModelFineTuner:
    """
    Fine-tunes sentence transformer models for career matching.
    """
    
    def __init__(self, base_model: str = 'all-mpnet-base-v2'):
        """
        Initialize fine-tuner with base model.
        
        Args:
            base_model: Pre-trained sentence transformer to fine-tune
        """
        self.base_model_name = base_model
        self.model = SentenceTransformer(base_model)
        self.dataset = CareerTransitionDataset()
        
    def prepare_training_data(self) -> Tuple[DataLoader, EmbeddingSimilarityEvaluator]:
        """Prepare training and evaluation data loaders."""
        print("Preparing training data...")
        
        # Generate training examples
        esco_examples = self.dataset.generate_training_pairs()
        custom_examples = self.dataset.add_custom_transitions()
        all_training = esco_examples + custom_examples
        
        # Create data loader
        train_dataloader = DataLoader(
            all_training,
            shuffle=True,
            batch_size=16
        )
        
        # Create evaluator
        eval_examples = self.dataset.create_evaluation_set()
        eval_sentences1 = [ex.texts[0] for ex in eval_examples]
        eval_sentences2 = [ex.texts[1] for ex in eval_examples]
        eval_scores = [ex.label for ex in eval_examples]
        
        evaluator = EmbeddingSimilarityEvaluator(
            eval_sentences1,
            eval_sentences2,
            eval_scores
        )
        
        return train_dataloader, evaluator
    
    def fine_tune(self, 
                  num_epochs: int = 4,
                  output_path: str = './models/genmentor-career-matcher',
                  evaluation_steps: int = 500):
        """
        Fine-tune the model on career transition data.
        
        Args:
            num_epochs: Number of training epochs
            output_path: Where to save the fine-tuned model
            evaluation_steps: How often to evaluate during training
        """
        print(f"Starting fine-tuning of {self.base_model_name}...")
        print(f"Training for {num_epochs} epochs")
        
        # Prepare data
        train_dataloader, evaluator = self.prepare_training_data()
        
        # Define loss function (CosineSimilarityLoss for regression)
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        # Train the model
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=num_epochs,
            evaluator=evaluator,
            evaluation_steps=evaluation_steps,
            warmup_steps=100,
            output_path=output_path,
            save_best_model=True,
            show_progress_bar=True
        )
        
        print(f"\n✅ Fine-tuning complete! Model saved to: {output_path}")
        print(f"📊 Use this model by setting model_name='{output_path}' in GenMentorAI")
        
        return output_path
    
    def evaluate_model(self, test_pairs: List[Tuple[str, str, float]] = None):
        """
        Evaluate fine-tuned model performance.
        
        Args:
            test_pairs: Optional list of (text1, text2, expected_score) tuples
        """
        if test_pairs is None:
            test_pairs = [
                ("I want to be a data scientist", 
                 "data scientist role", 0.95),
                ("transitioning to machine learning", 
                 "machine learning engineer", 0.90),
                ("I want to do marketing", 
                 "software developer", 0.15),
            ]
        
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60)
        
        for text1, text2, expected in test_pairs:
            emb1 = self.model.encode(text1)
            emb2 = self.model.encode(text2)
            
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            similarity = cosine_similarity(
                emb1.reshape(1, -1),
                emb2.reshape(1, -1)
            )[0][0]
            
            difference = abs(similarity - expected)
            status = "✅" if difference < 0.10 else "⚠️"
            
            print(f"\n{status} Test Pair:")
            print(f"   Text 1: {text1}")
            print(f"   Text 2: {text2}")
            print(f"   Expected: {expected:.3f}")
            print(f"   Actual: {similarity:.3f}")
            print(f"   Difference: {difference:.3f}")


def main():
    """Main fine-tuning workflow."""
    print("="*70)
    print("  GENMENTOR MODEL FINE-TUNING")
    print("="*70)
    
    # Initialize fine-tuner
    print("\n1. Initializing fine-tuner...")
    fine_tuner = CareerModelFineTuner(base_model='all-mpnet-base-v2')
    
    # Option 1: Full fine-tuning (takes time and compute)
    print("\n2. Fine-tuning model on career transition data...")
    print("   (This may take 30-60 minutes depending on hardware)")
    
    # Uncomment to run actual fine-tuning:
    # output_path = fine_tuner.fine_tune(num_epochs=4)
    
    # Option 2: Quick evaluation only (for testing)
    print("\n   Skipping fine-tuning, showing evaluation demo...")
    fine_tuner.evaluate_model()
    
    print("\n" + "="*70)
    print("  FINE-TUNING GUIDE")
    print("="*70)
    print("""
To fine-tune the model:
1. Uncomment the fine_tuner.fine_tune() line above
2. Run: python fine_tuning.py
3. Wait for training to complete (~30-60 min)
4. Update ai_engine.py to use the fine-tuned model:
   
   GenMentorAI(model_name='./models/genmentor-career-matcher')
   
5. The fine-tuned model will provide better career matching accuracy!

Note: Fine-tuning requires GPU for reasonable speed.
      CPU training will work but be significantly slower.
    """)


if __name__ == "__main__":
    main()
