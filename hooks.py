import posixpath
import re
from pathlib import PurePosixPath
from urllib.parse import urlsplit, urlunsplit


IMG_SRC_RE = re.compile(
    r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])([^"\']+)(\2)',
    re.IGNORECASE,
)


def on_env(env, config, files):
    env.add_extension('jinja2.ext.do')


def _is_vietnamese_page(page, config):
    page_url = (page.url or '').lstrip('/')
    if page_url.startswith('vi/'):
        return True

    theme = getattr(config, 'theme', None)
    try:
        return theme.get('language') == 'vi'
    except AttributeError:
        return False


def _rewrite_local_image_src(src, page):
    """Rewrite raw-HTML local image paths for the /vi/ output tree.

    Markdown image syntax is already rewritten by MkDocs. Raw HTML is not, so
    source paths such as ``MST_before.png`` or ``./MST_before.png`` would
    otherwise resolve below ``/vi/`` even though the assets are emitted in the
    default-language tree.

    Paths beginning with ``../`` are left alone because they can already be
    rewritten Markdown-image output. The rendered-site checker catches any
    genuinely broken path that remains.
    """
    parsed = urlsplit(src)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return src
    if parsed.path.startswith(('/', '#', '../')):
        return src

    source_relative_path = parsed.path[2:] if parsed.path.startswith('./') else parsed.path

    src_uri = PurePosixPath(page.file.src_uri)
    asset_path = PurePosixPath(
        posixpath.normpath(str(src_uri.parent / source_relative_path))
    )

    page_url = (page.url or '').lstrip('/')
    if not page_url.startswith('vi/'):
        page_url = f'vi/{page_url}'
    page_dir = PurePosixPath(page_url).parent

    rewritten_path = posixpath.relpath(str(asset_path), str(page_dir))
    return urlunsplit(('', '', rewritten_path, parsed.query, parsed.fragment))


def on_page_content(html, page, config, files):
    if not _is_vietnamese_page(page, config):
        return html

    def replace(match):
        src = match.group(3)
        rewritten = _rewrite_local_image_src(src, page)
        return f'{match.group(1)}{match.group(2)}{rewritten}{match.group(2)}'

    return IMG_SRC_RE.sub(replace, html)
