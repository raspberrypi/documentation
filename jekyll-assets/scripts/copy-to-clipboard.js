var listings = document.querySelectorAll('div.listingblock');

var showButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className.replace(/\bhidden\b/,'').trim();
};

var hideButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className + " hidden";
};

for (var i = 0; i < listings.length; i++) {
  listings[i].addEventListener('mouseenter', showButton, false);
  listings[i].addEventListener('mouseleave', hideButton, false);
}

var buttons = document.querySelectorAll('button.copy-button');

var showTooltip = function() {
  var tooltip = this.querySelector("span.tooltip");
  tooltip.className = "tooltip";
};

var hideTooltip = function() {
  var tooltip = this.querySelector("span.tooltip");
  tooltip.className = "tooltip hidden";
};

var extractDoxygenCode = function(node) {
  var lines = node.querySelectorAll("div.line");
  var preText = "";
  for (var i = 0; i < lines.length; i++) {
    var myText = lines[i].textContent;
    preText = preText + myText + "\n";
  }
  return preText;
};

for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('mouseenter', showTooltip, false);
  buttons[i].addEventListener('mouseleave', hideTooltip, false);
}

window.addEventListener('load', function() {
  var clipboard = new ClipboardJS('.copy-button', {
    text: function(trigger) {
      if (trigger.parentNode.querySelector('div.line')) {
        var text = extractDoxygenCode(trigger.parentNode);
      } else {
        var text = trigger.parentNode.querySelector('pre').textContent
        
        // if the code snippet represents a console snippet
        if (trigger.parentNode.querySelector('pre').querySelector('code') != null && trigger.parentNode.querySelector('pre').querySelector('code').getAttribute('data-lang') == 'console') {
          // for each line of the code snippet
          var text_split_into_lines = text.split('\n');

          // trim the '$ ' from the clipboard copy so users don't have to trim it themselves
          text_split_into_lines = text_split_into_lines.map(function(x) {
            if (x.startsWith('$ ')) {
              return x.substring(2);
            }
            else return x;
          })

          // re-assemble the snippet into multiple lines
          text = text_split_into_lines.join('\n');
        }
      }
      return text;
    },
  });

  clipboard.on('success', function(event) {
    event.clearSelection();
    var textEl = event.trigger.querySelector('.copy-button-label');
    var tooltip = event.trigger.querySelector('span.tooltip');
    tooltip.className = "tooltip hidden";
    textEl.textContent = ' Copied!';
    setTimeout(function() {
      textEl.textContent = '';
    }, 2000);
  });

  clipboard.on('error', function (e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
  });
});