"""
Basic AI service for text processing using NLTK.
"""
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
import string
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class AIService:
    """Service for basic AI operations using NLTK."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def generate_summary(self, content, title):
        """
        Generate a basic extractive summary of the provided content.
        
        Args:
            content (str): The text content to summarize
            title (str): The title of the material
            
        Returns:
            dict: Contains 'summary' and 'key_points'
        """
        try:
            # Tokenize into sentences
            sentences = sent_tokenize(content)
            if len(sentences) < 3:
                summary = content[:500] + "..." if len(content) > 500 else content
                key_points = [s.strip() for s in sentences if s.strip()]
            else:
                # Calculate word frequencies
                words = word_tokenize(content.lower())
                words = [word for word in words if word not in self.stop_words and word not in string.punctuation]
                freq_dist = FreqDist(words)
                
                # Score sentences based on word frequencies
                sentence_scores = defaultdict(float)
                for sentence in sentences:
                    sentence_words = word_tokenize(sentence.lower())
                    sentence_words = [word for word in sentence_words if word not in string.punctuation]
                    for word in sentence_words:
                        if word in freq_dist:
                            sentence_scores[sentence] += freq_dist[word]
                
                # Get top sentences for summary
                top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                summary_sentences = [sent[0] for sent in top_sentences]
                summary = ' '.join(summary_sentences)
                
                # Extract key points (remaining top sentences)
                key_points = [sent[0] for sent in top_sentences[3:6]] if len(top_sentences) > 3 else []
            
            return {
                'success': True,
                'summary': summary,
                'key_points': key_points[:5],
            }
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def generate_practice_questions(self, content, title, num_questions=5):
        """
        Generate basic practice questions based on the provided content.
        
        Args:
            content (str): The text content
            title (str): The title of the material
            num_questions (int): Number of questions to generate
            
        Returns:
            list: List of question dictionaries
        """
        try:
            # Tokenize and get nouns (basic POS tagging approximation)
            words = word_tokenize(content)
            # Simple heuristic: words longer than 4 chars that aren't stopwords
            potential_keywords = [word for word in words 
                                if len(word) > 4 
                                and word.lower() not in self.stop_words 
                                and word not in string.punctuation]
            
            freq_dist = FreqDist(potential_keywords)
            top_keywords = [word for word, _ in freq_dist.most_common(10)]
            
            questions = []
            question_templates = [
                "What is {keyword}?",
                "Explain the concept of {keyword}.",
                "How does {keyword} relate to {title}?",
                "What are the key aspects of {keyword}?",
                "Describe {keyword} in your own words."
            ]
            
            for i in range(min(num_questions, len(top_keywords))):
                keyword = top_keywords[i]
                template = question_templates[i % len(question_templates)]
                question = template.format(keyword=keyword, title=title)
                
                # Basic answer: extract sentences containing the keyword
                relevant_sentences = [sent for sent in sent_tokenize(content) 
                                    if keyword.lower() in sent.lower()]
                answer = ' '.join(relevant_sentences[:2]) if relevant_sentences else f"This relates to key concepts in {title}."
                
                difficulty = "easy" if i < 2 else "medium" if i < 4 else "hard"
                
                questions.append({
                    'question': question,
                    'answer': answer,
                    'difficulty': difficulty
                })
            
            return {
                'success': True,
                'questions': questions,
            }
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def answer_question(self, user_question, content, title):
        """
        Provide a basic answer based on keyword matching.
        
        Args:
            user_question (str): The question from the user
            content (str): The study material content
            title (str): The title of the material
            
        Returns:
            dict: Contains 'answer'
        """
        try:
            # Simple keyword matching
            question_words = word_tokenize(user_question.lower())
            question_keywords = [word for word in question_words 
                               if word not in self.stop_words and word not in string.punctuation]
            
            relevant_sentences = []
            for sentence in sent_tokenize(content):
                sentence_words = word_tokenize(sentence.lower())
                if any(keyword in sentence_words for keyword in question_keywords):
                    relevant_sentences.append(sentence)
            
            if relevant_sentences:
                answer = ' '.join(relevant_sentences[:3])
            else:
                answer = f"I'm sorry, I couldn't find specific information about that in the material '{title}'. Please try rephrasing your question or ask about key concepts from the content."
            
            return {
                'success': True,
                'answer': answer,
            }
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }


# Create a singleton instance
ai_service = AIService()
