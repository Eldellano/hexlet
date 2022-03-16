from django.db import models, transaction, IntegrityError
from django.db.models import Count


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampedModel):
    """A blog user."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    nick_name = models.CharField(max_length=100, null=True)

class Tag(TimestampedModel):
    """A tag for the group of posts."""

    title = models.CharField(max_length=100)


class Post(TimestampedModel):
    """A blog post."""

    title = models.CharField(max_length=200)
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class PostComment(TimestampedModel):
    """A commentary to the blog post."""

    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_to = models.ForeignKey(
        'PostComment', on_delete=models.SET_NULL, null=True,
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class PostLike(TimestampedModel):
    """A positive reaction to the blog post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'creator']


class Vote(models.Model):
    subject = models.CharField(max_length=200)
    positive = models.BooleanField(default=True)

    @classmethod
    def in_favour(cls, subject):
        return cls.objects.create(subject=subject)

    @classmethod
    def against(cls, subject):
        return cls.objects.create(subject=subject, positive=False)

    @classmethod
    def results_for(cls, subject):
        """Return the voting results for the subject."""
        question = Vote.objects.filter(subject=subject)
        dict_for_res = {'in favour': question.filter(positive=True).count(),
                        'against': question.filter(positive=False).count()}
        return dict_for_res


class CycleInGraphError(Exception):
    """An exception that means that some graph has cycles."""


class Task(models.Model):
    value = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    @property
    def root(self):
        graf_set = set()
        return self.get_null(graf_set)

    def get_null(self, graf_set):
        task = Task.objects.get(value=self.value)
        if task.parent_id is None:
            return self
        else:
            new_val = Task.objects.get(id=task.parent_id)
            if new_val.value in graf_set:
                raise CycleInGraphError(new_val.id)
            else:
                graf_set.add(task.value[0])
                return Task.get_null(new_val, graf_set)


class Island(models.Model):
    name = models.CharField(max_length=200)

    def can_reach(self, island, *, by_ship):
        """Return True if one can reach the @island using a @by ship"""
        island_a = Island.objects.filter(ships=by_ship).filter(name=self.name)
        island_b = Island.objects.filter(ships=by_ship).filter(name=island.name)
        if len(island_a) > 0 and len(island_b) > 0:
            return True
        else:
            return False


class Ship(models.Model):
    name = models.CharField(max_length=200)
    islands = models.ManyToManyField(Island, related_name='ships')


class Clip(models.Model):
    title = models.CharField(max_length=200)

    def like(self):
        ClipLike.objects.create(clip=self)

    def dislike(self):
        ClipDislike.objects.create(clip=self)

    @classmethod
    def rates_for(cls, **kwargs) -> (int, int):
        """Returns a tuple of integers (likes, dislikes)for the clip(s) filtered by provided kwargs."""
        like = Clip.objects.filter(**kwargs).annotate(Count('cliplike'))
        dislike = Clip.objects.filter(**kwargs).annotate(Count('clipdislike'))
        return (like[0].cliplike__count, dislike[0].clipdislike__count)


class ClipLike(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)


class ClipDislike(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)



class Project(models.Model):
    name = models.CharField(max_length=200)

    @classmethod
    @transaction.atomic
    def reorganize(self, assignments):
        Worker.objects.exclude(id__in=assignments).update(project_id=None)

        for key, value in assignments.items():
            Worker.objects.filter(id=key).update(project_id=value)


class Worker(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(
        Project,
        null=True,
        on_delete=models.SET_NULL,
    )