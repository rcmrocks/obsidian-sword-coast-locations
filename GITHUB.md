# Publishing this repo to GitHub

The project is ready to push. You need to create the repository on GitHub and add it as a remote.

## 1. Create the repository on GitHub

1. Go to [https://github.com/new](https://github.com/new).
2. **Repository name:** `obsidian-sword-coast-locations` (or any name you prefer).
3. **Description (optional):** e.g. "Generate Obsidian notes for every Sword Coast location from the AideDD map."
4. Choose **Public**.
5. **Do not** add a README, .gitignore, or license (this repo already has them).
6. Click **Create repository**.

## 2. Add the remote and push

GitHub will show you commands. Use these (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd C:\Users\mcdow\obsidian-sword-coast-locations
git remote add origin https://github.com/YOUR_USERNAME/obsidian-sword-coast-locations.git
git branch -M main
git push -u origin main
```

If you use SSH instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/obsidian-sword-coast-locations.git
git branch -M main
git push -u origin main
```

After the first push, your repo will be live. Update the clone URL in **README.md** (the `git clone` line) to use your real username if you used a placeholder.
