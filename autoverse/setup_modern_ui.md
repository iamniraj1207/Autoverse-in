# Setup Modern UI with React, Tailwind, and Radix (Shadcn)

Your current project is a Flask (Python) application using Jinja2 templates. To fully support and render the `.tsx` components (like the Timeline) with interactive `framer-motion` animations, you should initialize a frontend workspace.

## 1. Initialize a New Frontend (Next.js or Vite)
If you want to move to a modern full-stack setup:

### Option A: Next.js (Recommended)
```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint
```

### Option B: Vite (Lightweight)
```bash
npm create vite@latest frontend -- --template react-ts
# Then install tailwind
cd frontend
npm install -D tailwindcss携程 autoprefixer
npx tailwindcss init -p
```

## 2. Setup Shadcn CLI
Once your React project is initialized, run the shadcn init command to setup your `components.json` and themes:

```bash
npx shadcn-ui@latest init
```
- **Instructions**:
  - Choose "Default" style.
  - Choose "Slate" or "Zinc" color.
  - When asked for the path to components, use `components`.
  - When asked for the path to UI components, use `components/ui` (this is the industry standard for shadcn).

## 3. Install Dependencies
The provided components require these packages:

```bash
npm install framer-motion lucide-react clsx tailwind-merge
```

## 4. Why /components/ui?
In the shadcn/ui ecosystem, the `/components/ui/` folder is reserved for **atomic, reusable components** (buttons, inputs, timelines) that are managed by the CLI. Keeping them here ensures:
1. **Consistency**: Future components you add via `npx shadcn-ui@latest add [component]` will automatically go there.
2. **Maintenance**: You can easily separate your business logic components (in `/components/`) from your design system primitives (in `/components/ui/`).
