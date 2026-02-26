# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## ⚠️ Important Config Constraints

### Gateway Bind
- **DO NOT change** `gateway.bind` from `"loopback"` to `"0.0.0.0"`
- Changing it breaks the gateway — service won't start
- Current setup: WSL gateway, Windows access via WSL network

---

## API Keys & Credentials

### Tavily Search
- API Key: 已配置到 `~/.bashrc`
- 用法: `node {skills/tavily-search}/scripts/search.mjs "query"`

---

Add whatever helps you do your job. This is your cheat sheet.
