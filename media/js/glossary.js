function Glossary(terms) {
    var self = this;
    
    for (var term in terms) { 
        jQuery('div.block').highlight(terms[term].label, 
                                      {element: 'span',
                                       className: 'glossary',
                                       wordsOnly: true});              
    }
    
    jQuery('span.glossary').click(function(evt) {
        var srcElement = evt.srcElement || evt.target || evt.originalTarget;
        var slug = self.slugify(srcElement.innerHTML);
        if (terms.hasOwnProperty(slug)) {
            jQuery("#glossary-popup div.term").html(terms[slug].label);
            jQuery("#glossary-popup div.definition").html(terms[slug].definition);
            
            var pos = jQuery(srcElement).position();
            var left = pos.left + 15;
            var popupWidth = jQuery("#glossary-popup").outerWidth()
            
            if (jQuery(window).width() - (left + popupWidth) < 25) {
                left = (pos.left + jQuery(srcElement).outerWidth() + 15) - popupWidth;
            }
            
            jQuery("#glossary-popup").css({
                'top': pos.top + jQuery(srcElement).height() + 2,
                'left': left});
            
            jQuery("#glossary-popup").show();
        }
    });
    
    jQuery('#glossary-popup a').click(function(evt) {
        jQuery("#glossary-popup").hide();
    });
}

Glossary.prototype.slugify = function (str) {
    str = str.toLowerCase();
    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
    .replace(/\s+/g, '-') // collapse whitespace and replace by -
    .replace(/-+/g, '-'); // collapse dashes
 
    return str;
}