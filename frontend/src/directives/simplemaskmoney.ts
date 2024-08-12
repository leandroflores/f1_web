import { setMask, removeMask } from "simple-mask-money";

const config = {
  allowNegative: false,
  cursor: "move",
  decimalSeparator: ",",
  fixed: true,
  fractionDigits: 2,
  negativeSignAfter: false,
  prefix: "",
  suffix: "",
  thousandsSeparator: ".",
};

export default {
  mounted: (el: HTMLElement, binding: any) => {
    if (el instanceof HTMLInputElement) {
      setMask(el, config);
    } else {
      setMask(el.querySelector("input"), config);
    }
  },
  // updated(el: HTMLElement, binding: any) {
  //   const actualEl =
  //     el instanceof HTMLInputElement ? el : el.querySelector("input");
  //   console.log(actualEl?.value);

  //   if (actualEl?.value == "0") setMask(actualEl, binding.value);
  // },
  beforeUnmount: (el: HTMLElement) => {
    if (el instanceof HTMLInputElement) {
      removeMask(el);
    } else {
      removeMask(el.querySelector("input"));
    }
  },
};
