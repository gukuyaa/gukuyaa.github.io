# lovyy 的博客

个人博客，记录 ACM / C++ 竞赛模板、题解与学习笔记。

- 地址：https://gukuyaa.github.io/
- 框架：[Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
- 托管：GitHub Pages（GitHub Actions 自动部署）

## 本地预览

```bash
# 需要 Hugo extended >= 0.158
hugo server -D
# 打开 http://localhost:1313/
```

## 新建文章

```bash
hugo new posts/my-new-post.md
# 需要数学公式时把 front matter 里的 math 改成 true
```

## 迁移洛谷专栏

```bash
python3 scripts/luogu_import.py <洛谷专栏/文章链接> ...
```
