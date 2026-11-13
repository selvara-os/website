---
title: Welcome to SelvaraOS
date: 2026-11-12
category: Announcement
author: SelvaraOS team
cover: img/welcome-cover.webp
cover_alt: The Grafite wallpaper, dark version
summary: What SelvaraOS is, the rules behind every decision, how the system works and what's coming next.
---

SelvaraOS is a free desktop operating system for PCs. It's built on Debian, it collects nothing about you, and it's designed to feel at home from the first minute, even if you've never used Linux before.

This is the first post on our new news page. From now on, releases, announcements and notes from development will appear here first. If you use a feed reader, you can follow along with [RSS](../feed.xml).

## Why another operating system

Most desktop systems make you choose: privacy or convenience, speed or good looks, freedom or simplicity. We don't think you should have to. SelvaraOS starts from six rules, and every decision has to respect all of them.

- **Private by design.** No telemetry, no accounts, no ads. Nothing connects to the internet unless you ask.
- **Smooth on older PCs.** Built for computers with 4 GB of memory. Speed comes from careful optimisation, never from switching features off.
- **Easy from the first minute.** Installing apps, updating, Wi-Fi and printers all work without a terminal.
- **Familiar if you come from a Mac.** A top bar, a dock, one search for everything and the keyboard shortcuts you already know.
- **Secure from the start.** Sandboxed apps, a firewall that blocks incoming connections and optional disk encryption.
- **The same everywhere.** One design and one vocabulary in every app, dialog and settings page.

## How it works

Underneath, SelvaraOS is Debian 13 with the KWin compositor on Wayland. On top of that runs a desktop written from scratch for SelvaraOS: the top bar, the dock, the app launcher, search, quick settings, notifications and the Settings app.

**Privacy is tested, not just promised.** Every build goes through automated tests that record all network traffic during start-up, login and five minutes at rest. The current result is zero outgoing connections. You can see the latest numbers on the [home page](../index.html).

**Updates are designed never to get in your way.** No forced restarts and no installs while you work. Checking for updates is something you switch on yourself in the welcome screen, and the system takes a snapshot before every update so you can go back if something breaks.

**Three update channels are on the way.** Dev Beta, Beta and Stable. You pick one, and you're never downgraded: if you move from a beta to Stable, you stay on your version until Stable catches up.

## Where we are

The foundation is in place: the start-up experience, the desktop, Settings, the welcome screen and the installer. Our own apps, the full set of languages and several privacy tools are still to come. The [features page](../features.html) lists every item with an honest status.

## Roadmap

The roadmap has been updated since this post. You'll find the current plan, step by step, in [Where SelvaraOS is today, and the road to Canopy 1.0](where-selvaraos-is-today.html).

## Get involved

Right now the best way to follow SelvaraOS is our Discord server. Previews go there first, and it's where you can tell us what you think. The code lives on [GitHub](https://github.com/selvara-os).

Thanks for being here this early.
