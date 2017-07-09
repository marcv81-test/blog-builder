import os
import yaml

class Site:

    def __init__(self, dir):
        # Loads the metadata
        meta = os.path.join(dir, 'meta.yml')
        with open(meta) as stream:
            self.meta = yaml.load(stream)
        # Loads the posts
        posts_dir = os.path.join(dir, 'posts')
        self.posts = list(sorted(
            Post.all(posts_dir),
            key=lambda post: post.id))
        # Order the posts
        for i in range(len(self.posts) - 1):
            self.posts[i].next = self.posts[i + 1]
        for i in range(1, len(self.posts)):
            self.posts[i].previous = self.posts[i - 1]

class Post:

    def __init__(self, id, dir):
        self.id = id
        # Loads the metadata
        meta = os.path.join(dir, 'meta.yml')
        with open(meta) as stream:
            self.meta = yaml.load(stream)
        # Loads the content
        content = os.path.join(dir, 'content.md')
        with open(content) as stream:
            self.content = stream.read()
        # Loads the images
        images_dir = os.path.join(dir, 'images')
        self.images = list(Image.all(images_dir))

    @staticmethod
    def all(posts_dir):
        for post_id in os.listdir(posts_dir):
            post_dir = os.path.join(posts_dir, post_id)
            yield Post(post_id, post_dir)

class Image:

    def __init__(self, id, path):
        self.id = id
        self.path = path

    @staticmethod
    def all(images_dir):
        if not os.path.isdir(images_dir):
            return
        for image_name in os.listdir(images_dir):
            (image_id, image_ext) = os.path.splitext(image_name)
            image_path = os.path.join(images_dir, image_name)
            yield Image(image_id, image_path)
