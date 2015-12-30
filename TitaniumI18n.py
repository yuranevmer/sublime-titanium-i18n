import sublime, sublime_plugin, re
search_next = False

class TitaniumI18nCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = sublime.load_settings("TitaniumI18n.sublime-settings")
		sel = self.view.sel()
		reg = sel[0]
		search_from = reg.begin()
		if reg.empty():
			lang_regexp = settings.get("lang_regexp") or "[а-яА-Я]"
			pattern_1 = "title=\"[^\"]*" + lang_regexp + "+[^\"]*\""
			pattern_2 = "text=\"[^\"]*" + lang_regexp + "+[^\"]*\""
			pattern_3 = "\"[^\"]*" + lang_regexp + "+[^\"]*\""
			pattern_4 = "\'[^\'']*" + lang_regexp + "+[^\'']*\'"

			finded_region = False

			if self.view.find(pattern_1, search_from):
				finded_region = self.view.find(pattern_1, search_from)
			elif self.view.find(pattern_2, search_from):
				finded_region = self.view.find(pattern_2, search_from)
			elif self.view.find(pattern_3, search_from):
				finded_region = self.view.find(pattern_3, search_from)
			elif self.view.find(pattern_4, search_from):
				finded_region = self.view.find(pattern_4, search_from)

			if (finded_region):
				sel.subtract(reg)
				sel.add(finded_region)
				self.view.show(finded_region)
		else:

			resourse_file = settings.get("strings_file")
			resourse_view = self.view.window().find_open_file(resourse_file)

			if (resourse_view is None):
				resourse_view = self.view.window().open_file(resourse_file)

			text = self.view.substr(reg)
			cutted_string = re.sub(r"^(text=|title=)?(\"|\')|(\"|\')$", "", text)

			pattern = "(<string name=\")(.*)(\">)(" + re.escape(cutted_string) + ")(<\/string>)"
			resourse_string_region = resourse_view.find(pattern, 0)

			if resourse_string_region.empty():
				self.view.window().show_input_panel("Please enter a text_id:", '', lambda s: self.view.run_command("titanium_i18n_replace", {"replace_text": s, "resourse_file": resourse_file}), None, None)
			else:
				resourse_string = resourse_view.substr(resourse_string_region)
				m = re.search(pattern, resourse_string)
				self.view.run_command("titanium_i18n_replace", {"replace_text": m.group(2)})



class TitaniumI18nReplaceCommand(sublime_plugin.TextCommand):
	def run(self, edit, replace_text, resourse_file=None):
		sel = self.view.sel()
		reg = sel[0]
		text_id = replace_text
		selected_text = self.view.substr(reg)
		replacement = "L('" + text_id + "')"

		if re.search("^'.*'$", selected_text):
			selected_text = re.sub(r"^'|'$", "", selected_text)
		elif re.search('^".*"$', selected_text):
			selected_text = re.sub(r'^"|"$', "", selected_text)
		elif re.search("^title=(\"|\').*(\"|\')$", selected_text):
			selected_text = re.sub(r"^title=(\"|\')|(\"|\')$", "", selected_text)
			replacement = 'titleid="' + text_id + '"'
		elif re.search("^text=(\"|\').*(\"|\')$", selected_text):
			selected_text = re.sub(r"^text=(\"|\')|(\"|\')$", "", selected_text)
			replacement = 'textid="' + text_id + '"'

		self.view.replace(edit, reg, replacement)

		resourse_string = '<string name="' + text_id + '">' + selected_text + '</string>'
		sublime.set_clipboard(resourse_string)

		sel.clear()
		cursor_end = reg.begin() + len(replacement)
		sel.add(sublime.Region(cursor_end, cursor_end))

		print(resourse_file)
		if resourse_file is not None :
			auto_write_mark = "<!-- titanium_i18n: autowrite -->"
			resourse_view = self.view.window().find_open_file(resourse_file)
			resourse_string_region = resourse_view.find(auto_write_mark, 0)

			if resourse_string_region.empty(): 
				return

			resourse_string_point_before = sublime.Region(resourse_string_region.begin(), resourse_string_region.begin())
			resourse_sel = resourse_view.sel()
			resourse_sel.clear()
			resourse_sel.add(resourse_string_point_before)
			resourse_view.run_command("insert", {"characters": resourse_string + "\n"})
			resourse_view.run_command("save", {})
