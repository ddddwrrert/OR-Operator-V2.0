import { createPlugin as base } from './plugin.js'
export { schedule } from './schedule.js'
import { schedule } from './schedule.js'

export function createPlugin(options) {
  return base(options, { version: '2.0', schedule })
}
export const { name, inject, apply } = createPlugin()

