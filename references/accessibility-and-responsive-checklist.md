# Accessibility and Responsive Checklist

## Structure

- Exactly one clear primary page heading where appropriate.
- Landmark regions are meaningful and not duplicated unnecessarily.
- Heading levels describe hierarchy rather than visual size.
- Links navigate; buttons perform actions.

## Interaction

- Every form control has a visible or programmatic label.
- Keyboard focus is visible and the tab order is logical.
- Dialogs, menus, accordions, and toggles expose their state and can be operated by keyboard.
- Validation and status messages are understandable without relying only on color.

## Visuals

- Text and controls have sufficient contrast.
- Body text remains readable at narrow widths and increased browser font sizes.
- Images have useful alternative text, or empty alt text when decorative.
- Do not rely on hover as the only way to discover information.

## Responsive checks

- Test at approximately 320px, 768px, and 1280px viewport widths.
- Check overflow, clipped text, fixed elements, long labels, and touch target size.
- Check loading, empty, error, and success states when applicable.
- Respect `prefers-reduced-motion` and avoid essential information being conveyed only through animation.

