function Glossary(terms) {
    var self = this;

    for (var term in terms) {
        jQuery('div.block').highlight(terms[term].label,
                                      {element: 'span',
                                       className: 'glossary',
                                       wordsOnly: true});
    }

    jQuery('span.glossary').click(function(evt) {
        evt.preventDefault();
        var srcElement = evt.srcElement || evt.target || evt.originalTarget;
        var html = jQuery.trim(srcElement.innerHTML);
        var slug = self.slugify(html);
        if (terms.hasOwnProperty(slug)) {
            jQuery('#glossary-popup div.term').html(terms[slug].label);
            jQuery('#glossary-popup div.definition')
                .html(terms[slug].definition);

            var pos = jQuery(srcElement).position();
            var left = pos.left + 15;
            var top = pos.top + jQuery(srcElement).outerHeight() + 2;
            var popupWidth = jQuery('#glossary-popup').outerWidth();
            var popupHeight = jQuery('#glossary-popup').outerHeight();

            if ((jQuery(window).width() - (left + popupWidth)) < 25) {
                left = (pos.left + jQuery(srcElement)
                        .outerWidth() + 15) - popupWidth;
            }

            var docViewTop = jQuery(window).scrollTop();
            var docViewBottom = docViewTop + jQuery(window).height();

            var elemTop = jQuery(srcElement).offset().top;
            var elemBottom = elemTop + jQuery(srcElement)
                .height() + popupHeight;

            if ((docViewTop >= elemTop) || (docViewBottom <= elemBottom)) {
                top -= jQuery(srcElement).height() + popupHeight;
            }

            jQuery('#glossary-popup').css({
                'top': top,
                'left': left});

            jQuery('#glossary-popup').appendTo(srcElement);

            jQuery('#glossary-popup').show();
        }
        return false;
    });

    jQuery('#glossary-popup a').click(function(evt) {
        jQuery('#glossary-popup').hide();
        jQuery('#glossary-popup').appendTo('body');
    });

    jQuery('body').click(function(evt) {
        if (jQuery('#glossary-popup').is(':visible')) {
            jQuery('#glossary-popup').hide();
            jQuery('#glossary-popup').appendTo('body');
        }
    });
}

Glossary.prototype.slugify = function(str) {
    str = str.toLowerCase();
    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
};
