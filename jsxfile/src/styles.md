# styles.js

**What it is for:** Storing global CSS styles and injecting them into the document head.
**Technologies used:** JavaScript Template Literals, React (`useEffect`).
**Why:** This avoids reliance on CSS loaders or external stylesheets for simpler project scaffolding, adhering to the structure format without needing a heavy bundler config for CSS.
**How:** Exports a `STYLE` string containing all CSS. It also exports a `StyleTag` React component that creates a `<style>` DOM element on mount, inserts the CSS, appends it to `document.head`, and removes it on unmount.
