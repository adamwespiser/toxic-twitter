from abc import ABC, abstractmethod


class ApiIntegration(ABC):
    
    @abstractmethod
    def get_user_tweets(self, username, limit=None):
        """Returns tweets of a user.

        Args:
            username (str): Username as given in twitter.
        
        Returns:
            list of data_fetch_helpers.tweet.Tweet instances
        """
        pass
    
    @abstractmethod
    def get_tweets_from_search(self, search_term, limit=None):
        """Returns tweets that match the given search_term.

        Args:
            search_term (str): Term that has to be used for searching.
        
        Returns:
            list of data_fetch_helpers.tweet.Tweet instances
        """
        pass
