export function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}