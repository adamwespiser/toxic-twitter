from abc import ABC, abstractmethod


class ApiIntegration(ABC):
    
    @abstractmethod
    def get_user_tweets(self, username, limit=None):
        pass
    
    @abstractmethod
    def get_tweets_from_search(self, search_term, limit=None):
        pass
