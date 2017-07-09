import bs4
import hoedown
import jinja2
import os
import PIL.Image
import shutil

class Renderer:

    def __init__(self, html_renderer, image_renderer):
        self.html_renderer = html_renderer
        self.image_renderer = image_renderer

    @staticmethod
    def empty_dir(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

    def render_site(self, site, site_dir):
        self.render_post(site, site.posts[-1], site_dir)
        self.render_posts(site, site_dir)

    def render_posts(self, site, site_dir):
        posts_dir = os.path.join(site_dir, 'posts')
        Renderer.empty_dir(posts_dir)
        for post in site.posts:
            post_dir = os.path.join(posts_dir, post.id)
            self.render_post(site, post, post_dir)

    def render_post(self, site, post, post_dir):
        Renderer.empty_dir(post_dir)
        self.html_renderer.render(
            'post', {'site': site, 'post': post}, post_dir)
        self.render_post_images(post.images, post_dir)

    def render_post_images(self, images, post_dir):
        if len(images) == 0:
            return
        images_dir = os.path.join(post_dir, 'images')
        Renderer.empty_dir(images_dir)
        for image in images:
            self.image_renderer.render(image, images_dir)

class HtmlRenderer:

    def __init__(self, templates_dir):
        loader = jinja2.FileSystemLoader(templates_dir)
        environment = jinja2.Environment(loader=loader)
        environment.filters['markdown'] = HtmlRenderer.render_markdown
        self.templates = {'post': environment.get_template('post.html')}

    @staticmethod
    def render_markdown(markdown):
        # Converts Markdown to HTML
        renderer = hoedown.Markdown(hoedown.HtmlRenderer())
        html = renderer.render(markdown)
        # Injects customizations
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for image in soup.findAll('img'):
            image['class'] = 'img-responsive center-block'
        html = str(soup)
        # Returns the HTML
        return html

    @staticmethod
    def remove_blank_lines(html):
        lines = html.splitlines()
        lines = (line for line in lines if len(line) > 0)
        return '\n'.join(lines)

    def render(self, template, parameters, dir):
        index_path = os.path.join(dir, 'index.html')
        html = self.templates[template].render(**parameters)
        html = HtmlRenderer.remove_blank_lines(html)
        with open(index_path, 'w') as stream:
            stream.write(html)

class ImageRenderer:

    def __init__(self, image_x=800, image_y=600, quality=75):
        self.size = (image_x, image_y)
        self.quality = 75

    def render(self, image, dir):
        image_path = os.path.join(dir, image.id + '.jpeg')
        buffer = PIL.Image.open(image.path)
        buffer.thumbnail(self.size, PIL.Image.ANTIALIAS)
        buffer.save(image_path, 'JPEG', quality=self.quality)
