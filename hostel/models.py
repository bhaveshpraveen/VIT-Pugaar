from django.db import models
from django.utils.text import slugify

# TODO
''' 
    1. set predefined values(choices) for the block name, block slug, block_name
    2. associate the user and complaints with all the models below
    3. set predefined values(choices) for floor numbers
    4. I've set the choices for the block, you need to add in the names of the block before saving
    5. New Permission for Block and Floor
'''


class Block(models.Model):
    HOSTEL_NAMES = dict([
        ('a', 'Name of A block'),
        ('b', 'Name of B block'),
        ('c', 'Name of C block'),
        ('d', 'Name of D block'),
        ('e', 'Name of E block'),
        ('f', 'Name of F block'),
        ('g', 'Name of G block'),
        ('h', 'Name of F block'),
        ('j', 'Name of J block')]
    )
    block_letter = models.CharField(max_length=3, choices=HOSTEL_NAMES.items(), default='a', unique=True)
    name = models.CharField(max_length=125, null=False, blank=True)
    slug = models.SlugField(null=False, blank=True)

    def __str__(self):
        return "{}-{}".format(self.name, self.block_letter)

    def save(self, *args, **kwargs):
        self.name = self.HOSTEL_NAMES.get(self.block_letter)
        self.slug = slugify(self.HOSTEL_NAMES.get(self.block_letter))
        super(Block, self).save(*args, **kwargs)


class Floor(models.Model):
    block = models.ForeignKey(Block, related_name='floors', on_delete=models.CASCADE)
    floor_number = models.PositiveIntegerField()

    def __str__(self):
        return "Floor {} in block {}".format(self.floor_number, self.block.name)

    class Meta:
        unique_together = (
            ('block', 'floor_number'),
        )


# class Room(models.Model):
#     block = models.ForeignKey(Block, related_name='block')
#     floor = models.ForeignKey(Floor, related_name='floor')
#     room_number = models.IntegerField()
#
#     def __str__(self):
#         return "Room no {} in floor {} of block {}".format(self.room_number, self.floor.floor_number, self.block.name)
#
#
# class Toilet(models.Model):
#     block = models.ForeignKey(Block, related_name='block')
#     floor = models.ForeignKey(Floor, related_name='floor')
#
#     def __str__(self):
#         return "Toilet in floor number {} in block {}".format(self.floor.floor_number, self.block.name)





