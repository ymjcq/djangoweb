import datetime
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
	text=indexes.CharField(document=True,use_template=True)
	author=indexes.CharField(model_attr='author')
	timestamp=indexes.DateTimeField(model_attr='timestamp')
	
	def get_model(self):
		return Post
	def index_queryset(self,using=None):
		return self.get_model().objects.filter(timestamp__lte=datetime.datetime.now())