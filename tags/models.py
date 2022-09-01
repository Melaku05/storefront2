from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    '''
    file
    '''
    def get_tags_for(self, obj_type, obj_id):
        '''
        Return the tags for the given object.
        '''
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Tag(models.Model):
    '''
    The label of the tag.
    '''
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        '''
        Return the label of the tag.
        '''
        return self.label


class TaggedItem(models.Model):
    '''
    The tagged item.
    '''
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = TaggedItemManager()

    def __str__(self) -> str:
        '''
        Return the label of the tag.
        '''
        return self.tag.label

    class Meta:
        '''
        The ordering is based on the label field.
        '''
        ordering = ['tag__label']
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
