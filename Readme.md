# 关于latex
## VSCode插件
使用[latex-workshop](https://github.com/James-Yu/LaTeX-Workshop)

preview使用browser，方便多屏工作。

## 模板(cls file)
使用的模板是[ElegantPaper](https://github.com/ElegantLaTeX/ElegantPaper)。

如果用的是texlive2021，那么因为elegantpaper更新过一次，所以需要手动更新一下`elegantpaper.cls`。
更新方法：
1. `kpsewhich elegantpaper.cls`得到当前使用的`elegantpaper.cls`的路径
2. 从github上把新的`elegantpaper.cls`下下来，覆盖掉上一步找到的那个
3. 结束

## 引用(bib file)
1. `kpsewhich -var-value=TEXMFHOME`找到tex的根目录，记为`$TEXMFHOME`
2. 把bib文件放到`$TEXMFHOME/bibtex/bib/MINE`下（MINE是自己命名的一个子目录）
	* 在用zotero导出时可以选择keep updated，那样就不用每次都自己手动更新了。
