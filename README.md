# Learn Python

## mkdocs custom theme

[MkDocs 覆盖现有主题](https://mkdocs.org.cn/user-guide/customizing-your-theme/#customizing-your-theme)

theme.custom_dir 配置选项可用于指向一个目录，其中包含覆盖父主题中的文件的文件。父主题将是 theme.name 配置选项中定义的主题。custom_dir 中与父主题中文件同名的任何文件将替换父主题中同名文件。

所以可以通过浏览器网络请求复制某个文件内容到 custom_dir 对应目录，并修改其中内容。