import { Store } from "pinia";
import { toRaw } from "vue";

export default function resetStore({ store }: { store: Store }) {
  const initialState = structuredClone(toRaw(store.$state));
  store.$reset = () => store.$patch(structuredClone(initialState));
}
