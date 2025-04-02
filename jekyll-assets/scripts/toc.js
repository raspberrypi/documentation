/* Trigger Tocbot dynamic TOC, works with tocbot 3.0.2 */
function makeToc() {
    var tocElement = document.getElementById('toc');
    if (tocElement) { /* only run on pages that have a toc -- exclude boxes landing pages, for instance */
        var oldtoc = tocElement.nextElementSibling;
        var newtoc = document.getElementById('tocbot');
        newtoc.setAttribute('id', 'tocbot');
        newtoc.setAttribute('class', 'js-toc');
        oldtoc.parentNode.replaceChild(newtoc, oldtoc);
        tocbot.init({ contentSelector: '#content',
            headingSelector: 'h1, h2, h3, h4',
            smoothScroll: true,
            includeHtml: true
        });
        var handleTocOnResize = function() {
            var width = window.innerWidth
                        || document.documentElement.clientWidth
                        || document.body.clientWidth;
            if (width < 768) {
                tocbot.refresh({ contentSelector: '#content',
                    headingSelector: 'h1, h2, h3, h4',
                    collapseDepth: 6,
                    activeLinkClass: 'ignoreactive',
                    throttleTimeout: 1000,
                    smoothScroll: true });
            }
            else {
                tocbot.refresh({ contentSelector: '#content',
                    headingSelector: 'h1, h2, h3, h4',
                    smoothScroll: true });
            }
        };
        window.addEventListener('resize', handleTocOnResize);
        handleTocOnResize();
    }
}
