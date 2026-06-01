# Install instructions (for the agent)

You are installing the **instagram-carousel** skills into the user's current project. Do this:

1. **Clone the repo** into a temporary location (or use it if already cloned):
   ```bash
   git clone https://github.com/EricTechPro/instagram-carousel-skills /tmp/instagram-carousel-skills
   ```

2. **Run the installer** targeting the user's current project (default) or globally:
   ```bash
   bash /tmp/instagram-carousel-skills/install.sh "$PWD"      # this project
   # or: bash /tmp/instagram-carousel-skills/install.sh --global   # all projects (~/.claude)
   ```
   This copies both skills into `.claude/skills/` and the shared assets (fonts, style
   references, logos) into `.claude/instagram-carousel/`.

3. **(Optional) Pin the assets path.** The generate skill auto-resolves
   `.claude/instagram-carousel/`, so this is only needed if the user keeps assets elsewhere:
   ```bash
   export IG_CAROUSEL_ASSETS="$PWD/.claude/instagram-carousel"   # or ~/.claude/instagram-carousel if --global
   ```

4. **Install Python deps** (used to crop/compose slides):
   ```bash
   pip install -r /tmp/instagram-carousel-skills/requirements.txt   # Pillow
   ```

5. **Tell the user about HiggsField** (only needed to *generate* images, not to *plan*):
   - CLI: `npm install -g @higgsfield/cli && higgsfield auth login` (verify: `higgsfield account status`), **or**
   - MCP: connect the HiggsField MCP in the host (Clockwork/cowork).

6. **Confirm** both skills are discoverable, then tell the user:
   > "Installed. Say *plan an instagram carousel for &lt;topic&gt;* to start."

Do not require Superpowers or any other repo. If `install.sh` reports a missing skill or asset,
stop and show the user the exact line.
