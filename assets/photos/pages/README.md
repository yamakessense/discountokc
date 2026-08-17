# Drop photos here

One folder per page. Drop a photo in and it appears on that page — no code
change, no build step, nothing to install.

## The folder names

| Folder | Page |
|---|---|
| `home/` | the front page |
| `vanities/` `flooring/` `bath/` `kitchen/` | those category pages |
| `lighting/` `tools/` `patio/` | those category pages |
| `rubbermulchokc/` `bulk-rubber-mulch/` | the two mulch pages |
| `inventory/` `deals/` `about/` `location/` `contact/` | those pages |

Create the folder if it isn't there yet.

## How to add a photo, from a phone or a laptop

1. Go to the repository on github.com and open `assets/photos/pages/`.
2. Click the folder for the page you want.
3. **Add file → Upload files**, pick the photo, then **Commit changes**.

That's it. Within a couple of minutes the photo is optimised and live.

## Name the file like a sentence — it becomes the alt text

The filename is what a screen reader reads aloud and what Google and AI
assistants use to understand the picture. So name it like you'd describe it:

```
red rubber mulch supersack at the south okc store.jpg
60 inch double vanity with stone top.jpg
```

Those become "Red rubber mulch supersack at the south okc store" and so on.

Put a number in front to control the order — `01-`, `02-`. The number is
stripped from the alt text.

```
01-ceiling fans down the aisle.jpg
02-outdoor fans by the door.jpg
```

## What happens after you upload

A robot converts the photo to WebP, shrinks it to 1200px wide, and makes 800px
and 400px versions so phones download a small file instead of a big one. Then it
deletes your original and commits the tidy versions. You don't do anything.

**Upload straight off the phone — don't shrink it first.** Bigger is better
here; the robot handles the shrinking, and it never enlarges a small photo.

## Removing a photo

Open the file on github.com, click the bin icon, commit. Delete the `@400` and
`@800` versions of it too, or leave them — they're harmless either way.
