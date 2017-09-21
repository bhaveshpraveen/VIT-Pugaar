from django.db import models
from django.utils.text import slugify

# TODO
''' 
    1. set predefined values(choices) for the block name, block slug, block_name
    2. associate the user and complaints with all the models below
    3. set predefined values(choices) for floor numbers
'''


class Block(models.Model):
    name = models.CharField(max_length=125, null=True)
    block_letter = models.CharField(max_length=10, unique=True, null=False)
    slug = models.SlugField(null=False, unique=True)


    def __str__(self):
        return "{}-{}".format(self.name, self.block_letter)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.block_letter)

class Floor(models.Model):
    block = models.ForeignKey(Block, related_name='block', on_delete=models.CASCADE)
    floor_number = models.IntegerField()

    def __str__(self):
        return "Floor {} in block {}".format(self.floor_number, self.block.name)


class Room(models.Model):
    block = models.ForeignKey(Block, related_name='block')
    floor = models.ForeignKey(Floor, related_name='floor')
    room_number = models.IntegerField()

    def __str__(self):
        return "Room no {} in floor {} of block {}".format(self.room_number, self.floor.floor_number, self.block.name)


class Toilet(models.Model):
    block = models.ForeignKey(Block, related_name='block')
    floor = models.ForeignKey(Floor, related_name='floor')

    def __str__(self):
        return "Toilet in floor number {} in block {}".format(self.floor.floor_number, self.block.name)





