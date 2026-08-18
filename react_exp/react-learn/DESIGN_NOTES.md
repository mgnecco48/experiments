# Page Structure And Design Notes

This file documents the current page structure and visual decisions for future sections of the salsa shop.

## App Structure

Use this structure for new top-level views:

```tsx
<div className="font-roboto min-h-screen bg-[#f5f0e6] px-4 py-6 sm:px-8 lg:px-12">
    <PageHeader />

    <section className="mx-auto mt-10 max-w-7xl rounded-3xl bg-red-100 px-4 py-8 shadow-sm sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Section title
        </h2>

        {/* Section content */}
    </section>
</div>
```

## Shared Components

Current shared components in `src/App.tsx`:

- `PageHeader`: shared title/header used across shop and order overview views.
- `CartTotal`: fixed cart bubble in the top-right corner.
- `CardCounter`: plus/minus quantity selector for product cards.
- `OrderOverview`: post-order summary page.

Future sections should reuse `PageHeader` so the app feels consistent across views.

## Layout Decisions

- Mobile-first layout using Tailwind responsive classes.
- Main page wrapper uses `px-4 py-6` on mobile, then increases spacing on larger screens with `sm:px-8 lg:px-12`.
- Main content sections use `max-w-7xl` to avoid stretching too wide on desktop.
- Product-like content uses a responsive grid: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`.
- Cards use square images with `aspect-square` and `object-cover` for consistent product presentation.
- The cart is fixed with `fixed right-3 top-3 z-50 sm:right-6 sm:top-6` so it stays visible while scrolling.

## Colors

- Page background: `#f5f0e6`, a warm cream tone.
- Section background: `bg-red-100`, used for product grid and order overview sections.
- Primary action color: `bg-red-600`.
- Primary action hover: `hover:bg-red-700`.
- Card background: `bg-white`.
- Main text: `text-gray-900`.
- Supporting text: `text-gray-500` / `text-gray-600`.

Keep future sections within this warm cream/red palette unless there is a specific reason to introduce a new color.

## Typography

Configured in `src/App.css`:

- Display/header font: `font-pirata`, mapped to `Pirata One`.
- Body/UI font: `font-roboto`, mapped to `Roboto Condensed`.

Usage:

- Use `font-pirata` only for the main brand header.
- Use `font-roboto` for page body, cards, buttons, prices, and cart UI.
- Main header size: `text-6xl sm:text-6xl lg:text-9xl`.
- Section headings: `text-3xl font-bold`.
- Product/card text: generally `text-base`.
- Main action buttons: `text-xl font-semibold`.

## Card Pattern

Use this pattern for salsa/product-like cards:

```tsx
<div className="rounded-2xl bg-white p-3 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
    <img
        alt="Product name"
        src={imageUrl}
        className="aspect-square w-full rounded-xl bg-gray-200 object-cover"
    />

    <div className="mt-4 flex justify-between gap-4">
        <div>
            <h3 className="text-base font-semibold text-gray-900">Product name</h3>
            <p className="mt-1 text-base text-gray-500">Supporting detail</p>
        </div>
        <p className="shrink-0 text-base font-medium text-gray-900">Price</p>
    </div>
</div>
```

## Button Pattern

Use this for primary full-width actions:

```tsx
<button className="mt-8 w-full rounded-xl bg-red-600 py-4 text-xl font-semibold text-white hover:bg-red-700">
    Button text
</button>
```

## State And View Decisions

- The app currently uses state-based view switching instead of routing.
- `orderItems.length > 0` switches from the salsa selection view to the order overview view.
- This is intentionally simple while there are only two views.
- Add React Router later if the app needs URLs like `/salsas`, `/order`, `/checkout`, or product detail pages.

## Future Section Guidelines

- Keep sections inside the same cream page wrapper.
- Use the red rounded section container for major content areas.
- Use white rounded cards for individual items or summaries.
- Keep text large enough for mobile readability.
- Avoid adding extra nested wrappers unless they solve a layout problem.
- Prefer one shared component when the same visual pattern appears in multiple views.
