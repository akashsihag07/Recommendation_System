// The dataset has no poster images, so each card gets a colored gradient banner
// generated from its title instead. Same title always produces the same colors,
// which makes it look intentional and keeps the app self-contained (no image
// API or keys needed).

function hashString(str) {
  // basic string hash -> positive integer, enough to pick a hue from
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (h << 5) - h + str.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h);
}

export function bannerStyle(title) {
  const hue = hashString(title) % 360;
  const hue2 = (hue + 40) % 360;
  return {
    background: `linear-gradient(135deg, hsl(${hue}, 55%, 34%), hsl(${hue2}, 60%, 18%))`,
  };
}
