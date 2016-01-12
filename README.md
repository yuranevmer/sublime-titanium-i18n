# sublime-titanium-i18n
Sublime Text 3 plugin for helping internalization process Titanium Mobile apps.

<img src="https://raw.github.com/yuranevmer/sublime-titanium-i18n/master/demo.gif" width="1000"/>
<!--
## Features :
 - Auto seearch
-->
## Installation :
<!--
### Using [Package Control][1] (*Recommended*)

For all Sublime Text 2/3 users we recommend install via [Package Control][1].

1. [Install][2] Package Control if you haven't yet.
2. Use <kbd>cmd</kbd>+<kbd>shift</kbd>+<kbd>P</kbd> then `Package Control: Install Package`
3. Look for `Markdown Preview` and install it.
-->
### Manual Install

1. Click the `Preferences > Browse Packages…` menu
2. Browse up a folder and then into the `Installed Packages/` folder
3. Download [zip package][zip] rename it to `Titanium i18n.sublime-package` and copy it into the `Installed Packages/` directory
4. Restart Sublime Text

## Usage :

<kbd>cmd</kbd>+<kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>a</kbd> is the default keymap. 

- If no text is selected, plugin tries to find and select text starting from the cursor position.
- If there is selected text, plugin checks for entries in the resource file `string.xml`. If record for this text exists, then text will be automatically replaced according to patterns:
  + `text="Some text"` -> `textid="some_text_id"`
  + `title="Some text"` -> `titleid="some_text_id"`
  + `"Some text"` -> `L('some_text_id')`
  + `'Some text'` -> `L('some_text_id')`
- If there is no record for selected text, you will be prompted to enter `text_id`. Then text will be replaced according to patterns. Resource string will be generated and added to the clipboard, also autowrited to `string.xml` right before mark `<!-- titanium_i18n: autowrite -->`



[home]: https://github.com/revolunet/sublimetext-markdown-preview
 [1]: https://packagecontrol.io/
 [2]: https://packagecontrol.io/installation
 [zip]: https://github.com/yuranevmer/sublime-titanium-i18n/archive/master.zip

 [issue]: https://github.com/revolunet/sublimetext-markdown-preview/issues
 [settings]: https://github.com/revolunet/sublimetext-markdown-preview/blob/master/MarkdownPreview.sublime-settings
