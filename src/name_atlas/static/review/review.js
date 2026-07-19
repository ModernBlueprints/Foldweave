//#region \0rolldown/runtime.js
var e = Object.create, t = Object.defineProperty, n = Object.getOwnPropertyDescriptor, r = Object.getOwnPropertyNames, i = Object.getPrototypeOf, a = Object.prototype.hasOwnProperty, o = (e, t, n) => () => {
	if (n) throw n[0];
	try {
		return e && (t = e(e = 0)), t;
	} catch (e) {
		throw n = [e], e;
	}
}, s = (e, t) => () => (t || (e((t = { exports: {} }).exports, t), e = null), t.exports), c = (e, n) => {
	let r = {};
	for (var i in e) t(r, i, {
		get: e[i],
		enumerable: !0
	});
	return n || t(r, Symbol.toStringTag, { value: "Module" }), r;
}, l = (e, i, o, s) => {
	if (i && typeof i == "object" || typeof i == "function") for (var c = r(i), l = 0, u = c.length, d; l < u; l++) d = c[l], !a.call(e, d) && d !== o && t(e, d, {
		get: ((e) => i[e]).bind(null, d),
		enumerable: !(s = n(i, d)) || s.enumerable
	});
	return e;
}, u = (n, r, a) => (a = n == null ? {} : e(i(n)), l(r || !n || !n.__esModule ? t(a, "default", {
	value: n,
	enumerable: !0
}) : a, n)), d = {
	CENTER: "center",
	END: "end",
	LEFT: "left",
	RIGHT: "right",
	START: "start"
}, f = {
	ZERO: 0,
	ONE: 1,
	TWO: 2,
	THREE: 3,
	FOUR: 4
}, p = {
	NONE: "none",
	PRIMARY: "primary",
	SUCCESS: "success",
	WARNING: "warning",
	DANGER: "danger"
}, m = {
	BOTTOM: "bottom",
	BOTTOM_LEFT: "bottom-left",
	BOTTOM_RIGHT: "bottom-right",
	LEFT: "left",
	LEFT_BOTTOM: "left-bottom",
	LEFT_TOP: "left-top",
	RIGHT: "right",
	RIGHT_BOTTOM: "right-bottom",
	RIGHT_TOP: "right-top",
	TOP: "top",
	TOP_LEFT: "top-left",
	TOP_RIGHT: "top-right"
}, h = "bp6";
typeof BLUEPRINT_NAMESPACE < "u" ? h = BLUEPRINT_NAMESPACE : typeof REACT_APP_BLUEPRINT_NAMESPACE < "u" && (h = REACT_APP_BLUEPRINT_NAMESPACE);
var g = `${h}-active`, _ = `${h}-align-left`, v = `${h}-align-right`, y = `${h}-compact`;
`${h}`;
var b = `${h}-disabled`, x = `${h}-fill`;
`${h}`, `${h}`;
var ee = `${h}-inline`, te = `${h}-interactive`, S = `${h}-large`, C = `${h}-loading`, ne = `${h}-minimal`, re = `${h}-outlined`;
`${h}`, `${h}`;
var ie = `${h}-read-only`, ae = `${h}-round`, oe = `${h}-selected`, se = `${h}-small`, ce = `${h}-vertical`;
wt(m.TOP), wt(m.BOTTOM), wt(m.LEFT), wt(m.RIGHT), xt(f.ZERO), xt(f.ONE), xt(f.TWO), xt(f.THREE), xt(f.FOUR), Ct(p.PRIMARY), Ct(p.SUCCESS), Ct(p.WARNING), Ct(p.DANGER), `${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`;
var le = `${h}-text-overflow-ellipsis`, w = `${h}-blockquote`, ue = `${h}-code`, de = `${h}-code-block`, T = `${h}-heading`, fe = `${h}-list`;
`${h}`, `${h}`;
var pe = `${h}-alert`;
`${pe}`, `${pe}`, `${pe}`;
var me = `${h}-breadcrumb`;
`${me}`, `${me}`, `${me}`;
var he = `${h}-button`, ge = `${he}-group`, _e = `${he}-spinner`, ve = `${he}-text`, ye = `${h}-callout`;
`${ye}`, `${ye}`;
var be = `${h}-card`;
`${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`;
var xe = `${h}-context-menu`;
`${xe}`, `${xe}`, `${xe}`, `${h}`;
var Se = `${h}-dialog`;
`${Se}`, `${Se}`, `${Se}`, `${Se}`, `${Se}`, `${Se}`, `${Se}`, `${Se}`, `${Se}`;
var Ce = `${h}-dialog-step`;
`${Ce}`, `${Ce}`, `${Ce}`, `${Ce}`, `${h}`;
var we = `${h}-drawer`;
`${we}`, `${we}`, `${we}`;
var Te = `${h}-editable-text`;
`${Te}`, `${Te}`, `${Te}`, `${Te}`;
var Ee = `${h}-entity-title`;
`${h}`, `${Ee}`, `${Ee}`, `${Ee}`, `${Ee}`, `${Ee}`, `${Ee}`, `${Ee}`, `${h}`, `${h}`;
var De = `${h}-html-table`;
`${De}`, `${De}`;
var Oe = `${h}-input`;
`${Oe}`;
var ke = `${Oe}-group`, Ae = `${Oe}-left-container`, je = `${Oe}-action`;
`${h}`, `${h}`;
var Me = `${h}-control`, Ne = `${Me}-input`, Pe = `${Me}-indicator`, Fe = `${Pe}-child`, Ie = `${h}-checkbox`, Le = `${h}-radio`;
`${h}`;
var Re = `${h}-switch`, ze = `${Re}-inner-text`;
`${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`;
var Be = `${h}-hotkey`;
`${Be}`, `${Be}`, `${Be}`;
var Ve = `${h}-label`;
`${h}`, `${h}`, `${h}`, `${h}`;
var He = `${h}-link`;
`${He}`, `${He}`, `${He}`, `${He}`;
var Ue = `${h}-menu`, We = `${Ue}-item`;
`${We}`, `${We}`, `${We}`, `${We}`, `${h}`, `${Ue}`, `${Ue}`;
var Ge = `${h}-multistep-dialog`;
`${Ge}`, `${Ge}`, `${Ge}`, `${Ge}`, `${Ge}`;
var Ke = `${h}-section`;
`${Ke}`;
var qe = `${Ke}-header`;
`${qe}`, `${qe}`, `${qe}`, `${qe}`, `${qe}`, `${qe}`, `${qe}`, `${Ke}`;
var Je = `${h}-navbar`;
`${Je}`, `${Je}`, `${Je}`;
var Ye = `${h}-non-ideal-state`, Xe = `${Ye}-visual`, Ze = `${Ye}-text`;
`${h}`, `${h}`;
var Qe = `${h}-overlay`;
`${Qe}`, `${Qe}`, `${Qe}`, `${Qe}`, `${Qe}`, `${Qe}`, `${Qe}`, `${Qe}`;
var $e = `${h}-panel-stack2`;
`${$e}`, `${$e}`, `${$e}`;
var et = `${h}-popover`;
`${et}`, `${et}`, `${et}`;
var tt = `${et}-content`;
`${et}`, `${tt}`, `${et}`, `${et}`, `${et}`, `${et}`, `${et}`, `${et}`, `${et}`, `${et}`, `${et}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`, `${h}`;
var nt = `${h}-slider`;
`${nt}`, `${nt}`, `${nt}`, `${nt}`, `${nt}`, `${h}`, `${h}`;
var rt = `${h}-spinner`, it = `${rt}-animation`, at = `${rt}-head`, ot = `${h}-no-spin`, st = `${rt}-track`;
`${h}`;
var ct = `${h}-tab`;
`${ct}`, `${ct}`, `${ct}`, `${ct}`, `${ct}`, `${ct}`;
var lt = `${h}-tag`, ut = `${lt}-remove`, dt = `${h}-compound-tag`;
`${dt}`, `${dt}`, `${dt}`, `${dt}`;
var ft = `${h}-tag-input`;
`${ft}`, `${ft}`;
var pt = `${h}-toast`;
`${pt}`, `${pt}`, `${h}`, `${h}`;
var mt = `${h}-tree-node`, ht = `${mt}-caret`;
`${ht}`, `${ht}`, `${ht}`, `${mt}`, `${mt}`, `${mt}`, `${mt}`, `${mt}`, `${mt}`, `${mt}`, `${h}`;
var gt = `${h}-icon`, _t = `${gt}-standard`, vt = `${gt}-large`, yt = `${gt}-muted`;
function bt(e) {
	switch (e) {
		case d.LEFT:
		case d.START: return _;
		case d.RIGHT:
		case d.END: return v;
		default: return;
	}
}
function xt(e) {
	if (e !== void 0) return `${h}-elevation-${e}`;
}
function St(e) {
	if (e != null) return e.indexOf(`${h}-icon-`) === 0 ? e : `${h}-icon-${e}`;
}
function Ct(e) {
	if (!(e == null || e === p.NONE)) return `${h}-intent-${e.toLowerCase()}`;
}
function wt(e) {
	if (e !== void 0) return `${h}-position-${e}`;
}
function Tt(e, t) {
	if (e === "small") return se;
	if (e === "large") return S;
	let { large: n = !1, small: r = !1 } = t;
	return {
		[S]: n,
		[se]: r
	};
}
function Et(e, t) {
	if (e === "outlined") return re;
	if (e === "minimal") return ne;
	let { minimal: n = !1, outlined: r = !1 } = t;
	return {
		[ne]: n,
		[re]: r
	};
}
//#endregion
//#region node_modules/react/cjs/react.production.min.js
var Dt = /* @__PURE__ */ s(((e) => {
	var t = Symbol.for("react.element"), n = Symbol.for("react.portal"), r = Symbol.for("react.fragment"), i = Symbol.for("react.strict_mode"), a = Symbol.for("react.profiler"), o = Symbol.for("react.provider"), s = Symbol.for("react.context"), c = Symbol.for("react.forward_ref"), l = Symbol.for("react.suspense"), u = Symbol.for("react.memo"), d = Symbol.for("react.lazy"), f = Symbol.iterator;
	function p(e) {
		return typeof e != "object" || !e ? null : (e = f && e[f] || e["@@iterator"], typeof e == "function" ? e : null);
	}
	var m = {
		isMounted: function() {
			return !1;
		},
		enqueueForceUpdate: function() {},
		enqueueReplaceState: function() {},
		enqueueSetState: function() {}
	}, h = Object.assign, g = {};
	function _(e, t, n) {
		this.props = e, this.context = t, this.refs = g, this.updater = n || m;
	}
	_.prototype.isReactComponent = {}, _.prototype.setState = function(e, t) {
		if (typeof e != "object" && typeof e != "function" && e != null) throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
		this.updater.enqueueSetState(this, e, t, "setState");
	}, _.prototype.forceUpdate = function(e) {
		this.updater.enqueueForceUpdate(this, e, "forceUpdate");
	};
	function v() {}
	v.prototype = _.prototype;
	function y(e, t, n) {
		this.props = e, this.context = t, this.refs = g, this.updater = n || m;
	}
	var b = y.prototype = new v();
	b.constructor = y, h(b, _.prototype), b.isPureReactComponent = !0;
	var x = Array.isArray, ee = Object.prototype.hasOwnProperty, te = { current: null }, S = {
		key: !0,
		ref: !0,
		__self: !0,
		__source: !0
	};
	function C(e, n, r) {
		var i, a = {}, o = null, s = null;
		if (n != null) for (i in n.ref !== void 0 && (s = n.ref), n.key !== void 0 && (o = "" + n.key), n) ee.call(n, i) && !S.hasOwnProperty(i) && (a[i] = n[i]);
		var c = arguments.length - 2;
		if (c === 1) a.children = r;
		else if (1 < c) {
			for (var l = Array(c), u = 0; u < c; u++) l[u] = arguments[u + 2];
			a.children = l;
		}
		if (e && e.defaultProps) for (i in c = e.defaultProps, c) a[i] === void 0 && (a[i] = c[i]);
		return {
			$$typeof: t,
			type: e,
			key: o,
			ref: s,
			props: a,
			_owner: te.current
		};
	}
	function ne(e, n) {
		return {
			$$typeof: t,
			type: e.type,
			key: n,
			ref: e.ref,
			props: e.props,
			_owner: e._owner
		};
	}
	function re(e) {
		return typeof e == "object" && !!e && e.$$typeof === t;
	}
	function ie(e) {
		var t = {
			"=": "=0",
			":": "=2"
		};
		return "$" + e.replace(/[=:]/g, function(e) {
			return t[e];
		});
	}
	var ae = /\/+/g;
	function oe(e, t) {
		return typeof e == "object" && e && e.key != null ? ie("" + e.key) : t.toString(36);
	}
	function se(e, r, i, a, o) {
		var s = typeof e;
		(s === "undefined" || s === "boolean") && (e = null);
		var c = !1;
		if (e === null) c = !0;
		else switch (s) {
			case "string":
			case "number":
				c = !0;
				break;
			case "object": switch (e.$$typeof) {
				case t:
				case n: c = !0;
			}
		}
		if (c) return c = e, o = o(c), e = a === "" ? "." + oe(c, 0) : a, x(o) ? (i = "", e != null && (i = e.replace(ae, "$&/") + "/"), se(o, r, i, "", function(e) {
			return e;
		})) : o != null && (re(o) && (o = ne(o, i + (!o.key || c && c.key === o.key ? "" : ("" + o.key).replace(ae, "$&/") + "/") + e)), r.push(o)), 1;
		if (c = 0, a = a === "" ? "." : a + ":", x(e)) for (var l = 0; l < e.length; l++) {
			s = e[l];
			var u = a + oe(s, l);
			c += se(s, r, i, u, o);
		}
		else if (u = p(e), typeof u == "function") for (e = u.call(e), l = 0; !(s = e.next()).done;) s = s.value, u = a + oe(s, l++), c += se(s, r, i, u, o);
		else if (s === "object") throw r = String(e), Error("Objects are not valid as a React child (found: " + (r === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : r) + "). If you meant to render a collection of children, use an array instead.");
		return c;
	}
	function ce(e, t, n) {
		if (e == null) return e;
		var r = [], i = 0;
		return se(e, r, "", "", function(e) {
			return t.call(n, e, i++);
		}), r;
	}
	function le(e) {
		if (e._status === -1) {
			var t = e._result;
			t = t(), t.then(function(t) {
				(e._status === 0 || e._status === -1) && (e._status = 1, e._result = t);
			}, function(t) {
				(e._status === 0 || e._status === -1) && (e._status = 2, e._result = t);
			}), e._status === -1 && (e._status = 0, e._result = t);
		}
		if (e._status === 1) return e._result.default;
		throw e._result;
	}
	var w = { current: null }, ue = { transition: null }, de = {
		ReactCurrentDispatcher: w,
		ReactCurrentBatchConfig: ue,
		ReactCurrentOwner: te
	};
	function T() {
		throw Error("act(...) is not supported in production builds of React.");
	}
	e.Children = {
		map: ce,
		forEach: function(e, t, n) {
			ce(e, function() {
				t.apply(this, arguments);
			}, n);
		},
		count: function(e) {
			var t = 0;
			return ce(e, function() {
				t++;
			}), t;
		},
		toArray: function(e) {
			return ce(e, function(e) {
				return e;
			}) || [];
		},
		only: function(e) {
			if (!re(e)) throw Error("React.Children.only expected to receive a single React element child.");
			return e;
		}
	}, e.Component = _, e.Fragment = r, e.Profiler = a, e.PureComponent = y, e.StrictMode = i, e.Suspense = l, e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = de, e.act = T, e.cloneElement = function(e, n, r) {
		if (e == null) throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
		var i = h({}, e.props), a = e.key, o = e.ref, s = e._owner;
		if (n != null) {
			if (n.ref !== void 0 && (o = n.ref, s = te.current), n.key !== void 0 && (a = "" + n.key), e.type && e.type.defaultProps) var c = e.type.defaultProps;
			for (l in n) ee.call(n, l) && !S.hasOwnProperty(l) && (i[l] = n[l] === void 0 && c !== void 0 ? c[l] : n[l]);
		}
		var l = arguments.length - 2;
		if (l === 1) i.children = r;
		else if (1 < l) {
			c = Array(l);
			for (var u = 0; u < l; u++) c[u] = arguments[u + 2];
			i.children = c;
		}
		return {
			$$typeof: t,
			type: e.type,
			key: a,
			ref: o,
			props: i,
			_owner: s
		};
	}, e.createContext = function(e) {
		return e = {
			$$typeof: s,
			_currentValue: e,
			_currentValue2: e,
			_threadCount: 0,
			Provider: null,
			Consumer: null,
			_defaultValue: null,
			_globalName: null
		}, e.Provider = {
			$$typeof: o,
			_context: e
		}, e.Consumer = e;
	}, e.createElement = C, e.createFactory = function(e) {
		var t = C.bind(null, e);
		return t.type = e, t;
	}, e.createRef = function() {
		return { current: null };
	}, e.forwardRef = function(e) {
		return {
			$$typeof: c,
			render: e
		};
	}, e.isValidElement = re, e.lazy = function(e) {
		return {
			$$typeof: d,
			_payload: {
				_status: -1,
				_result: e
			},
			_init: le
		};
	}, e.memo = function(e, t) {
		return {
			$$typeof: u,
			type: e,
			compare: t === void 0 ? null : t
		};
	}, e.startTransition = function(e) {
		var t = ue.transition;
		ue.transition = {};
		try {
			e();
		} finally {
			ue.transition = t;
		}
	}, e.unstable_act = T, e.useCallback = function(e, t) {
		return w.current.useCallback(e, t);
	}, e.useContext = function(e) {
		return w.current.useContext(e);
	}, e.useDebugValue = function() {}, e.useDeferredValue = function(e) {
		return w.current.useDeferredValue(e);
	}, e.useEffect = function(e, t) {
		return w.current.useEffect(e, t);
	}, e.useId = function() {
		return w.current.useId();
	}, e.useImperativeHandle = function(e, t, n) {
		return w.current.useImperativeHandle(e, t, n);
	}, e.useInsertionEffect = function(e, t) {
		return w.current.useInsertionEffect(e, t);
	}, e.useLayoutEffect = function(e, t) {
		return w.current.useLayoutEffect(e, t);
	}, e.useMemo = function(e, t) {
		return w.current.useMemo(e, t);
	}, e.useReducer = function(e, t, n) {
		return w.current.useReducer(e, t, n);
	}, e.useRef = function(e) {
		return w.current.useRef(e);
	}, e.useState = function(e) {
		return w.current.useState(e);
	}, e.useSyncExternalStore = function(e, t, n) {
		return w.current.useSyncExternalStore(e, t, n);
	}, e.useTransition = function() {
		return w.current.useTransition();
	}, e.version = "18.3.1";
})), Ot = /* @__PURE__ */ s(((e, t) => {
	t.exports = Dt();
}));
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/utils/domUtils.js
function E() {
	return typeof window < "u" && window.document != null;
}
[
	"a[href]:not([tabindex=\"-1\"])",
	"button:not([disabled]):not([tabindex=\"-1\"])",
	"details:not([tabindex=\"-1\"])",
	"input:not([disabled]):not([tabindex=\"-1\"])",
	"select:not([disabled]):not([tabindex=\"-1\"])",
	"textarea:not([disabled]):not([tabindex=\"-1\"])",
	"[tabindex]:not([tabindex=\"-1\"])"
].join(",");
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/utils/functionUtils.js
/* istanbul ignore next */
function kt(e) {
	return typeof e == "function";
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/errors.js
var At = "[Blueprint]", jt = "[Blueprint] clamp: max cannot be less than min", Mt = "[Blueprint] <InputGroup> leftElement and leftIcon prop are mutually exclusive, with leftElement taking priority.";
`${At}`, `${At}`, `${At}`;
var Nt = "[Blueprint] <Spinner> Classes.SMALL/LARGE are ignored if size prop is set.", D = /* @__PURE__ */ u(Ot());
function Pt(e) {
	return typeof NODE_ENV < "u" && NODE_ENV === e;
}
function Ft(e, t, n) {
	if (e == null) return e;
	if (n < t) throw Error(jt);
	return Math.min(Math.max(e, t), n);
}
function It(e) {
	return typeof e == "string" && e.trim().length === 0;
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/props.js
var O = "Blueprint6", Lt = /* @__PURE__ */ "active.alignText.asyncControl.containerRef.current.elementRef.ellipsizeText.endIcon.fill.icon.iconSize.inputClassName.inputRef.intent.inline.large.loading.leftElement.leftIcon.minimal.onRemove.outlined.panel.panelClassName.popoverProps.rightElement.rightIcon.round.selectedValue.size.small.tagName.text.textClassName.variant".split(".");
function Rt(e, t = Lt, n = !1) {
	return n && (t = t.concat(Lt)), t.reduce((e, t) => (t.indexOf("-") === -1 && e.hasOwnProperty(t) && delete e[t], e), { ...e });
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/utils/reactUtils.js
function zt(e, t = !1) {
	return e == null || e === "" || e === !1 || !t && Array.isArray(e) && (e.length === 0 || e.every((e) => zt(e, !0)));
}
function Bt(e, t = "span", n = {}) {
	if (!(e == null || typeof e == "boolean" || It(e))) return typeof e == "string" || typeof e == "number" || Ht(e) || Ut(e) ? (0, D.createElement)(t, n, e) : Vt(e) ? Object.keys(n).length > 0 ? (0, D.cloneElement)(e, n) : e : void 0;
}
function Vt(e) {
	return typeof e == "object" && e.type !== void 0 && e.props !== void 0;
}
function Ht(e) {
	return typeof e.type == "symbol";
}
function Ut(e) {
	return Array.isArray(e);
}
var Wt = `${O}.Icon.`;
function Gt(e) {
	if (!(0, D.isValidElement)(e)) return !1;
	let { type: t } = e;
	if (typeof t == "string") return !1;
	let { displayName: n } = t;
	return typeof n == "string" && n.startsWith(Wt);
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/utils/keyboardUtils.js
function Kt(e) {
	return e.key === "Enter" || e.key === " ";
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/refs.js
function qt(e) {
	return e != null && typeof e != "function";
}
function Jt(e) {
	return typeof e == "function";
}
function Yt(e, t) {
	qt(e) ? e.current = t : Jt(e) && e(t);
}
function Xt(...e) {
	return (t) => {
		e.forEach((e) => {
			Yt(e, t);
		});
	};
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/common/abstractPureComponent.js
var Zt = class extends D.PureComponent {
	componentWillUpdate;
	componentWillReceiveProps;
	componentWillMount;
	getDerivedStateFromProps;
	displayName;
	timeoutIds = [];
	requestIds = [];
	constructor(e) {
		super(e), Pt("production") || this.validateProps(this.props);
	}
	componentDidUpdate(e, t, n) {
		Pt("production") || this.validateProps(this.props);
	}
	componentWillUnmount() {
		this.clearTimeouts(), this.cancelAnimationFrames();
	}
	requestAnimationFrame(e) {
		let t = window.requestAnimationFrame(e);
		return this.requestIds.push(t), () => window.cancelAnimationFrame(t);
	}
	setTimeout(e, t) {
		let n = window.setTimeout(e, t);
		return this.timeoutIds.push(n), () => window.clearTimeout(n);
	}
	clearTimeouts = () => {
		if (this.timeoutIds.length > 0) {
			for (let e of this.timeoutIds) window.clearTimeout(e);
			this.timeoutIds = [];
		}
	};
	cancelAnimationFrames = () => {
		if (this.requestIds.length > 0) {
			for (let e of this.requestIds) window.cancelAnimationFrame(e);
			this.requestIds = [];
		}
	};
	validateProps(e) {}
}, k = /* @__PURE__ */ s(((e) => {
	var t = Ot(), n = Symbol.for("react.element"), r = Symbol.for("react.fragment"), i = Object.prototype.hasOwnProperty, a = t.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, o = {
		key: !0,
		ref: !0,
		__self: !0,
		__source: !0
	};
	function s(e, t, r) {
		var s, c = {}, l = null, u = null;
		for (s in r !== void 0 && (l = "" + r), t.key !== void 0 && (l = "" + t.key), t.ref !== void 0 && (u = t.ref), t) i.call(t, s) && !o.hasOwnProperty(s) && (c[s] = t[s]);
		if (e && e.defaultProps) for (s in t = e.defaultProps, t) c[s] === void 0 && (c[s] = t[s]);
		return {
			$$typeof: n,
			type: e,
			key: l,
			ref: u,
			props: c,
			_owner: a.current
		};
	}
	e.Fragment = r, e.jsx = s, e.jsxs = s;
})), Qt = /* @__PURE__ */ s(((e, t) => {
	t.exports = k();
})), $t = /* @__PURE__ */ s(((e, t) => {
	(function() {
		var e = {}.hasOwnProperty;
		function n() {
			for (var e = "", t = 0; t < arguments.length; t++) {
				var n = arguments[t];
				n && (e = i(e, r(n)));
			}
			return e;
		}
		function r(t) {
			if (typeof t == "string" || typeof t == "number") return t;
			if (typeof t != "object") return "";
			if (Array.isArray(t)) return n.apply(null, t);
			if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]")) return t.toString();
			var r = "";
			for (var a in t) e.call(t, a) && t[a] && (r = i(r, a));
			return r;
		}
		function i(e, t) {
			return t ? e ? e + " " + t : e + t : e;
		}
		t !== void 0 && t.exports ? (n.default = n, t.exports = n) : typeof define == "function" && typeof define.amd == "object" && define.amd ? define("classnames", [], function() {
			return n;
		}) : window.classNames = n;
	})();
}));
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/hooks/useValidateProps.js
function en(e, t = []) {
	(0, D.useEffect)(() => {
		Pt("production") || e();
	}, t);
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/accessibility/useInteractiveAttributes.js
var tn = {
	defaultTabIndex: void 0,
	disabledTabIndex: -1
};
function nn(e, t, n, r = tn) {
	let { defaultTabIndex: i, disabledTabIndex: a } = r, { active: o, onClick: s, onFocus: c, onKeyDown: l, onKeyUp: u, onBlur: d, tabIndex: f = i } = t, [p, m] = (0, D.useState)(), [h, g] = (0, D.useState)(!1), _ = (0, D.useRef)(null), v = (0, D.useCallback)((e) => {
		h && g(!1), d?.(e);
	}, [h, d]), y = (0, D.useCallback)((e) => {
		Kt(e) && (e.preventDefault(), e.key !== p && g(!0)), m(e.key), l?.(e);
	}, [p, l]), b = (0, D.useCallback)((e) => {
		Kt(e) && (g(!1), _.current?.click()), m(void 0), u?.(e);
	}, [u, _]);
	return [e && (o || h), {
		onBlur: v,
		onClick: e ? s : void 0,
		onFocus: e ? c : void 0,
		onKeyDown: y,
		onKeyUp: b,
		ref: Xt(_, n),
		tabIndex: e ? f : a
	}];
}
//#endregion
//#region node_modules/tslib/tslib.es6.mjs
var rn, an = o((() => {
	rn = function() {
		return rn = Object.assign || function(e) {
			for (var t, n = 1, r = arguments.length; n < r; n++) for (var i in t = arguments[n], t) Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i]);
			return e;
		}, rn.apply(this, arguments);
	};
}));
//#endregion
//#region node_modules/lower-case/dist.es2015/index.js
function on(e) {
	return e.toLowerCase();
}
var sn = o((() => {}));
//#endregion
//#region node_modules/no-case/dist.es2015/index.js
function cn(e, t) {
	t === void 0 && (t = {});
	for (var n = t.splitRegexp, r = n === void 0 ? un : n, i = t.stripRegexp, a = i === void 0 ? dn : i, o = t.transform, s = o === void 0 ? on : o, c = t.delimiter, l = c === void 0 ? " " : c, u = ln(ln(e, r, "$1\0$2"), a, "\0"), d = 0, f = u.length; u.charAt(d) === "\0";) d++;
	for (; u.charAt(f - 1) === "\0";) f--;
	return u.slice(d, f).split("\0").map(s).join(l);
}
function ln(e, t, n) {
	return t instanceof RegExp ? e.replace(t, n) : t.reduce(function(e, t) {
		return e.replace(t, n);
	}, e);
}
var un, dn, fn = o((() => {
	sn(), un = [/([a-z0-9])([A-Z])/g, /([A-Z])([A-Z][a-z])/g], dn = /[^A-Z0-9]+/gi;
}));
//#endregion
//#region node_modules/pascal-case/dist.es2015/index.js
function pn(e, t) {
	var n = e.charAt(0), r = e.substr(1).toLowerCase();
	return t > 0 && n >= "0" && n <= "9" ? "_" + n + r : "" + n.toUpperCase() + r;
}
function mn(e, t) {
	return t === void 0 && (t = {}), cn(e, rn({
		delimiter: "",
		transform: pn
	}, t));
}
var hn = o((() => {
	an(), fn();
})), gn = o((() => {})), _n = o((() => {})), vn = o((() => {}));
//#endregion
//#region node_modules/dot-case/dist.es2015/index.js
function yn(e, t) {
	return t === void 0 && (t = {}), cn(e, rn({ delimiter: "." }, t));
}
var bn = o((() => {
	an(), fn();
})), xn = o((() => {})), Sn = o((() => {})), Cn = o((() => {})), wn = o((() => {}));
//#endregion
//#region node_modules/snake-case/dist.es2015/index.js
function Tn(e, t) {
	return t === void 0 && (t = {}), yn(e, rn({ delimiter: "_" }, t));
}
var En = o((() => {
	an(), bn();
})), Dn = o((() => {
	gn(), _n(), vn(), bn(), xn(), fn(), Sn(), hn(), Cn(), wn(), En();
})), On, kn = o((() => {
	On = ["M10.99 6.99h-2v-2c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1m-3-7c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.68 6-6 6"];
})), An, jn = o((() => {
	An = ["M13 0a1 1 0 0 0-1 1v1h-1a1 1 0 1 0 0 2h1v1a1 1 0 1 0 2 0V4h1a1 1 0 1 0 0-2h-1V1a1 1 0 0 0-1-1M8.765 1A3 3 0 0 0 8 3c0 .769.29 1.47.765 2H2v8h12V7.827a3 3 0 0 0 1.87-1.957l.001.001.129.425V14c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1zM8.5 10c.28 0 .5.22.5.5s-.22.5-.5.5h-5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5zm-1-2c.28 0 .5.22.5.5s-.22.5-.5.5h-4c-.28 0-.5-.22-.5-.5s.22-.5.5-.5zm2.674-2c.124.35.31.67.547.947A.5.5 0 0 1 10.5 7h-7c-.28 0-.5-.22-.5-.5s.22-.5.5-.5z"];
})), Mn, Nn = o((() => {
	Mn = ["M2 2v6h1v2H.8a.8.8 0 0 1-.8-.8V.8A.8.8 0 0 1 .8 0h14.4a.8.8 0 0 1 .8.8v8.4a.8.8 0 0 1-.8.8H13V8h1V2zm7 9h2c.55 0 1 .45 1 1s-.45 1-1 1H9v2c0 .55-.45 1-1 1s-1-.45-1-1v-2H5c-.55 0-1-.45-1-1s.45-1 1-1h2V9c0-.55.45-1 1-1s1 .45 1 1z"];
})), Pn, Fn = o((() => {
	Pn = ["M12 0a1 1 0 0 0-1 1v2H9a1 1 0 0 0 0 2h2v2a1 1 0 1 0 2 0V5h2a1 1 0 1 0 0-2h-2V1a1 1 0 0 0-1-1M0 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 0 2H2v2a1 1 0 0 1-2 0zm1 12a1 1 0 0 1-1-1v-3a1 1 0 1 1 2 0v2h2.5a1 1 0 1 1 0 2zm11 0a1 1 0 0 0 1-1v-3a1 1 0 1 0-2 0v2H9a1 1 0 1 0 0 2zm-5.5-4a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"];
})), In, Ln = o((() => {
	In = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-5 14H2V2h8zm4 0h-3V2h3zM4 9h1v1c0 .55.45 1 1 1s1-.45 1-1V9h1c.55 0 1-.45 1-1s-.45-1-1-1H7V6c0-.55-.45-1-1-1s-1 .45-1 1v1H4c-.55 0-1 .45-1 1s.45 1 1 1"];
})), Rn, zn = o((() => {
	Rn = ["M8 9h1v1c0 .55.45 1 1 1s1-.45 1-1V9h1c.55 0 1-.45 1-1s-.45-1-1-1h-1V6c0-.55-.45-1-1-1s-1 .45-1 1v1H8c-.55 0-1 .45-1 1s.45 1 1 1m7-9H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M5 14H2V2h3zm9 0H6V2h8z"];
})), Bn, Vn = o((() => {
	Bn = ["M13 0a1 1 0 0 1 1 1v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0V4h-1a1 1 0 1 1 0-2h1V1a1 1 0 0 1 1-1m-3 5.83a3 3 0 0 1-1-.594V7H2V5h6.764A3 3 0 0 1 8 3c0-.768.289-1.47.764-2H.909C.364 1 0 1.5 0 2v12c0 .6.364 1 .91 1H9v1h5a1 1 0 0 0 1-1V7.236A3 3 0 0 1 13 8h-3zM2 13v-2h7v2zm7-3H2V8h7zm4-1v2h-3V9zm-3 3h3v2h-3z"];
})), Hn, Un = o((() => {
	Hn = ["M8 0a1 1 0 1 1 0 2 6 6 0 1 0 6 6 1 1 0 0 1 2 0 8 8 0 1 1-8-8m0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6m5-5a1 1 0 0 1 1 1v.999L15 2a1 1 0 0 1 0 2h-1v1a1 1 0 0 1-2 0V4h-1a1 1 0 0 1 0-2h1V1a1 1 0 0 1 1-1"];
})), Wn, Gn = o((() => {
	Wn = ["M7 5H5c-.55 0-1-.45-1-1s.45-1 1-1h2V1c0-.55.45-1 1-1s1 .45 1 1v2h2c.55 0 1 .45 1 1s-.45 1-1 1H9v2c0 .55-.45 1-1 1s-1-.45-1-1zm7 9V8h-1V6h2.2a.8.8 0 0 1 .8.8v8.4a.8.8 0 0 1-.8.8H.8a.8.8 0 0 1-.8-.8V6.8A.8.8 0 0 1 .8 6H3v2H2v6z"];
})), Kn, qn = o((() => {
	Kn = ["M6 11h1v1c0 .55.45 1 1 1s1-.45 1-1v-1h1c.55 0 1-.45 1-1s-.45-1-1-1H9V8c0-.55-.45-1-1-1s-1 .45-1 1v1H6c-.55 0-1 .45-1 1s.45 1 1 1m9-11H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2V6h12zm0-9H2V2h12z"];
})), Jn, Yn = o((() => {
	Jn = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2v-3h12zm0-4H2V2h12zM6 7h1v1c0 .55.45 1 1 1s1-.45 1-1V7h1c.55 0 1-.45 1-1s-.45-1-1-1H9V4c0-.55-.45-1-1-1s-1 .45-1 1v1H6c-.55 0-1 .45-1 1s.45 1 1 1"];
})), Xn, Zn = o((() => {
	Xn = ["M0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm9 0a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zm3.5 8c.483 0 .875.392.875.875v1.75h1.75a.875.875 0 0 1 0 1.75h-1.75v1.75a.875.875 0 0 1-1.75 0v-1.75h-1.75a.875.875 0 0 1 0-1.75h1.75v-1.75c0-.483.392-.875.875-.875"];
})), Qn, $n = o((() => {
	Qn = ["M14 4.01h-1v-1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1v-1h1c.55 0 1-.45 1-1 0-.56-.45-1-1-1m-13 2h6c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m8 6H1c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1 0-.56-.45-1-1-1m0-4H1c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1 0-.56-.45-1-1-1"];
})), er, tr = o((() => {
	er = ["M.01 7V5H16v7c0 .55-.45 1-1 1H9.005v-2.99C8.974 8.332 7.644 7 5.996 7zM15 2H7.416L5.706.29a1 1 0 0 0-.71-.29H1C.45 0 0 .45 0 1v3h15.99V3c.01-.55-.44-1-.99-1M5.997 9H2c-.55 0-1 .45-1 1s.45 1 1 1h1.589L.3 14.29a1.003 1.003 0 0 0 1.42 1.42l3.287-3.29v1.59c0 .55.45 1 1 1 .549 0 .999-.45.999-1v-4A1.02 1.02 0 0 0 5.996 9"];
})), nr, rr = o((() => {
	nr = ["M2.1 9.101a4 4 0 0 0-1.828.974A8 8 0 0 1 10.075.272 4 4 0 0 0 9.1 2.1a6 6 0 0 0-7 7M14 8a6 6 0 0 0-.1-1.101 4 4 0 0 0 1.828-.974 8 8 0 0 1-9.803 9.803A4 4 0 0 0 6.9 13.9q.535.1 1.1.1a6 6 0 0 0 6-6M8 3a1 1 0 0 0-1 1v2a1 1 0 0 0 2 0V4a1 1 0 0 0-1-1m1 5a1 1 0 0 1 1-1h2a1 1 0 0 1 0 2h-2a1 1 0 0 1-1-1M3 8a1 1 0 0 1 1-1h2a1 1 0 0 1 0 2H4a1 1 0 0 1-1-1m4 2a1 1 0 0 1 2 0v2a1 1 0 0 1-2 0zm-2 3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m8-8a2 2 0 1 0 0-4 2 2 0 0 0 0 4"];
})), ir, ar = o((() => {
	ir = ["M16 1.5A1.498 1.498 0 0 0 13.44.44L9.91 3.97 2 1 1 3l5.93 3.95L3.88 10H1l-1 1 3 2 2 3 1-1v-2.88l3.05-3.05L13 15l2-1-2.97-7.91 3.53-3.53c.27-.27.44-.65.44-1.06"];
})), or, sr = o((() => {
	or = ["M4 4c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1zM1 3h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m13 10H2c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1m1-6H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m-5 5c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1z"];
})), cr, lr = o((() => {
	cr = ["M15 12.98H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m-14-10h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1 0 .56.45 1 1 1m14 4H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m0-3H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m0 6H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), ur, dr = o((() => {
	ur = ["M13 13H1c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1M1 3h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m0 3h8c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 1H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M1 12h4c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), fr, pr = o((() => {
	fr = ["M15 12.98H3c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1m-14-10h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1 0 .56.45 1 1 1m14 1H7c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m0 6h-4c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1m0-3H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), mr, hr = o((() => {
	mr = ["M10 12h3c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1h-3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1m5 2H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M3 12h3c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1"];
})), gr, _r = o((() => {
	gr = ["M15 7h-1V6c0-.55-.45-1-1-1h-3c-.55 0-1 .45-1 1v1H7V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v4H1c-.55 0-1 .45-1 1s.45 1 1 1h1v4c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V9h2v1c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V9h1c.55 0 1-.45 1-1s-.45-1-1-1"];
})), vr, yr = o((() => {
	vr = ["M9 9H5c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1M1 0C.45 0 0 .45 0 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m13 2H5c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), br, xr = o((() => {
	br = ["M11 9H7c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1m4-9c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m-4 2H2c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), Sr, Cr = o((() => {
	Sr = ["M15 0H1C.45 0 0 .45 0 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M6 4H3c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m7 0h-3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1"];
})), wr, Tr = o((() => {
	wr = ["M13 2H9V1c0-.55-.45-1-1-1S7 .45 7 1v1H3c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h4v2H6c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1v-1h1c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1H9V7h4c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), Er, Dr = o((() => {
	Er = ["M2.126 1.1A5 5 0 0 1 4 5v8H0V5c0-1.517.69-2.952 1.874-3.9L2 1zm6 0A5 5 0 0 1 10 5v8H6V5c0-1.517.69-2.952 1.874-3.9L8 1zM16 5c0-1.517-.69-2.952-1.874-3.9L14 1l-.126.1A5 5 0 0 0 12 5v8h4zM4 15v-1H0v1zm6-1v1H6v-1zm6 1v-1h-4v1z"];
})), Or, kr = o((() => {
	Or = ["M10 2a2 2 0 0 1-1 1.732V5h2v2H9v6.874a4 4 0 0 0 2.976-3.436l-.269.27a1 1 0 0 1-1.414-1.415l2-2a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1-1.414 1.414l-.306-.306a6 6 0 0 1-11.974 0l-.306.306A1 1 0 0 1 .293 9.293l2-2a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1-1.414 1.414l-.27-.27A4 4 0 0 0 7 13.875V7H5V5h2V3.732A2 2 0 1 1 10 2"];
})), Ar, jr = o((() => {
	Ar = ["M15.52 2.77c.3-.29.48-.7.48-1.15C16 .73 15.27 0 14.38 0c-.45 0-.85.18-1.15.48l-1.34 1.34 2.3 2.3zM7.4 10.9l6.21-6.21-2.3-2.3L5.1 8.6zM14 14H2V2h6.34l2-2H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V5.66l-2 2zM3 13l3.58-1.29-2.29-2.27z"];
})), Mr, Nr = o((() => {
	Mr = ["M7 5c-.363-.017-4.16-.009-6.005-.003a1 1 0 0 0-.995 1V9a1 1 0 0 0 1 1h2v5.057c0 .53.413.946.943.946h.082a1 1 0 0 0 .996-1.004L5 10h2l3.228 3.924c.596.724 1.772.303 1.772-.636V1.762c0-.936-1.17-1.359-1.768-.64zm8 3c0 1.018-.616 2.046-1.457 2.67-.237.176-.543-.012-.543-.306V5.769c0-.296.31-.484.55-.312C14.384 6.055 15 6.991 15 8"];
})), Pr, Fr = o((() => {
	Pr = ["M2.673 10.758a1.4 1.4 0 0 1 .093.234c.127.442.012.932-.362 1.212-.441.332-1.075.246-1.349-.233a8 8 0 1 1 14.014-.225c-.259.488-.889.594-1.341.277-.382-.269-.513-.755-.4-1.2a1.3 1.3 0 0 1 .085-.238 6 6 0 1 0-10.74.173m2.464-1.862a1.8 1.8 0 0 1 .076.404c.03.415-.096.831-.43 1.078-.444.328-1.08.237-1.314-.264a5 5 0 0 1-.24-.62l-.004-.011a5 5 0 1 1 9.574-.08l-.003.011q-.095.32-.23.625c-.226.504-.861.606-1.31.285-.338-.241-.47-.654-.448-1.07a1.7 1.7 0 0 1 .07-.405 3 3 0 0 0-.216-2.233 3 3 0 0 0-5.525 2.28M8 7a1 1 0 0 1 1 1v3.586l2.707 2.707a1 1 0 0 1-1.414 1.414L8 13.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L7 11.586V8a1 1 0 0 1 1-1"];
})), Ir, Lr = o((() => {
	Ir = ["M15 0a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zM6 4a1 1 0 0 0-1.993-.117L4 4v8a1 1 0 0 0 1.993.117L6 12V9h4v3a1 1 0 0 0 1.993.117L12 12V4a1 1 0 0 0-1.993-.117L10 4v3H6z"];
})), Rr, zr = o((() => {
	Rr = ["M3.5 7h7c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-7c-.28 0-.5.22-.5.5s.22.5.5.5M15 1H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1m-1 12H2V5h12zM3.5 9h4c.28 0 .5-.22.5-.5S7.78 8 7.5 8h-4c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-5c-.28 0-.5.22-.5.5s.22.5.5.5"];
})), Br, Vr = o((() => {
	Br = ["M3.5 11h2c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-2c-.28 0-.5.22-.5.5s.22.5.5.5m0-2h5c.28 0 .5-.22.5-.5S8.78 8 8.5 8h-5c-.28 0-.5.22-.5.5s.22.5.5.5M11 4H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m-1 10H2V7h8zm5-14H5c-.55 0-1 .45-1 1v2h2V2h8v7h-1v2h2c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M3.5 13h3c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-3c-.28 0-.5.22-.5.5s.22.5.5.5"];
})), Hr, Ur = o((() => {
	Hr = ["M13.382 0a1 1 0 0 1 .894.553L16 4v11a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V4L1.724.553A1 1 0 0 1 2.618 0zM8 6c-.55 0-1 .45-1 1v2.59l-.29-.29-.081-.076A.97.97 0 0 0 6 9a1.003 1.003 0 0 0-.71 1.71l2 2 .096.084c.168.13.38.206.614.206.28 0 .53-.11.71-.29l2-2 .084-.096A1.003 1.003 0 0 0 9.29 9.29l-.29.3V7l-.007-.116A1.004 1.004 0 0 0 8 6m5-4H3L2 4h12z"];
})), Wr, Gr = o((() => {
	Wr = ["M4 3.664C4 1.644 5.793 0 8 0s3.993 1.643 4 3.664C12 5.692 8 11 8 11S4 5.693 4 3.664M6 4a2 2 0 1 0 4.001-.001A2 2 0 0 0 6 4m7.504 6.269-2.68-1.609.021-.033c.34-.538.688-1.115 1-1.687l3.67 2.202a1 1 0 0 1 .266 1.483l-4 5A1 1 0 0 1 11 16H5a1 1 0 0 1-.78-.376l-4-5a1 1 0 0 1 .266-1.482l3.67-2.202a31 31 0 0 0 .999 1.687l.021.033-2.68 1.609 2.985 3.73h5.038z"];
})), Kr, qr = o((() => {
	Kr = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm4 7a1 1 0 1 1 0 2 1 1 0 0 1 0-2M5 7a1 1 0 1 1 0 2 1 1 0 0 1 0-2m6 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"];
})), Jr, Yr = o((() => {
	Jr = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm7 6a1 1 0 0 1 .993.883L12 7v2a1 1 0 0 1-.883.993L11 10H5a1 1 0 0 1-.993-.883L4 9V7a1 1 0 0 1 .883-.993L5 6zm0 1H8v2h3z"];
})), Xr, Zr = o((() => {
	Xr = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm6.5 4a.5.5 0 0 1 .5.5V5a1 1 0 0 1 .993.883L12 6v5a1 1 0 0 1-.883.993L11 12H5a1 1 0 0 1-.993-.883L4 11V6a1 1 0 0 1 .883-.993L5 5v-.5a.5.5 0 0 1 1 0V5h4v-.5a.5.5 0 0 1 .5-.5m.5 3H5v4h6z"];
})), Qr, $r = o((() => {
	Qr = ["M15.993.883A1 1 0 0 0 15 0h-3l-.117.007A1 1 0 0 0 11 1l.007.117A1 1 0 0 0 12 2h2v12h-2l-.117.007A1 1 0 0 0 12 16h3l.117-.007A1 1 0 0 0 16 15V1zM5 1a1 1 0 0 0-1-1H1L.883.007A1 1 0 0 0 0 1v14l.007.117A1 1 0 0 0 1 16h3l.117-.007A1 1 0 0 0 5 15l-.007-.117A1 1 0 0 0 4 14H2V2h2l.117-.007A1 1 0 0 0 5 1m-.653 4.86q-.266.046-.547.047v.703h1.344v3.86h.977V5h-.727a.84.84 0 0 1-.203.422 1.2 1.2 0 0 1-.367.281q-.21.11-.477.157m7.115-.59q-.354-.264-.918-.264t-.925.263a1.8 1.8 0 0 0-.557.662q-.195.4-.27.88-.069.481-.068.933 0 .45.067.933.075.481.271.887.203.4.557.662.36.255.925.256.564 0 .918-.256.36-.263.556-.662a2.9 2.9 0 0 0 .271-.887q.075-.482.075-.933 0-.45-.075-.933a2.8 2.8 0 0 0-.27-.88 1.7 1.7 0 0 0-.557-.662m-.452 4.34a.7.7 0 0 1-.466.157.7.7 0 0 1-.474-.158 1.2 1.2 0 0 1-.293-.436 2.8 2.8 0 0 1-.15-.647 6 6 0 0 1-.046-.782q0-.414.045-.775.045-.369.15-.647.114-.277.294-.436a.7.7 0 0 1 .474-.166.68.68 0 0 1 .466.166q.188.157.294.436.113.278.158.647.045.361.045.775t-.045.782q-.045.37-.158.647-.105.27-.294.436m-3.928-.163H8.17V10.5H7.082z"];
})), ei, ti = o((() => {
	ei = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm6.904 5q.384 0 .68.112.296.113.5.312.204.2.312.476t.108.604q0 .344-.152.636a1.3 1.3 0 0 1-.456.492v.016l.08.04q.083.046.168.124.128.116.232.284a1.67 1.67 0 0 1 .24.872q0 .375-.128.68a1.52 1.52 0 0 1-.896.852 2 2 0 0 1-.68.116q-.64 0-1.096-.304a1.36 1.36 0 0 1-.584-.864q-.016-.08.064-.104l.696-.16.033-.002q.045.004.063.058.088.24.288.408t.536.168q.384 0 .592-.228a.83.83 0 0 0 .208-.58q0-.416-.24-.652t-.648-.236h-.232l-.035-.005q-.045-.015-.045-.075v-.632l.005-.035q.015-.045.075-.045h.216l.138-.009a.73.73 0 0 0 .438-.207q.216-.216.216-.576a.75.75 0 0 0-.192-.532q-.192-.204-.536-.204-.304 0-.48.152a.8.8 0 0 0-.248.408q-.024.072-.096.056l-.68-.16-.034-.012q-.042-.024-.03-.084a1.35 1.35 0 0 1 .516-.828q.204-.156.48-.244A2 2 0 0 1 10.904 5m-6.152.088.035.005q.045.015.045.075v5.28l-.005.035q-.015.045-.075.045h-.736l-.035-.005q-.045-.015-.045-.075V6.16H3.92l-.832.584-.032.016Q3 6.779 3 6.696V5.88l.006-.04a.16.16 0 0 1 .05-.072l.872-.632.04-.027a.24.24 0 0 1 .104-.021zM7.344 5q.384 0 .68.12t.5.324.312.48.108.596q0 .367-.136.676-.136.308-.376.596l-1.584 1.92v.016h2.016l.035.005q.045.015.045.075v.64l-.005.035q-.015.045-.075.045H5.808l-.035-.005q-.045-.015-.045-.075v-.6l.004-.04a.13.13 0 0 1 .036-.064l1.92-2.392.1-.133a2 2 0 0 0 .156-.267 1 1 0 0 0 .096-.432.74.74 0 0 0-.188-.512Q7.664 5.8 7.32 5.8q-.329 0-.512.184a.83.83 0 0 0-.224.496q-.015.08-.088.064L5.792 6.4l-.034-.012q-.042-.024-.03-.084a1.43 1.43 0 0 1 .94-1.192A1.9 1.9 0 0 1 7.344 5"];
})), ni, ri = o((() => {
	ni = ["M4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm11 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM6.5 3c-.646 0-1.151.205-1.416.725-.117.23-.16.477-.176.692a5 5 0 0 0-.001.622c.017.421.028 1.808-.04 2.024a.5.5 0 0 1-.126.214.8.8 0 0 1-.362.184C4.156 7.523 4 7.745 4 8s.156.477.379.539a.8.8 0 0 1 .362.184.5.5 0 0 1 .126.214c.068.216.057 1.603.04 2.024a5 5 0 0 0 0 .622c.017.215.06.461.177.692.265.52.77.725 1.416.725.276 0 .5-.249.5-.556 0-.306-.224-.555-.5-.555-.467 0-.533-.135-.544-.159l-.001-.001a.7.7 0 0 1-.051-.24 4 4 0 0 1 .005-.558c.015-.34.036-1.93-.097-2.358A1.6 1.6 0 0 0 5.505 8c.146-.174.244-.371.307-.573.133-.427.112-2.017.097-2.358l-.003-.08a4 4 0 0 1-.002-.478.7.7 0 0 1 .05-.24l.002-.001c.011-.024.077-.159.544-.159.276 0 .5-.249.5-.555S6.776 3 6.5 3m3 0c.646 0 1.152.205 1.416.725.117.23.16.477.176.692.017.213.009.434.001.622-.017.421-.027 1.808.04 2.024.027.09.067.157.126.214.063.06.17.13.362.184.223.062.379.284.379.539s-.156.477-.379.539a.8.8 0 0 0-.362.184.5.5 0 0 0-.126.214c-.067.216-.057 1.603-.04 2.024.008.188.016.409 0 .622-.017.215-.06.461-.177.692-.264.52-.77.725-1.416.725-.276 0-.5-.249-.5-.556 0-.306.224-.555.5-.555.467 0 .533-.135.544-.159l.001-.001a.7.7 0 0 0 .051-.24c.01-.132.006-.284-.002-.478l-.003-.08c-.015-.34-.036-1.93.097-2.358A1.6 1.6 0 0 1 10.495 8a1.6 1.6 0 0 1-.307-.573c-.133-.427-.112-2.017-.097-2.358l.003-.08c.008-.194.012-.346.002-.478a.7.7 0 0 0-.05-.24l-.002-.001c-.011-.024-.077-.159-.544-.159-.276 0-.5-.249-.5-.555S9.224 3 9.5 3"];
})), ii, ai = o((() => {
	ii = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm1.61 5q.771 0 1.343.637.573.637.573 1.716 0 1.257-.773 2.252-.772.995-2.437 1.609v-.465l.233-.095a3.1 3.1 0 0 0 1.274-1.017q.55-.757.55-1.577a.5.5 0 0 0-.057-.26q-.027-.056-.074-.056-.046 0-.149.075-.297.214-.744.214-.54 0-.944-.433A1.45 1.45 0 0 1 4 6.572q0-.633.465-1.102Q4.931 5 5.61 5m4.474 0q.772 0 1.344.637T12 7.353q0 1.257-.772 2.252T8.79 11.214v-.465l.233-.095a3.1 3.1 0 0 0 1.274-1.017q.549-.757.549-1.577a.5.5 0 0 0-.056-.26q-.029-.056-.075-.056-.045 0-.149.075-.297.214-.744.214-.54 0-.944-.433a1.45 1.45 0 0 1-.405-1.028q0-.633.466-1.102T10.084 5"];
})), oi, si = o((() => {
	oi = ["M15 0a1 1 0 0 1 .993.883L16 1v14a1 1 0 0 1-.883.993L15 16h-3a1 1 0 0 1-.117-1.993L12 14h2V2h-2a1 1 0 0 1-.993-.883L11 1a1 1 0 0 1 .883-.993L12 0zM4 0a1 1 0 0 1 .117 1.993L4 2H2v12h2a1 1 0 0 1 .993.883L5 15a1 1 0 0 1-.883.993L4 16H1a1 1 0 0 1-.993-.883L0 15V1A1 1 0 0 1 .883.007L1 0zm4 3a5 5 0 1 1 0 10A5 5 0 0 1 8 3m0 1a4 4 0 1 0 0 8 4 4 0 0 0 0-8m2.354 1.646a.5.5 0 0 1 .057.638l-.057.07-2 2a.5.5 0 0 1-.638.057l-.07-.057-1-1a.5.5 0 0 1 .638-.765l.07.057.646.647 1.646-1.647a.5.5 0 0 1 .708 0"];
})), ci, li = o((() => {
	ci = ["M14 3a1.003 1.003 0 0 0-1.71-.71L4 10.59V6c0-.55-.45-1-1-1s-1 .45-1 1v7c0 .55.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1H5.41l8.29-8.29c.19-.18.3-.43.3-.71"];
})), ui, di = o((() => {
	ui = ["M13 5c-.55 0-1 .45-1 1v4.59l-8.29-8.3a1.003 1.003 0 0 0-1.42 1.42l8.3 8.29H6c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1"];
})), fi, pi = o((() => {
	fi = ["M13 8c-.3 0-.5.1-.7.3L9 11.6V2c0-.5-.4-1-1-1s-1 .5-1 1v9.6L3.7 8.3C3.5 8.1 3.3 8 3 8c-.5 0-1 .5-1 1 0 .3.1.5.3.7l5 5c.2.2.4.3.7.3s.5-.1.7-.3l5-5c.2-.2.3-.4.3-.7 0-.6-.4-1-1-1"];
})), mi, hi = o((() => {
	mi = ["M13.99 6.99H4.41L7.7 3.7a1.003 1.003 0 0 0-1.42-1.42l-5 5a1.014 1.014 0 0 0 0 1.42l5 5a1.003 1.003 0 0 0 1.42-1.42L4.41 8.99H14c.55 0 1-.45 1-1s-.46-1-1.01-1"];
})), gi, _i = o((() => {
	gi = ["m14.7 7.29-5-5a.97.97 0 0 0-.71-.3 1.003 1.003 0 0 0-.71 1.71l3.29 3.29H1.99c-.55 0-1 .45-1 1s.45 1 1 1h9.59l-3.29 3.29a1.003 1.003 0 0 0 1.42 1.42l5-5c.18-.18.29-.43.29-.71s-.12-.52-.3-.7"];
})), A, vi = o((() => {
	A = ["M13.71 12.29 5.41 4H10c.55 0 1-.45 1-1s-.45-1-1-1H3c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1s1-.45 1-1V5.41l8.29 8.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), yi, bi = o((() => {
	yi = ["M13 2H6c-.55 0-1 .45-1 1s.45 1 1 1h4.59L2.3 12.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L12 5.41V10c0 .55.45 1 1 1s1-.45 1-1V3c0-.55-.45-1-1-1"];
})), xi, Si = o((() => {
	xi = ["m13.7 6.3-5-5C8.5 1.1 8.3 1 8 1s-.5.1-.7.3l-5 5c-.2.2-.3.4-.3.7 0 .6.5 1 1 1 .3 0 .5-.1.7-.3L7 4.4V14c0 .6.4 1 1 1s1-.4 1-1V4.4l3.3 3.3c.2.2.4.3.7.3.6 0 1-.4 1-1 0-.3-.1-.5-.3-.7"];
})), Ci, wi = o((() => {
	Ci = ["M3.396.146a.5.5 0 0 1 .708 0l3.182 3.182a.5.5 0 1 1-.708.708L4.246 1.704v.002c-.008 1.795-.014 3.149.184 4.315.233 1.367.747 2.455 1.923 3.625 1.182 1.176 2.216 1.686 3.546 1.919 1.149.201 2.507.196 4.39.188h.007l-2.331-2.331a.5.5 0 1 1 .707-.708l3.182 3.182a.5.5 0 0 1 0 .708l-3.182 3.182a.5.5 0 1 1-.708-.708l2.325-2.324c-1.866.008-3.325.013-4.563-.204-1.545-.27-2.761-.885-4.079-2.196C4.323 9.038 3.712 7.76 3.445 6.19c-.213-1.25-.208-2.7-.199-4.478L.922 4.036a.5.5 0 1 1-.708-.708z"];
})), Ti, Ei = o((() => {
	Ti = ["m15.7 7.3-4-4c-.2-.2-.4-.3-.7-.3-.6 0-1 .5-1 1 0 .3.1.5.3.7L12.6 7H3.4l2.3-2.3c.2-.2.3-.4.3-.7 0-.5-.4-1-1-1-.3 0-.5.1-.7.3l-4 4c-.2.2-.3.4-.3.7s.1.5.3.7l4 4c.2.2.4.3.7.3.6 0 1-.4 1-1 0-.3-.1-.5-.3-.7L3.4 9h9.2l-2.3 2.3c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3l4-4c.2-.2.3-.4.3-.7s-.1-.5-.3-.7"];
})), Di, Oi = o((() => {
	Di = ["M12 10c-.3 0-.5.1-.7.3L9 12.6V3.4l2.3 2.3c.2.2.4.3.7.3.6 0 1-.4 1-1 0-.3-.1-.5-.3-.7l-4-4C8.5.1 8.3 0 8 0s-.5.1-.7.3l-4 4c-.2.2-.3.4-.3.7 0 .6.5 1 1 1 .3 0 .5-.1.7-.3L7 3.4v9.2l-2.3-2.3c-.2-.2-.4-.3-.7-.3-.5 0-1 .4-1 1 0 .3.1.5.3.7l4 4c.2.2.4.3.7.3s.5-.1.7-.3l4-4c.2-.2.3-.4.3-.7 0-.6-.4-1-1-1"];
})), ki, Ai = o((() => {
	ki = ["m14.54 11.18.01-.02L9.8 8l4.75-3.17-.01-.02c.27-.17.46-.46.46-.81 0-.55-.45-1-1-1-.21 0-.39.08-.54.18l-.01-.02L9 6.13V1c0-.55-.45-1-1-1S7 .45 7 1v5.13L2.55 3.17l-.01.01A.97.97 0 0 0 2 3c-.55 0-1 .45-1 1 0 .35.19.64.46.82l-.01.01L6.2 8l-4.75 3.17.01.02c-.27.17-.46.46-.46.81 0 .55.45 1 1 1 .21 0 .39-.08.54-.18l.01.02L7 9.87V15c0 .55.45 1 1 1s1-.45 1-1V9.87l4.45 2.96.01-.02c.15.11.33.19.54.19.55 0 1-.45 1-1 0-.35-.19-.64-.46-.82"];
})), ji, Mi = o((() => {
	ji = ["M5.816 8.371q-.001 2.273 1.814 2.274 1.91 0 2.089-2.86l.12-2.331a5.3 5.3 0 0 0-1.337-.165q-1.272 0-1.979.828-.707.83-.707 2.254M16 7.133q0 1.395-.446 2.55-.445 1.156-1.253 1.802a2.9 2.9 0 0 1-1.868.642q-.783 0-1.356-.41a2 2 0 0 1-.773-1.111h-.12q-.485.76-1.198 1.14a3.35 3.35 0 0 1-1.605.38q-1.615 0-2.541-1.023-.927-1.024-.926-2.77 0-2.01 1.229-3.264Q6.37 3.816 8.44 3.816q.753 0 1.669.13.916.132 1.63.367l-.218 4.536v.234q0 1.561 1.031 1.562.782 0 1.241-.996.462-.995.463-2.537 0-1.669-.695-2.931a4.76 4.76 0 0 0-1.97-1.947q-1.277-.683-2.934-.682-2.107 0-3.67.858a5.74 5.74 0 0 0-2.382 2.455q-.823 1.593-.822 3.7 0 2.832 1.535 4.353t4.409 1.52q2.19.002 4.567-.877v1.6q-2.08.84-4.527.839-3.668-.001-5.717-1.945Q.001 12.108 0 8.625q0-2.547 1.11-4.532a7.56 7.56 0 0 1 3.076-3.038Q6.153 0 8.64 0q2.15.001 3.827.878a6.3 6.3 0 0 1 2.607 2.504q.927 1.623.926 3.75"];
})), Ni, Pi = o((() => {
	Ni = ["M8 14c-3.31 0-6-2.69-6-6 0-1.77.78-3.36 2-4.46V5c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1s.45 1 1 1h1.74A7.95 7.95 0 0 0 0 8c0 4.42 3.58 8 8 8 .55 0 1-.45 1-1s-.45-1-1-1M8 2a5.9 5.9 0 0 1 2.95.81l1.47-1.47A7.9 7.9 0 0 0 8 0c-.55 0-1 .45-1 1s.45 1 1 1m2.71 6.71 5-5a1.003 1.003 0 0 0-1.42-1.42L10 6.59l-1.29-1.3a1.003 1.003 0 0 0-1.42 1.42l2 2c.18.18.43.29.71.29s.53-.11.71-.29M16 8c0-.55-.06-1.08-.16-1.6l-1.87 1.87A5.97 5.97 0 0 1 12 12.45V11c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1h-1.74A7.95 7.95 0 0 0 16 8"];
})), Fi, Ii = o((() => {
	Fi = ["M13.5 2a.5.5 0 0 1 .5.5V3h1v4a1 1 0 1 1 0 2v4h-1v.5a.5.5 0 0 1-1 0V10l-1.79-.895A1 1 0 0 0 10.765 9H10a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1h-.764c-.155 0-.308.036-.447.105L3 10v3.5a.5.5 0 0 1-1 0V13H1V9a1 1 0 0 1 0-2V3h1v-.5a.5.5 0 0 1 1 0V6l1.79.895A1 1 0 0 0 5.236 7H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h.764a1 1 0 0 0 .447-.105L13 6V2.5a.5.5 0 0 1 .5-.5"];
})), Li, Ri = o((() => {
	Li = ["M14 10a1 1 0 1 1 0 2h-.585l2.292 2.293a1 1 0 0 1-1.32 1.497l-.094-.083L12 13.415V14a1 1 0 1 1-2 0l.003-3.075.012-.1.012-.059.033-.108.034-.081.052-.098.067-.096.08-.09a1 1 0 0 1 .112-.097l.11-.071.143-.065.076-.024.091-.02.116-.014zM6.036 6.136l-3.45 3.45-.117.127a2 2 0 0 0 2.818 2.818l.127-.117 3.45-3.449a4 4 0 0 1-.885 3.704l-.15.16-1 1A4 4 0 0 1 1.02 8.33l.15-.16 1-1a4 4 0 0 1 3.865-1.035m4.671-1.843a1 1 0 0 1 .083 1.32l-.083.094-5 5a1 1 0 0 1-1.497-1.32l.083-.094 5-5a1 1 0 0 1 1.414 0m3.121-3.121a4 4 0 0 1 .151 5.497l-.15.16-1 1a4 4 0 0 1-3.864 1.036l3.45-3.45.116-.128a2 2 0 0 0-2.818-2.818l-.127.117-3.45 3.45A4 4 0 0 1 7.02 2.33l.15-.16 1-1a4 4 0 0 1 5.657 0"];
})), zi, Bi = o((() => {
	zi = ["M8.002 16a6.8 6.8 0 0 1-2.732-.556 7.1 7.1 0 0 1-2.221-1.509 7.1 7.1 0 0 1-1.498-2.239A6.9 6.9 0 0 1 1 8.955q0-.41.285-.698a.94.94 0 0 1 .692-.287q.407 0 .692.287t.285.698q0 2.12 1.469 3.598Q5.89 14.031 8 14.031t3.577-1.48q1.47-1.482 1.47-3.607 0-2.12-1.477-3.598-1.476-1.478-3.58-1.478h-.121l.49.496q.242.244.239.577a.82.82 0 0 1-.238.578.8.8 0 0 1-.588.248.78.78 0 0 1-.588-.24l-1.93-1.945a.97.97 0 0 1-.294-.7q0-.401.294-.697L7.184.24A.78.78 0 0 1 7.772 0q.345.004.588.259a.8.8 0 0 1 .233.583q-.001.339-.244.583l-.47.474h.11q1.459 0 2.732.556 1.274.555 2.225 1.51a7.1 7.1 0 0 1 1.503 2.233A6.9 6.9 0 0 1 15 8.945q0 1.466-.551 2.751a7.1 7.1 0 0 1-1.498 2.239 7.1 7.1 0 0 1-2.219 1.51 6.75 6.75 0 0 1-2.73.555M9 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1m1 1H9v3h1zm-5-.5a.5.5 0 0 1 .5-.5H6a1 1 0 0 1 1 1v3.5a.5.5 0 0 1-1 0V8h-.5a.5.5 0 0 1-.5-.5"];
})), Vi, Hi = o((() => {
	Vi = ["M13.36 4.59c-.15-1.13.5-2.01 1.1-2.87L13.43.53c-1.72.88-4.12.65-5.63-.53-1.51 1.18-3.91 1.41-5.63.52l-1.03 1.2c.61.86 1.25 1.74 1.1 2.87-.3 2.29-2.45 4.17-1.32 6.68.45 1.14 1.44 1.9 2.72 2.2 1.56.36 3.52.72 4.16 2.53.64-1.81 2.6-2.16 4.16-2.54 1.28-.3 2.27-1.06 2.72-2.2 1.12-2.5-1.03-4.38-1.32-6.67"];
})), Ui, Wi = o((() => {
	Ui = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m3 9H5c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1s-.45 1-1 1"];
})), Gi, Ki = o((() => {
	Gi = ["m15.36 6.46-.62-.14c-.31-1.12-.98-2.15-1.87-2.99l.4-1.77a.438.438 0 0 0-.49-.56c-.85.09-1.6.42-2.14.98-.84-.32-1.87-.51-2.85-.51-2.49 0-4.63 1.17-5.92 2.89-.18-.04-.36-.09-.53-.09-.76 0-1.34.61-1.34 1.4 0 .56.31 1.03.76 1.26-.05.33-.09.7-.09 1.07 0 1.68.71 3.17 1.83 4.34l-.27 1.59c-.09.56.35 1.07.89 1.07h.58c.45 0 .8-.33.89-.79l.04-.37c.94.42 2 .7 3.16.7 1.11 0 2.23-.23 3.16-.7l.05.37c.09.47.45.79.89.79h.58c.53 0 .98-.51.89-1.07l-.27-1.54c.62-.61 1.07-1.35 1.38-2.15l.8-.19c.4-.09.71-.47.71-.93V7.4c.09-.47-.22-.84-.62-.94M12 8c-.6 0-1-.7-1-1.5S11.4 5 12 5s1 .7 1 1.5S12.6 8 12 8M6.21 4.92c-.41.2-.91.04-1.12-.36s-.04-.88.37-1.07c1.35-.65 2.73-.65 4.08 0 .41.2.58.68.37 1.07-.21.4-.71.56-1.12.36-.87-.43-1.71-.43-2.58 0"];
})), qi, Ji = o((() => {
	qi = ["M0 14h2V2H0zm6 0h1V2H6zm2 0h1V2H8zm-5 0h2V2H3zM15 2v12h1V2zm-5 12h1V2h-1zm2 0h2V2h-2z"];
})), Yi, Xi = o((() => {
	Yi = ["M7.004 4.385Q6.487 4 5.662 4t-1.353.385q-.517.373-.814.967-.286.582-.396 1.285A10 10 0 0 0 3 8q0 .66.099 1.363.11.703.396 1.296.297.583.814.967.528.375 1.353.374.825 0 1.342-.374.528-.384.814-.967.297-.593.396-1.296.11-.704.11-1.363 0-.66-.11-1.363a4 4 0 0 0-.396-1.285 2.5 2.5 0 0 0-.814-.967m-.66 6.34q-.274.231-.682.231-.418 0-.693-.23a1.8 1.8 0 0 1-.429-.638 4 4 0 0 1-.22-.945A9 9 0 0 1 4.254 8q0-.604.066-1.132.066-.539.22-.945.165-.406.429-.637.274-.242.693-.242.407 0 .682.242.274.23.429.637.165.407.231.945.066.529.066 1.132 0 .605-.066 1.143a3.7 3.7 0 0 1-.231.945 1.6 1.6 0 0 1-.429.637m4.457-5.468q-.39.069-.801.069v1.028h1.968V12h1.43V4h-1.064q-.069.366-.298.617a1.7 1.7 0 0 1-.537.412 2.4 2.4 0 0 1-.698.228"];
})), Zi, Qi = o((() => {
	Zi = [];
})), $i, ea = o((() => {
	$i = ["M3 2h10a1 1 0 0 1 1 1v4h1a1 1 0 1 1 0 2h-1v4a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V9H1a1 1 0 1 1 0-2h1V3a1 1 0 0 1 1-1m5.854 3.146a.5.5 0 1 0-.708.708L10.293 8l-2.147 2.146a.5.5 0 0 0 .708.708l2.5-2.5a.5.5 0 0 0 0-.708zm-4.208 0a.5.5 0 0 0 0 .708L6.793 8l-2.147 2.146a.5.5 0 0 0 .708.708l2.5-2.5a.5.5 0 0 0 .144-.306.5.5 0 0 0-.001-.106.5.5 0 0 0-.143-.296l-2.5-2.5a.5.5 0 0 0-.708 0"];
})), ta, na = o((() => {
	ta = ["M9.39 12.69c-1.2-.53-1.04-.85-1.08-1.29-.01-.07-.01-.13-.02-.2.41-.37.75-.87.97-1.44 0 0 .01-.03.01-.04.05-.13.09-.26.13-.39.27-.06.43-.36.5-.63.01-.03.03-.08.05-.12C8.18 7.8 6.94 6.04 6.94 4c0-.32.04-.62.09-.92-.17-.03-.35-.08-.51-.08-.65 0-1.37.2-1.88.59-.5.38-.87.92-1.05 1.51-.04.14-.07.27-.09.41-.09.48-.14 1.23-.14 1.74v.06c-.19.08-.36.27-.4.68-.03.31.1.59.16.7.06.28.23.59.51.64.04.14.08.27.13.39 0 .01.01.02.01.02v.01c.22.59.57 1.1.99 1.46 0 .06-.01.12-.01.17-.04.44.08.76-1.12 1.29S.62 13.77.25 14.62C-.12 15.5.03 16 .03 16h12.96s.15-.5-.22-1.36c-.37-.85-2.18-1.42-3.38-1.95M11.97 0C9.75 0 7.94 1.79 7.94 4s1.8 4 4.03 4S16 6.21 16 4s-1.8-4-4.03-4M9.96 4c0-1.1.9-2 2.01-2 .37 0 .72.11 1.02.28l-2.75 2.73c-.17-.3-.28-.64-.28-1.01m2.01 2c-.37 0-.72-.11-1.02-.28l2.75-2.73c.18.3.28.64.28 1.01.01 1.1-.9 2-2.01 2"];
})), j, M = o((() => {
	j = ["M11.7 7c.2-.4.3-1 .3-1.5V5c0-.1 0-.2-.1-.3v-.1C11.4 3.1 10.1 2 8.5 2H4c-.5 0-1 .4-1 1v10c0 .5.4 1 1 1h5c2.2 0 4-1.8 4-4 0-1.2-.5-2.3-1.3-3M6 5h2c.6 0 1 .4 1 1s-.4 1-1 1H6zm3 6H6V9h3c.6 0 1 .4 1 1s-.4 1-1 1"];
})), ra, N = o((() => {
	ra = ["M2 1v14c0 .55.45 1 1 1h1V0H3c-.55 0-1 .45-1 1m11-1h-1v7l-2-2-2 2V0H5v16h8c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), ia, aa = o((() => {
	ia = ["M11.2.01h-.15C11.03.01 11.02 0 11 0H5c-.02 0-.03.01-.05.01H4.8c-.44 0-.8.37-.8.82v14.75c0 .45.25.56.57.24l2.87-2.94c.31-.32.82-.32 1.13 0l2.87 2.94c.31.32.57.21.57-.24V.83C12 .38 11.64.01 11.2.01"];
})), oa, sa = o((() => {
	oa = ["M6 10h4c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1m9.93-4.37v-.02L13.94.63C13.78.26 13.42 0 13 0H3c-.42 0-.78.26-.93.63L.08 5.61l-.01.02C.03 5.74 0 5.87 0 6v9c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V6c0-.13-.03-.26-.07-.37M9 2h3.32l1.2 3H9zM3.68 2H7v3H2.48zM14 14H2V7h12z"];
})), ca, la = o((() => {
	ca = ["M11 1C9.34 1 8 2.34 8 4c0 1.25.76 2.32 1.85 2.77A2.02 2.02 0 0 1 8 8H6c-.73 0-1.41.2-2 .55V5.82C5.16 5.4 6 4.3 6 3c0-1.66-1.34-3-3-3S0 1.34 0 3c0 1.3.84 2.4 2 2.82v4.37c-1.16.4-2 1.51-2 2.81 0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.04-.53-1.95-1.32-2.49.35-.31.81-.51 1.32-.51h2c1.92 0 3.52-1.35 3.91-3.15A2.996 2.996 0 0 0 11 1M3 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 12c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m8-9c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m2.5 8a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 1 .5-.5H9v-1c0-.636.244-1.15.637-1.499a2.05 2.05 0 0 1 1.363-.5c.481 0 .98.159 1.363.5.393.35.637.864.637 1.5v1zM12 13v-1c0-.364-.132-.6-.3-.75A1.06 1.06 0 0 0 11 11c-.268 0-.52.09-.7.25-.168.15-.3.386-.3.75v1z"];
})), ua, da = o((() => {
	ua = ["M11 1C9.34 1 8 2.34 8 4c0 1.25.76 2.32 1.85 2.77A2.02 2.02 0 0 1 8 8H6c-.73 0-1.41.2-2 .55V5.82C5.16 5.4 6 4.3 6 3c0-1.66-1.34-3-3-3S0 1.34 0 3c0 1.3.84 2.4 2 2.82v4.37c-1.16.4-2 1.51-2 2.81 0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.04-.53-1.95-1.32-2.49.35-.31.81-.51 1.32-.51h2c1.92 0 3.52-1.35 3.91-3.15A2.996 2.996 0 0 0 11 1M3 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 12c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m8-9c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m2.5 8a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 1 .5-.5H12v-1c0-.636.243-1.15.637-1.499A2.05 2.05 0 0 1 14 10c.481 0 .98.16 1.363.501.394.35.637.863.637 1.499a.5.5 0 0 1-1 0c0-.364-.132-.6-.3-.751A1.06 1.06 0 0 0 14 11c-.268 0-.52.09-.7.249-.168.15-.3.387-.3.751v1z"];
})), fa, pa = o((() => {
	fa = ["M15 3.98h-3v-2c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v2H1c-.55 0-1 .45-1 1v4h3v-1h2v1h6v-1h2v1h3v-4c0-.55-.45-1-1-1m-5 0H6v-1h4zm3 7h-2v-1H5v1H3v-1H0v4c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-4h-3z"];
})), ma, ha = o((() => {
	ma = ["M14 14a1 1 0 0 1 0 2H2a1 1 0 0 1 0-2zM7.995 3.005c.55 0 1 .45 1 .999v5.584l1.29-1.288a1.002 1.002 0 0 1 1.42 1.419l-3 2.996a1.015 1.015 0 0 1-1.42 0l-3-2.997A1.002 1.002 0 0 1 5.705 8.3l1.29 1.29V4.013c0-.55.45-1.009 1-1.009M14 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2m-3 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M8 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M5 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M2 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"];
})), ga, _a = o((() => {
	ga = ["M8.697.29a1 1 0 0 0-.7-.29c-.27 0-.53.11-.71.29L4.29 3.28A1.003 1.003 0 0 0 5.71 4.7l1.288-1.29L7 7H1a1 1 0 0 0 0 2h6v2H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H9V9h6a1 1 0 1 0 0-2H9V3.414h-.003V3.41l1.29 1.29c.179.18.429.29.699.29a1.003 1.003 0 0 0 .71-1.71z"];
})), va, ya = o((() => {
	va = ["M7.2 1.428A4 4 0 0 0 5 5v2H4a1 1 0 0 0 0 2h1v1.5c0 1.133-.229 1.79-.457 2.133-.21.315-.413.367-.543.367H3v2h10v-2H6.591c.27-.684.409-1.522.409-2.5V9h3a1 1 0 1 0 0-2H7V5a2 2 0 0 1 3.732-1l1.732-1a4 4 0 0 0-4.666-1.815"];
})), ba, xa = o((() => {
	ba = ["M5 3a3 3 0 0 1 6 0 5 5 0 0 1 1.425 1.67L13 4.382V3a1 1 0 1 1 2 0v2a1 1 0 0 1-.553.894l-1.46.731q.012.186.013.375v1h2a1 1 0 1 1 0 2h-2a5 5 0 0 1-.21 1.439l1.581.633A1 1 0 0 1 15 13v2a1 1 0 1 1-2 0v-1.323l-1.167-.467A4.99 4.99 0 0 1 8 15a4.99 4.99 0 0 1-3.833-1.79L3 13.677V15a1 1 0 1 1-2 0v-2a1 1 0 0 1 .629-.928l1.581-.633A5 5 0 0 1 3 10H1a1 1 0 1 1 0-2h2V7q0-.189.014-.375l-1.461-.73A1 1 0 0 1 1 5V3a1 1 0 0 1 2 0v1.382l.575.288A5 5 0 0 1 5 3m0 6v1a3 3 0 1 0 6 0V7a3 3 0 0 0-6 0z"];
})), Sa, Ca = o((() => {
	Sa = ["m13.929.629 1.763 4.41A.5.5 0 0 1 16 5.5v4a.5.5 0 0 1-.5.5h-3a1.5 1.5 0 0 0-1.2.6l-.9 1.2a.5.5 0 0 1-.4.2H6.5a.5.5 0 0 1-.312-.11l-1.952-1.56a1.5 1.5 0 0 0-.938-.33H.5a.5.5 0 0 1-.5-.5v-3a.5.5 0 0 1 .431-.495l2.711-4.52a1 1 0 0 1 .748-.479l9-1a1 1 0 0 1 1.038.623M12.36 2.094l-.006-.016-3.166.352 1.121 3.083zm.467 1.166-1.649 2.748 2.51-.594zM9.603 6.496 8.166 2.543l-3.563.396L2.766 6H3.5a.5.5 0 0 1 .367.16L6.218 8.7h1.914l1.452-2.177zM2.5 16a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m11 0a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5"];
})), wa, Ta = o((() => {
	wa = ["M15.39 12.41 7.7 6l1.07-1.1c.34-.34-.12-.63.12-1.26.88-2.17 3.41-2.35 3.41-2.35s.36-.37.71-.72C9.74-.81 7.53.53 6.54 1.4L3.12 4.9l-.71.72c-.39.4-.39 1.05 0 1.45l-.7.72c-.39-.4-1.02-.4-1.41 0s-.39 1.05 0 1.45l1.41 1.45c.39.4 1.02.4 1.41 0s.39-1.05 0-1.45l.71-.72c.39.4 1.02.4 1.41 0l.8-.82 6.39 7.67c.82.82 2.14.82 2.96 0 .81-.82.81-2.15 0-2.96"];
})), Ea, Da = o((() => {
	Ea = ["M15.76 1.35a1 1 0 0 1-.11 1.41l-7 6a1 1 0 1 1-1.3-1.52l7-6a1 1 0 0 1 1.41.11M8 14a6 6 0 0 0 5.598-8.164l1.586-1.36A8 8 0 1 1 12.58 1.44L10.994 2.8A6 6 0 1 0 8 14m1.33-9.774a4 4 0 1 0 2.603 3.037l-2.624 2.25q-.09.077-.19.144a2 2 0 0 1-1.924.174 2 2 0 0 1-.803-.642 1.99 1.99 0 0 1-.212-2.02c.123-.27.305-.508.53-.697z"];
})), Oa, ka = o((() => {
	Oa = ["M13 0H3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M6 14H4v-2h2zm0-3H4V9h2zm0-3H4V6h2zm3 6H7v-2h2zm0-3H7V9h2zm0-3H7V6h2zm3 6h-2V9h2zm0-6h-2V6h2zm0-3H4V2h8z"];
})), Aa, ja = o((() => {
	Aa = ["M11 3c.6 0 1-.5 1-1V1c0-.6-.4-1-1-1s-1 .4-1 1v1c0 .5.4 1 1 1m3-2h-1v1c0 1.1-.9 2-2 2s-2-.9-2-2V1H6v1c0 1.1-.9 2-2 2s-2-.9-2-2V1H1c-.6 0-1 .5-1 1v12c0 .6.4 1 1 1h13c.6 0 1-.4 1-1V2c0-.6-.5-1-1-1M5 13H2v-3h3zm0-4H2V6h3zm4 4H6v-3h3zm0-4H6V6h3zm4 4h-3v-3h3zm0-4h-3V6h3zM4 3c.6 0 1-.5 1-1V1c0-.6-.4-1-1-1S3 .4 3 1v1c0 .5.4 1 1 1"];
})), Ma, Na = o((() => {
	Ma = ["M15 3h-2.59L10.7 1.29A.96.96 0 0 0 10 1H6c-.28 0-.53.11-.71.29L3.59 3H1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h2.56c1.1 1.22 2.67 2 4.44 2s3.34-.78 4.44-2H15c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1M3 6H1V5h2zm5 6c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4m0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), P, Pa = o((() => {
	P = ["M12 6.5c0-.28-.22-.5-.5-.5h-7a.495.495 0 0 0-.37.83l3.5 4c.09.1.22.17.37.17s.28-.07.37-.17l3.5-4c.08-.09.13-.2.13-.33"];
})), Fa, Ia = o((() => {
	Fa = ["M9.5 4c-.13 0-.24.05-.33.13l-4 3.5c-.1.09-.17.22-.17.37s.07.28.17.37l4 3.5a.495.495 0 0 0 .83-.37v-7c0-.28-.22-.5-.5-.5"];
})), La, Ra = o((() => {
	La = ["M11 8c0-.15-.07-.28-.17-.37l-4-3.5A.495.495 0 0 0 6 4.5v7a.495.495 0 0 0 .83.37l4-3.5c.1-.09.17-.22.17-.37"];
})), za, Ba = o((() => {
	za = ["M11.87 9.17s.01 0 0 0l-3.5-4C8.28 5.07 8.15 5 8 5s-.28.07-.37.17l-3.5 4a.495.495 0 0 0 .37.83h7a.495.495 0 0 0 .37-.83"];
})), Va, Ha = o((() => {
	Va = ["M10 1h3a1 1 0 0 1 1 1v2h-4zM2.25 4a.25.25 0 0 0-.25.25V9H.883a.5.5 0 0 0-.429.757l1.072 1.787c.207.344.477.638.791.87A10 10 0 0 1 1 12.5a.5.5 0 0 0 0 1c2.067 0 3.414-.543 4.161-.917.55.373 1.505.917 2.839.917 1.32 0 2.27-.533 2.822-.905l.004.002c.196.105.48.24.856.374.75.268 1.857.529 3.318.529a.5.5 0 0 0 0-1q-.488 0-.916-.039c.47-.328.848-.79 1.07-1.347l.572-1.428A.5.5 0 0 0 15.26 9H4V4.25A.25.25 0 0 0 3.75 4zm2.714 9.56a.5.5 0 0 1 .527.033c.455.325 1.277.907 2.509.907s2.054-.582 2.51-.907a.5.5 0 0 1 .579-.001l.006.004.036.023q.051.034.168.097c.154.082.394.197.72.313.649.232 1.642.471 2.981.471a.5.5 0 0 1 0 1c-1.46 0-2.568-.261-3.318-.53a6 6 0 0 1-.856-.373l-.004-.002c-.552.372-1.502.905-2.822.905-1.334 0-2.289-.544-2.839-.917-.747.374-2.094.917-4.161.917a.5.5 0 0 1 0-1c2.129 0 3.384-.63 3.964-.94M14 5h-4v3h3a1 1 0 0 0 1-1zM5 2a1 1 0 0 1 1-1h3v3H5zm4 3H5v2a1 1 0 0 0 1 1h3z"];
})), Ua, Wa = o((() => {
	Ua = ["M8.97 6.76c-.01-.05-.04-.08-.06-.13s-.03-.1-.05-.15c.08-.14.14-.3.14-.48 0-.55-.45-1-1-1s-1 .45-1 1c0 .18.06.34.14.48-.03.05-.03.1-.05.15s-.05.08-.06.13l-2 8c-.13.54.19 1.08.73 1.21a.995.995 0 0 0 1.21-.73L7.53 13h.94l.56 2.24a1 1 0 0 0 1.94-.48zM3.72 1.7C4.1 1.3 4.09.67 3.7.28S2.67-.09 2.28.3c-3.05 3.12-3.05 8.28 0 11.4a.996.996 0 1 0 1.43-1.39c-2.28-2.35-2.28-6.27.01-8.61m7.88 1.5c-.44-.33-1.07-.24-1.4.2s-.24 1.07.2 1.4c.43.32.53 1.96-.04 2.43-.42.35-.48.98-.13 1.41.35.42.98.48 1.41.13 1.59-1.33 1.39-4.5-.04-5.57M13.72.3c-.39-.4-1.02-.4-1.41-.02s-.41 1.02-.03 1.42c2.29 2.34 2.29 6.26 0 8.6-.39.39-.38 1.03.02 1.41s1.03.38 1.41-.02c3.05-3.11 3.05-8.27.01-11.39M5.4 7.23c-.57-.47-.47-2.11-.04-2.43.44-.33.53-.96.2-1.4s-.96-.53-1.4-.2c-1.44 1.07-1.63 4.24-.04 5.57.42.35 1.05.3 1.41-.13.35-.42.29-1.06-.13-1.41"];
})), Ga, Ka = o((() => {
	Ga = ["m8.29 7.71 3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3a1.003 1.003 0 0 0-1.42-1.42L13 7.59V1c0-.55-.45-1-1-1s-1 .45-1 1v6.59l-1.29-1.3a1.003 1.003 0 0 0-1.42 1.42M14.5 13h-13c-.83 0-1.5.67-1.5 1.5S.67 16 1.5 16h13c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5M1 5c.28 0 .53-.11.71-.29L3 3.41V10c0 .55.45 1 1 1s1-.45 1-1V3.41L6.29 4.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-3-3C4.53.11 4.28 0 4 0s-.53.11-.71.29l-3 3A1.003 1.003 0 0 0 1 5"];
})), qa, Ja = o((() => {
	qa = ["M0 15c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V9.4L0 11zm6-5.5V15c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-5l-1 1zM13 7l-1 1v7c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V7.88c-.26.07-.58.12-1 .12-1.96 0-2-1-2-1m2-6h-3c-.55 0-1 .45-1 1s.45 1 1 1h.59L8.8 6.78 5.45 5.11v.01C5.31 5.05 5.16 5 5 5s-.31.05-.44.11V5.1l-4 2v.01C.23 7.28 0 7.61 0 8c0 .55.45 1 1 1 .16 0 .31-.05.44-.11v.01L5 7.12 8.55 8.9v-.01c.14.06.29.11.45.11.28 0 .53-.11.71-.29L14 4.41V5c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1"];
})), Ya, Xa = o((() => {
	Ya = ["M6 10c-1.1 0-2-.9-2-2V3H1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1v2a1.003 1.003 0 0 0 1.71.71L5.41 13H10c.55 0 1-.45 1-1v-1.17l-.83-.83zm9-10H6c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h4.59l2.71 2.71c.17.18.42.29.7.29.55 0 1-.45 1-1V9c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), Za, Qa = o((() => {
	Za = ["m7.41 8 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L6 6.59V4c0-.55-.45-1-1-1s-1 .45-1 1v8c0 .55.45 1 1 1s1-.45 1-1V9.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), $a, eo = o((() => {
	$a = ["M12 5c-.28 0-.53.11-.71.29L8 8.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 12 5"];
})), to, no = o((() => {
	to = ["M10 3c-.55 0-1 .45-1 1v2.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42L7.59 8 4.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L9 9.41V12c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1"];
})), ro, io = o((() => {
	ro = ["m7.41 8 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C5.11 7.47 5 7.72 5 8s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42z"];
})), ao, oo = o((() => {
	ao = ["m10.71 7.29-4-4a1.003 1.003 0 0 0-1.42 1.42L8.59 8 5.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), so, co = o((() => {
	so = ["m12.71 9.29-4-4C8.53 5.11 8.28 5 8 5s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L8 7.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), lo, uo = o((() => {
	lo = ["M8 0C3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8m0 14c-3.3 0-6-2.7-6-6s2.7-6 6-6 6 2.7 6 6-2.7 6-6 6"];
})), fo, po = o((() => {
	fo = ["M11 7c-.28 0-.53.11-.71.29L9 8.59V5c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-1.29-1.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 11 7M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), mo, ho = o((() => {
	mo = ["M11 7H7.41L8.7 5.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C4.11 7.47 4 7.72 4 8s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L7.41 9H11c.55 0 1-.45 1-1s-.45-1-1-1M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), go, _o = o((() => {
	go = ["M8.71 4.29a1.003 1.003 0 0 0-1.42 1.42L8.59 7H5c-.55 0-1 .45-1 1s.45 1 1 1h3.59L7.3 10.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71zM8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), vo, yo = o((() => {
	vo = ["M8.71 4.29C8.53 4.11 8.28 4 8 4s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L7 7.41V11c0 .55.45 1 1 1s1-.45 1-1V7.41l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), bo, xo = o((() => {
	bo = ["M6.827 13.886Q7.394 13.999 8 14v2a8 8 0 0 1-1.56-.154zm2.733 1.96Q8.802 15.998 8 16v-2q.606-.002 1.173-.114zm-6.55-4.514a6 6 0 0 0 1.658 1.659l-.557.83-.395.59-.161.24a8 8 0 0 1-2.207-2.206zm11.635 1.109.006.003a8 8 0 0 1-2.206 2.207l-.557-.83-.556-.83a6 6 0 0 0 1.659-1.659zM0 8q.002-.803.153-1.56l.98.193.981.194a6 6 0 0 0 0 2.346l-.981.193v.001l-.98.193A8 8 0 0 1 0 8m16 0q-.002.802-.154 1.56l-.98-.193-.98-.194a6 6 0 0 0 0-2.346l1.96-.388Q15.998 7.198 16 8M4.112 2.178l.556.831a6 6 0 0 0-1.659 1.659L1.35 3.555a8 8 0 0 1 2.206-2.207zm8.333-.83a8 8 0 0 1 2.206 2.207l-.83.557V4.11l-.83.557a6 6 0 0 0-1.659-1.659zM8 0q.802.002 1.56.153l-.387 1.961a6 6 0 0 0-2.346 0L6.439.154A8 8 0 0 1 8 0"];
})), So, Co = o((() => {
	So = ["M15.02 5c0-1.66-1.34-3-3-3s-3 1.34-3 3a2.996 2.996 0 0 0 3.6 2.94C12.1 9.76 11.14 11 10.02 11c-.55 0-1 .45-1 1s.45 1 1 1c2.76 0 5-3.13 5-7 0-.2-.02-.39-.04-.58.01-.14.04-.28.04-.42m-11-3c-1.66 0-3 1.34-3 3a2.996 2.996 0 0 0 3.6 2.94C4.1 9.76 3.14 11 2.02 11c-.55 0-1 .45-1 1s.45 1 1 1c2.76 0 5-3.13 5-7 0-.2-.02-.39-.04-.58.01-.14.04-.28.04-.42 0-1.66-1.35-3-3-3"];
})), wo, To = o((() => {
	wo = ["m12 8-1.2 2.796-2.8 1.2 2.8 1.197L12 16l1.2-2.807L16 12l-2.8-1.204zM5 0 3.5 3.5 0 4.995 3.5 6.5 5 10l1.5-3.5L10 5 6.5 3.5z"];
})), Eo, Do = o((() => {
	Eo = ["M0 1a1 1 0 0 1 1-1h4a1 1 0 0 1 0 2H2v3a1 1 0 0 1-2 0zm1 15a1 1 0 0 1-1-1v-4a1 1 0 1 1 2 0v3h3a1 1 0 1 1 0 2zm14 0a1 1 0 0 0 1-1v-4a1 1 0 1 0-2 0v3h-3a1 1 0 1 0 0 2zm0-16a1 1 0 0 1 1 1v4a1 1 0 1 1-2 0V2h-3a1 1 0 1 1 0-2zM8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6"];
})), Oo, F = o((() => {
	Oo = ["M11 2c0-.55-.45-1-1-1h.22C9.88.4 9.24 0 8.5 0S7.12.4 6.78 1H7c-.55 0-1 .45-1 1v1h5zm2 0h-1v2H5V2H4c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), ko, Ao = o((() => {
	ko = ["M11.586 6a1 1 0 0 1 .707.293l1.414 1.414a1 1 0 0 1 .293.707V15a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1zM8 9a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zm0 2a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zm0 2a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zM8.09.91c.5 0 .91.408.91.908V2.5H5v-.682c0-.5.41-.909.91-.909h-.2C6.017.364 6.326 0 7 0s.982.364 1.29.91zM10 2h1.09c.5 0 .91.41.91.91V5H6a1 1 0 0 0-1 1v8H2.91c-.5 0-.91-.409-.91-.909V2.91c0-.5.41-.909.91-.909H4v1.5h6z"];
})), jo, Mo = o((() => {
	jo = ["M12 6c-.03 0-.07 0-.1.01A5 5 0 0 0 2 7c0 .11.01.22.02.33A3.51 3.51 0 0 0 0 10.5C0 12.43 1.57 14 3.5 14H12c2.21 0 4-1.79 4-4s-1.79-4-4-4"];
})), No, Po = o((() => {
	No = ["M11 11c-.28 0-.53.11-.71.29L9 12.59V8c0-.55-.45-1-1-1s-1 .45-1 1v4.59L5.71 11.3A.97.97 0 0 0 5 11a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 11 11m1-7c-.03 0-.07 0-.1.01A5 5 0 0 0 2 5c0 .11.01.22.02.33A3.51 3.51 0 0 0 0 8.5c0 1.41.84 2.61 2.03 3.17C2.2 10.17 3.46 9 5 9c.06 0 .13.02.19.02C5.07 8.7 5 8.36 5 8c0-1.66 1.34-3 3-3s3 1.34 3 3c0 .36-.07.7-.19 1.02.06 0 .13-.02.19-.02 1.48 0 2.7 1.07 2.95 2.47A3.96 3.96 0 0 0 16 8c0-2.21-1.79-4-4-4"];
})), I, L = o((() => {
	I = ["M12 4a4 4 0 0 1 3.944 4.67A1 1 0 0 0 15 8H7a1 1 0 0 0-1 1v3H3.5C1.57 12 0 10.43 0 8.5c0-1.4.83-2.61 2.02-3.17C2.01 5.22 2 5.11 2 5a5 5 0 0 1 9.9-.99c.03-.01.07-.01.1-.01M7 9h8v3H7zm3 1.5a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 0-1h-3a.5.5 0 0 0-.5.5m-1 0a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0M7 13h8v3H7zm3.5 1a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm-1.5.5a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0"];
})), R, Fo = o((() => {
	R = ["M11.9 4.01c.03-.01.07-.01.1-.01a4 4 0 0 1 3.907 3.14 3 3 0 0 0-3.028.739L10 10.757l-.879-.878A3 3 0 0 0 4 12h-.5C1.57 12 0 10.43 0 8.5c0-1.4.83-2.61 2.02-3.17C2.01 5.22 2 5.11 2 5a5 5 0 0 1 9.9-.99m3.865 5.346a1 1 0 0 1-.058 1.351l-5 5a1 1 0 0 1-1.414 0l-3-3a1 1 0 0 1 1.414-1.414L10 13.586l4.293-4.293a1 1 0 0 1 1.472.063"];
})), Io, Lo = o((() => {
	Io = ["M8.71 7.29C8.53 7.11 8.28 7 8 7s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L7 10.41V15c0 .55.45 1 1 1s1-.45 1-1v-4.59l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM12 4c-.03 0-.07 0-.1.01A5 5 0 0 0 2 5c0 .11.01.22.02.33a3.495 3.495 0 0 0 .07 6.37c-.05-.23-.09-.46-.09-.7 0-.83.34-1.58.88-2.12l3-3a2.993 2.993 0 0 1 4.24 0l3 3c.54.54.88 1.29.88 2.12 0 .16-.02.32-.05.47C15.17 10.78 16 9.5 16 8c0-2.21-1.79-4-4-4"];
})), Ro, z = o((() => {
	Ro = ["m15.71 7.29-3-3a1.003 1.003 0 0 0-1.42 1.42L13.59 8l-2.29 2.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M5 5a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 7.47 0 7.72 0 8s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L2.41 8 4.7 5.71c.19-.18.3-.43.3-.71m4-3c-.48 0-.87.35-.96.81l-2 10c-.01.06-.04.12-.04.19 0 .55.45 1 1 1 .48 0 .87-.35.96-.81l2-10c.01-.06.04-.12.04-.19 0-.55-.45-1-1-1"];
})), zo, Bo = o((() => {
	zo = ["M15 3h-2V2c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1v1H7V2c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v1H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1m-8.29 8.29a1.003 1.003 0 0 1-1.42 1.42l-3-3C2.11 9.53 2 9.28 2 9s.11-.53.29-.71l3-3a1.003 1.003 0 0 1 1.42 1.42L4.41 9zm7-1.58-3 3a1.003 1.003 0 0 1-1.42-1.42L11.59 9l-2.3-2.29a1.003 1.003 0 0 1 1.42-1.42l3 3c.18.18.29.43.29.71s-.11.53-.29.71"];
})), Vo, Ho = o((() => {
	Vo = ["M15.19 6.39h-1.85c-.11-.37-.27-.71-.45-1.04l1.36-1.36c.31-.31.31-.82 0-1.13l-1.13-1.13a.803.803 0 0 0-1.13 0l-1.36 1.36c-.33-.17-.67-.33-1.04-.44V.79c0-.44-.36-.8-.8-.8h-1.6c-.44 0-.8.36-.8.8v1.86c-.39.12-.75.28-1.1.47l-1.3-1.3c-.3-.3-.79-.3-1.09 0L1.82 2.91c-.3.3-.3.79 0 1.09l1.3 1.3c-.2.34-.36.7-.48 1.09H.79c-.44 0-.8.36-.8.8v1.6c0 .44.36.8.8.8h1.85c.11.37.27.71.45 1.04l-1.36 1.36c-.31.31-.31.82 0 1.13l1.13 1.13c.31.31.82.31 1.13 0l1.36-1.36c.33.18.67.33 1.04.44v1.86c0 .44.36.8.8.8h1.6c.44 0 .8-.36.8-.8v-1.86c.39-.12.75-.28 1.1-.47l1.3 1.3c.3.3.79.3 1.09 0l1.09-1.09c.3-.3.3-.79 0-1.09l-1.3-1.3c.19-.35.36-.71.48-1.1h1.85c.44 0 .8-.36.8-.8v-1.6a.816.816 0 0 0-.81-.79m-7.2 4.6c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3"];
})), Uo, Wo = o((() => {
	Uo = ["M7.29 6.71c.18.18.43.29.71.29s.53-.11.71-.29l4-4a1.003 1.003 0 0 0-1.42-1.42L8 4.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42zm1.42 2.58C8.53 9.11 8.28 9 8 9s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L8 11.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), Go, Ko = o((() => {
	Go = ["M3.093 7q.025-.075.058-.15c.106-.248.225-.397.263-.436L7 2.828 11.172 7zM6.5 13c1 0 2.5-1 3-1.5l3.086-3.086L14 7l-1.414-1.414-4.172-4.172L7 0 5.586 1.414 2 5c-.5.5-1 1.5-1 2.5s.5 2 1 2.5l2 2c.5.5 1.5 1 2.5 1m7-4 1.125 1.667c.238.353.375.666.375 1 0 .666-.375 1.333-1.5 1.333s-1.5-.667-1.5-1.333c0-.334.137-.647.375-1zM0 15a1 1 0 0 1 1-1h14a1 1 0 1 1 0 2H1a1 1 0 0 1-1-1"];
})), qo, Jo = o((() => {
	qo = ["M15 1H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M4 13H2V3h2zm3 0H5V3h2zm7 0H8V3h6z"];
})), Yo, Xo = o((() => {
	Yo = ["M14 1H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h2v3a1.003 1.003 0 0 0 1.71.71L8.41 12H14c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M3.5 8C2.67 8 2 7.33 2 6.5S2.67 5 3.5 5 5 5.67 5 6.5 4.33 8 3.5 8m4 0C6.67 8 6 7.33 6 6.5S6.67 5 7.5 5 9 5.67 9 6.5 8.33 8 7.5 8m4 0c-.83 0-1.5-.67-1.5-1.5S10.67 5 11.5 5s1.5.67 1.5 1.5S12.33 8 11.5 8"];
})), Zo, Qo = o((() => {
	Zo = ["M7.99-.01c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1v-14c0-.55-.45-1-1-1m-3 3h-4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1m10 0h-4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1m0 3h-4v-2h4zm0 3h-4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1m0 3h-4v-2h4zm-10-3h-4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1"];
})), $o, es = o((() => {
	$o = ["M12 8c0 .14-.03.27-.08.39l-3 6.99c-.15.37-.51.62-.92.62s-.77-.25-.92-.61l-3-6.99a1 1 0 0 1 0-.79l3-6.99C7.23.25 7.59 0 8 0s.77.25.92.61l3 6.99c.05.13.08.26.08.4M8 3.54 6.09 8h3.82z"];
})), ts, ns = o((() => {
	ts = ["M15.93 5.63v-.02L13.94.63C13.78.26 13.42 0 13 0H3c-.42 0-.78.26-.93.63L.08 5.61l-.01.02C.03 5.74 0 5.87 0 6v9c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V6c0-.13-.03-.26-.07-.37M9 2h3.32l1.2 3H9zM3.68 2H7v3H2.48zM14 14H2V7h5v2.59l-1.29-1.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3a1.003 1.003 0 0 0-1.42-1.42L9 9.59V7h5z"];
})), rs, is = o((() => {
	rs = ["M8.7 4.29a.97.97 0 0 0-.71-.3 1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l5-5a1.003 1.003 0 0 0-1.42-1.42l-4.29 4.3zm5.22 3.01c.03.23.07.45.07.69 0 3.31-2.69 6-6 6s-6-2.69-6-6 2.69-6 6-6c.81 0 1.59.17 2.3.46l1.5-1.5A7.998 7.998 0 0 0-.01 7.99c0 4.42 3.58 8 8 8s8-3.58 8-8c0-.83-.13-1.64-.36-2.39z"];
})), as, os = o((() => {
	as = ["M15 15H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1M14 5H2v8h12zM4 6c.28 0 .53.11.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2a1.003 1.003 0 0 1-1.42-1.42L4.59 9l-1.3-1.29A1.003 1.003 0 0 1 4 6m5 4h3c.55 0 1 .45 1 1s-.45 1-1 1H9c-.55 0-1-.45-1-1s.45-1 1-1"];
})), ss, cs = o((() => {
	ss = ["M13 1a1 1 0 1 1 2 0v3a1 1 0 1 1-2 0zm0 6a1 1 0 1 1 2 0 1 1 0 0 1-2 0M1 1h10v3c0 .35.06.687.17 1H2v8h12v-3c.768 0 1.47-.289 2-.764V14c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1m3 5c.28 0 .53.11.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2a1.003 1.003 0 0 1-1.42-1.42L4.59 9l-1.3-1.29A1.003 1.003 0 0 1 4 6m5 4h3c.55 0 1 .45 1 1s-.45 1-1 1H9c-.55 0-1-.45-1-1s.45-1 1-1"];
})), ls, us = o((() => {
	ls = ["M5 0a1 1 0 0 1 1 1v2h4V1a1 1 0 0 1 2 0v2h2.038c.216 0 .453 0 .65.022.202.022.584.086.894.396s.374.692.396.893c.022.198.022.435.022.65v4.077c0 .216 0 .453-.022.65-.022.202-.085.584-.396.894-.31.31-.692.374-.893.396a6 6 0 0 1-.65.022H12v4a1 1 0 1 1-2 0v-4H6v4a1 1 0 1 1-2 0v-4H1.962c-.216 0-.453 0-.65-.022-.202-.022-.584-.086-.894-.396S.044 9.89.022 9.69A6 6 0 0 1 0 9V4.962c0-.216 0-.453.022-.65.022-.202.086-.584.396-.894s.692-.374.893-.396C1.51 3 1.746 3 1.961 3H4V1a1 1 0 0 1 1-1m0 5h-.882l1.776 3.553.224.447h1.764L6.106 5.447 5.882 5zm3.118 0 1.776 3.553.224.447h1.764l-1.776-3.553L9.882 5zm4 0 1.776 3.553.106.211V5zM3.882 9 2.106 5.447 2 5.237V9z"];
})), ds, fs = o((() => {
	ds = ["M15.2 6.4h-1.44c-.13-.47-.32-.92-.56-1.34L14.26 4c.31-.31.31-.82 0-1.13l-1.13-1.13a.803.803 0 0 0-1.13 0L10.94 2.8c-.42-.24-.86-.42-1.34-.56V.8c0-.44-.36-.8-.8-.8H7.2c-.44 0-.8.36-.8.8v1.44c-.5.14-.96.34-1.4.59l-1-1c-.3-.3-.79-.3-1.09 0L1.83 2.91c-.3.3-.3.79 0 1.09l1 1c-.25.44-.45.9-.59 1.4H.8c-.44 0-.8.36-.8.8v1.6c0 .44.36.8.8.8h1.44c.13.47.32.92.56 1.34L1.74 12c-.31.31-.31.82 0 1.13l1.13 1.13c.31.31.82.31 1.13 0l1.06-1.06c.42.24.86.42 1.34.56v1.44c0 .44.36.8.8.8h1.6c.44 0 .8-.36.8-.8v-1.44c.5-.14.96-.33 1.4-.59l1 1c.3.3.79.3 1.09 0l1.09-1.09c.3-.3.3-.79 0-1.09l-1-1c.25-.43.45-.9.59-1.4h1.44c.44 0 .8-.36.8-.8V7.2a.82.82 0 0 0-.81-.8M8 12c-2.21 0-4-1.79-4-4s1.79-4 4-4z"];
})), ps, ms = o((() => {
	ps = ["M13 8H8v5h5zm0-5H8v4h5zm2-3H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2V2h12zM7 3H3v10h4z"];
})), hs, gs = o((() => {
	hs = ["M14.99 2.95h-14c-.55 0-1 .45-1 1v1h16v-1c0-.55-.45-1-1-1m-15 10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-6h-16zm5.5-2h5c.28 0 .5.22.5.5s-.22.5-.5.5h-5c-.28 0-.5-.22-.5-.5s.23-.5.5-.5m-3 0h1c.28 0 .5.22.5.5s-.22.5-.5.5h-1c-.28 0-.5-.22-.5-.5s.23-.5.5-.5"];
})), _s, vs = o((() => {
	_s = ["M11 15a1 1 0 1 0 2 0v-2h2a1 1 0 1 0 0-2H5V1a1 1 0 0 0-2 0v2H1a1 1 0 1 0 0 2h2v7a1 1 0 0 0 1 1h7zm1-12H6v2h5v5h2V4a1 1 0 0 0-1-1"];
})), ys, bs = o((() => {
	ys = ["m9.41 8 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L8 6.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42L6.59 8 3.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L8 9.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), xs, Ss = o((() => {
	xs = ["M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m3.7-10.29L9.41 8l2.3 2.29A1.003 1.003 0 0 1 11 12c-.28 0-.53-.11-.71-.3L8 9.41l-2.29 2.3A1.003 1.003 0 0 1 4 11c0-.28.11-.53.3-.71L6.59 8l-2.3-2.29a1.003 1.003 0 0 1 1.42-1.42L8 6.59l2.29-2.3A1.003 1.003 0 0 1 12 5c0 .28-.11.53-.3.71"];
})), Cs, ws = o((() => {
	Cs = ["m2 6 3 2 3-4 3 4 3-2-1 6H3zm6-5a1 1 0 1 1 0 2 1 1 0 0 1 0-2M1 3a1 1 0 1 1 0 2 1 1 0 0 1 0-2m14 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M3 13h10v2H3z"];
})), Ts, Es = o((() => {
	Ts = ["m11.5 1 .916 2.584L15 4.5l-2.584.916L11.5 8l-.916-2.584L8 4.5l2.584-.916zM8 .5a7 7 0 0 1 1.983.286L9.41 2.41l-.496.175a5 5 0 1 0 3.967 6q.018-.04.034-.083l.676-1.911 1.276-.452Q14.998 6.8 15 7.5c0 1.903-.76 3.629-1.993 4.89.302.275.493.67.493 1.11 0 .996-.77 1.515-1.05 1.68-.381.226-.832.376-1.258.482C10.318 15.881 9.19 16 8 16s-2.318-.12-3.192-.338c-.426-.106-.877-.257-1.257-.481-.28-.166-1.051-.685-1.051-1.681 0-.44.19-.835.492-1.11A7 7 0 0 1 8 .5M8 6l.51 1.49L10 8l-1.49.51L8 10l-.51-1.49L6 8l1.49-.51z"];
})), Ds, Os = o((() => {
	Ds = ["M2 1a1 1 0 0 1 1-1h7l5 5v10a1 1 0 0 1-1 1h-2.518A2.5 2.5 0 0 0 12 14.5q-.002-.267-.053-.5H13V6H9V2H4v8.514a2.6 2.6 0 0 0-.492.5A2.34 2.34 0 0 0 2 10.046zm5.491 14.988L7.5 16h-.018zM1.5 11a1.42 1.42 0 0 0-1.035.426c-.262.268-.41.626-.46 1.008L0 12.467V14.5c0 .76.655 1.5 1.5 1.5A1.5 1.5 0 0 0 3 14.5a.5.5 0 0 0-1 0 .5.5 0 0 1-.5.5c-.26 0-.5-.26-.5-.5v-1.964a.75.75 0 0 1 .18-.412A.42.42 0 0 1 1.5 12c.173 0 .264.048.321.104.066.064.146.197.184.466a.5.5 0 1 0 .99-.14c-.057-.406-.2-.773-.474-1.04-.28-.275-.642-.39-1.021-.39M4 12.5c0-.76.655-1.5 1.5-1.5A1.5 1.5 0 0 1 7 12.5a.5.5 0 0 1-1 0 .5.5 0 0 0-.5-.5c-.26 0-.5.26-.5.5 0 .092.028.154.129.236.126.103.31.188.575.308l.027.011c.23.104.533.239.773.434.274.225.496.55.496 1.011 0 .76-.655 1.5-1.5 1.5A1.5 1.5 0 0 1 4 14.5a.5.5 0 0 1 1 0 .5.5 0 0 0 .5.5c.26 0 .5-.26.5-.5 0-.092-.028-.154-.129-.236-.126-.103-.31-.188-.575-.308l-.027-.011c-.23-.104-.533-.239-.773-.434C4.222 13.286 4 12.96 4 12.5M9.5 11c-.845 0-1.5.74-1.5 1.5 0 .46.222.786.496 1.01.24.196.543.331.773.435l.027.011c.266.12.45.205.575.308.1.082.129.144.129.236 0 .24-.24.5-.5.5a.5.5 0 0 1-.5-.5.5.5 0 0 0-1 0A1.5 1.5 0 0 0 9.5 16c.845 0 1.5-.74 1.5-1.5 0-.46-.222-.786-.496-1.01-.24-.196-.543-.331-.773-.435l-.027-.011c-.266-.12-.45-.205-.575-.308-.1-.082-.129-.144-.129-.236 0-.24.24-.5.5-.5a.5.5 0 0 1 .5.5.5.5 0 0 0 1 0A1.5 1.5 0 0 0 9.5 11"];
})), ks, As = o((() => {
	ks = ["M14.194 3.54 8 7.41 1.806 3.54 7.504.283a1 1 0 0 1 .992 0zm.75.71a1 1 0 0 1 .056.33v6.84a1 1 0 0 1-.504.868L8.5 15.714V8.277zm-13.888 0L7.5 8.277v7.437l-5.996-3.426A1 1 0 0 1 1 11.42V4.58a1 1 0 0 1 .056-.33"];
})), js, Ms = o((() => {
	js = ["M14 2h1a1 1 0 0 1 0 2h-1v1a1 1 0 0 1-2 0V4h-1a1 1 0 0 1 0-2h1V1a1 1 0 0 1 2 0zM9.136.65a3.001 3.001 0 0 0 .992 5.222q.027.087.059.172L8 7.41 1.806 3.54 7.504.283a1 1 0 0 1 .992 0zM15 7.235v4.184a1 1 0 0 1-.504.868L8.5 15.714V8.277l2.187-1.367A3 3 0 0 0 13 8c.768 0 1.47-.289 2-.764M1.056 4.25 7.5 8.277v7.437l-5.996-3.426A1 1 0 0 1 1 11.42V4.58a1 1 0 0 1 .056-.33"];
})), Ns, Ps = o((() => {
	Ns = ["M15 0a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zm-4.43 6.731-1.604.947-.466.273v5.486l3.871-1.754c.38-.172.629-.589.629-1.052V5.3l-.001-.009c-.487.29-1.48.88-2.429 1.44M3 5.368v5.33c0 .429.214.821.553 1.013L7.5 13.393V7.95L3.005 5.295Q3 5.332 3 5.368m5.401-2.805a.9.9 0 0 0-.818-.038L3.629 4.317a1 1 0 0 0-.157.091L8 7.086l.458-.27 1.604-.946a646 646 0 0 0 2.516-1.491 1 1 0 0 0-.13-.09z"];
})), Fs, Is = o((() => {
	Fs = ["M15 3a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm-3.34 5.604c-.489.29-.966.57-1.32.779l-.34.2v4.424l3.098-1.403c.312-.142.517-.486.517-.867v-4.29c-.415.246-1.202.713-1.955 1.157m-6.275 3.189c0 .353.176.676.455.834L9 13.974V9.582L5.385 7.446zM9.83 5.099a.74.74 0 0 0-.674-.033L5.902 6.541l-.043.023L9.5 8.717l.332-.196 1.32-.778c.817-.482 1.662-.983 2.037-1.207l-.029-.018zM12 0a1 1 0 0 1 1 1v1H3a1 1 0 0 0-1 1v10H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1z"];
})), Ls, Rs = o((() => {
	Ls = ["M8.74 9.203 6.8 7.263l5.022-5.021 1.94 1.94zM5 11.008l1.093-3.033 1.942 1.941zM13.657.4c.251-.243.597-.4.975-.4.763 0 1.376.62 1.368 1.367 0 .385-.15.723-.401.974l-1.132 1.132-1.942-1.94zM8.496.284 10.96 1.69 6.301 6.349l-4.495-2.81L7.504.284a1 1 0 0 1 .992 0M1.056 4.25l4.52 2.824-.193.193a1 1 0 0 0-.256.44L4.059 10.67a1 1 0 0 0 1.28 1.28l2.161-.777v4.542l-5.996-3.426A1 1 0 0 1 1 11.42V4.58a1 1 0 0 1 .056-.33M8.5 15.714v-4.912a1 1 0 0 0 .314-.258l5.655-5.655.05-.054.46-.46q.021.101.021.205v6.84a1 1 0 0 1-.504.868z"];
})), zs, Bs = o((() => {
	zs = ["M10.365 5.933 8 7.41 1.806 3.54 7.504.283a1 1 0 0 1 .992 0l.64.365a3.001 3.001 0 0 0 1.228 5.283M15 6v5.42a1 1 0 0 1-.504.868L8.5 15.714V8.277L12.143 6zM1.056 4.25 7.5 8.277v7.437l-5.996-3.426A1 1 0 0 1 1 11.42V4.58a1 1 0 0 1 .056-.33M11 2h4a1 1 0 0 1 0 2h-4a1 1 0 0 1 0-2"];
})), Vs, Hs = o((() => {
	Vs = ["M3.978.124a1.12 1.12 0 0 1 1.145.073l2.368 1.616c.318.217.509.582.509.973v.668l-.749.305A2.02 2.02 0 0 0 6 5.632v.952l-.313-.213a2.12 2.12 0 0 0-2.164-.138l-2.521 1.29-.493-.336A1.18 1.18 0 0 1 0 6.214V2.883c0-.443.245-.848.632-1.046zm3.65 4.561 3.955-1.612a.98.98 0 0 1 .819.035l3.045 1.552c.339.173.553.526.553.912v4.796c0 .417-.249.792-.629.947l-3.954 1.612a.98.98 0 0 1-.819-.035L7.553 11.34A1.02 1.02 0 0 1 7 10.428V5.632c0-.417.249-.792.629-.947M6 7.795v2.633c0 .755.418 1.456 1.099 1.803l.901.46v.426c0 .443-.245.848-.632 1.047l-3.346 1.713a1.12 1.12 0 0 1-1.145-.074L.509 14.188A1.18 1.18 0 0 1 0 13.214v-3.33c0-.444.245-.85.632-1.047l3.346-1.713a1.12 1.12 0 0 1 1.145.073z"];
})), Us, Ws = o((() => {
	Us = ["M3.62 3.056C4.102 2.25 5 2 6 2a1 1 0 0 1 0 2c-.44 0-.615.065-.67.097a.7.7 0 0 0-.03.17 5 5 0 0 0 .01.612l.008.118c.03.48.074 1.18-.112 1.854A3 3 0 0 1 4.61 8c.29.348.483.737.596 1.149.186.674.142 1.375.112 1.854l-.007.118a5 5 0 0 0-.01.613.7.7 0 0 0 .028.169c.056.032.23.097.671.097a1 1 0 1 1 0 2c-1 0-1.897-.25-2.38-1.056a2.4 2.4 0 0 1-.313-1.05 6.5 6.5 0 0 1 .007-.89l.002-.023c.033-.573.056-.96-.038-1.301-.072-.26-.224-.535-.725-.786a1 1 0 0 1 0-1.788c.501-.251.653-.526.725-.786.094-.34.071-.728.038-1.301l-.002-.023a6.5 6.5 0 0 1-.007-.89c.025-.313.097-.692.312-1.05m1.687 8.828.016.015q-.018-.014-.016-.015m0-7.768q-.002 0 .016-.015-.015.016-.016.015m7.074-1.06C11.898 2.25 11 2 10 2a1 1 0 0 0 0 2c.44 0 .615.065.67.097a.7.7 0 0 1 .03.17 5 5 0 0 1-.01.612l-.008.118c-.03.48-.074 1.18.112 1.854.113.412.305.801.595 1.149-.29.348-.482.737-.595 1.149-.186.674-.142 1.375-.112 1.854l.007.118c.016.27.023.46.01.613a.7.7 0 0 1-.028.169c-.056.032-.23.097-.671.097a1 1 0 1 0 0 2c1 0 1.897-.25 2.38-1.056.216-.358.288-.737.313-1.05.025-.31.008-.629-.007-.89l-.002-.023c-.033-.573-.056-.96.038-1.301.072-.26.224-.535.725-.786a1 1 0 0 0 0-1.788c-.501-.251-.653-.526-.725-.786-.094-.34-.071-.728-.038-1.301l.002-.023c.015-.261.032-.58.007-.89a2.4 2.4 0 0 0-.312-1.05m-1.687 8.828-.016.015q.018-.014.016-.015m0-7.768q.002 0-.016-.015.015.016.016.015"];
})), Gs, Ks = o((() => {
	Gs = ["M15 12H3.12l1.81-1.39c1.73 1.01 5.53-.03 9.08-2.61l-1.22-1.5C10.3 8.3 7.86 9.37 6.65 9.29L14.3 3.4l-.6-.8-7.83 6.03c-.01-1.07 1.8-3.19 4.47-5.13L9.12 2C5.38 4.7 3.34 8.1 4.25 9.87L2 11.6V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), qs, Js = o((() => {
	qs = ["M13 2s.71-1.29 0-2L8.66 5.07l1.05 1.32zm.07 8c-.42 0-.82.09-1.18.26L3.31 0c-.69.71 0 2 0 2l3.68 5.02-2.77 3.24A2.996 2.996 0 0 0 0 13c0 1.66 1.34 3 3 3s3-1.34 3-3c0-.46-.11-.89-.29-1.27L8.1 8.54l2.33 3.19c-.18.39-.29.82-.29 1.27 0 1.66 1.31 3 2.93 3S16 14.66 16 13s-1.31-3-2.93-3M3 14c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m10.07 0c-.54 0-.98-.45-.98-1s.44-1 .98-1 .98.45.98 1-.44 1-.98 1"];
})), Ys, Xs = o((() => {
	Ys = ["M13 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6M3 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6m6.169-5.27.087.09 1.51 1.746 1.589.549a1 1 0 0 1 .65 1.16l-.032.112a1 1 0 0 1-1.159.65l-.112-.032-1.843-.636a1 1 0 0 1-.337-.198l-.092-.093-.959-1.109L7.041 7.5l1.691 1.819a1 1 0 0 1 .26.556L9 10v3a1 1 0 0 1-1.993.117L7 13l-.001-2.608-2.056-2.211a1 1 0 0 1-.081-1.264l.082-.1 2.825-3.026a1 1 0 0 1 1.4-.061M13 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m-10 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M11 1a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3"];
})), Zs, Qs = o((() => {
	Zs = ["M5 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1M4 7c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m4-2c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1m-2 6c0 1.1.9 2 2 2s2-.9 2-2c0-.53-2-5-2-5s-2 4.47-2 5M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6m4-9c0-.55-.45-1-1-1s-1 .45-1 1 .45 1 1 1 1-.45 1-1m0 2c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1"];
})), $s, ec = o((() => {
	$s = ["M12 4c-.03 0-.07 0-.1.01A5 5 0 0 0 2 5c0 .11.01.22.02.33A3.51 3.51 0 0 0 0 8.5C0 10.43 1.57 12 3.5 12H7V9c0-.71.551-1.1.806-1.25.32-.19.719-.326 1.123-.427C9.753 7.117 10.839 7 12 7s2.247.117 3.071.323c.32.08.636.182.913.315A4 4 0 0 0 12 4m0 6.5c1.133 0 2.176-.114 2.95-.308.383-.096.728-.218.99-.372l.06-.037V12c0 .552-1.79 1-4 1s-4-.448-4-1V9.783l.06.037c.262.154.607.276.99.372.774.194 1.817.308 2.95.308m3.94 2.32.06-.037V15c0 .552-1.79 1-4 1s-4-.448-4-1v-2.217l.06.037c.262.154.607.276.99.372.774.194 1.817.308 2.95.308s2.176-.114 2.95-.308c.383-.096.728-.218.99-.372M8 9c0 .552 1.79 1 4 1s4-.448 4-1-1.79-1-4-1-4 .448-4 1"];
})), tc, nc = o((() => {
	tc = ["M1 9.52c.889.641 2.308 1.133 4.003 1.354L5 11a6 6 0 0 0 2.664 4.988Q7.337 16 7 16c-3.215 0-5.846-.85-5.993-1.906L1 14zM11 6c2.762 0 5 2.238 5 5s-2.238 5-5 5-5-2.238-5-5 2.238-5 5-5m1 1-4 5h2.5l-.5 3 4-5h-2.5zm1-3.48v1.822a6.002 6.002 0 0 0-7.9 4.556l-.248-.03c-2.168-.28-3.733-.966-3.845-1.774L1 8V3.52C2.22 4.4 4.44 5 7 5s4.78-.6 6-1.48M7 0c3.31 0 6 .9 6 2s-2.69 2-6 2c-3.32 0-6-.9-6-2s2.68-2 6-2"];
})), rc, ic = o((() => {
	rc = ["M1.067 0C.477 0 0 .478 0 1.067V3.2c0 .59.478 1.067 1.067 1.067h2.24a5.34 5.34 0 0 0 2.9 3.734 5.34 5.34 0 0 0-2.9 3.733h-2.24A1.065 1.065 0 0 0 0 12.8v2.133C0 15.523.478 16 1.067 16H6.4c.59 0 1.067-.478 1.067-1.067V12.8c0-.59-.478-1.067-1.067-1.067H4.401a4.27 4.27 0 0 1 3.92-3.194l.212-.006V9.6c0 .59.478 1.067 1.067 1.067h5.333c.59 0 1.067-.478 1.067-1.067V6.4c0-.59-.478-1.067-1.067-1.067H9.6c-.59 0-1.067.478-1.067 1.067v1.067a4.27 4.27 0 0 1-4.132-3.2H6.4c.59 0 1.067-.478 1.067-1.067V1.067C7.467.477 6.989 0 6.4 0z"];
})), ac, oc = o((() => {
	ac = ["M13 2c0 1.1-2.69 2-6 2-3.32 0-6-.9-6-2s2.68-2 6-2c3.31 0 6 .9 6 2M1 8V3.52C2.22 4.4 4.44 5 7 5s4.78-.6 6-1.48V6a5 5 0 0 0-7.999 3.886C2.671 9.61 1 8.867 1 8m0 1.52c.902.65 2.35 1.148 4.078 1.363a5 5 0 0 0 6.75 3.772l.352.353C11.137 15.6 9.206 16 7 16c-3.31 0-6-.9-6-2zm13.29 6.19-2.256-2.265A4.002 4.002 0 0 1 6 10v-.028a4 4 0 1 1 7.445 2.063l2.265 2.255a1.003 1.003 0 0 1-1.42 1.42M10 12a2 2 0 1 0-2-2.028V10a2 2 0 0 0 2 2"];
})), sc, cc = o((() => {
	sc = ["M7 4c3.31 0 6-.9 6-2s-2.69-2-6-2C3.68 0 1 .9 1 2s2.68 2 6 2m-6-.48V8c0 .55.67 1.049 1.755 1.411l1.828-1.828A2 2 0 0 1 6 7c.548 0 1.052.218 1.417.583l.59.59A2 2 0 0 1 8 8c0-.527.18-1.044.568-1.432S9.473 6 10 6a4.97 4.97 0 0 1 3 1.005V3.52C11.78 4.4 9.56 5 7 5s-4.78-.6-6-1.48m0 6c.327.236.725.451 1.182.64A2.003 2.003 0 0 0 4.1 12.997a5.02 5.02 0 0 0 1.867 2.973C3.148 15.806 1 14.983 1 14zM14 11c0-2.2-1.8-4-4-4-.6 0-1 .4-1 1s.4 1 1 1c1.1 0 2 .9 2 2v.59l-.29-.3a1.003 1.003 0 0 0-1.42 1.42l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 15 11c-.28 0-.53.11-.71.3l-.29.29zm-9.29.71a1.003 1.003 0 0 1-1.42-1.42l2-2C5.47 8.11 5.72 8 6 8s.53.11.71.29l2 2A1.003 1.003 0 0 1 8 12c-.28 0-.53-.11-.71-.3L7 11.41V12c0 1.1.9 2 2 2 .6 0 1 .4 1 1s-.4 1-1 1c-2.2 0-4-1.8-4-4v-.59z"];
})), lc, uc = o((() => {
	lc = ["M8 4c3.31 0 6-.9 6-2s-2.69-2-6-2C4.68 0 2 .9 2 2s2.68 2 6 2m-6-.48V8c0 1.1 2.69 2 6 2s6-.9 6-2V3.52C12.78 4.4 10.56 5 8 5s-4.78-.6-6-1.48m0 6V14c0 1.1 2.69 2 6 2s6-.9 6-2V9.52C12.78 10.4 10.56 11 8 11s-4.78-.6-6-1.48"];
})), dc, fc = o((() => {
	dc = ["M11.99 4.99a1.003 1.003 0 0 0-1.71-.71l-2.29 2.3L5.7 4.29a.97.97 0 0 0-.71-.3 1.003 1.003 0 0 0-.71 1.71l2.29 2.29-2.29 2.29A1.003 1.003 0 0 0 5.7 11.7l2.29-2.29 2.29 2.29a1.003 1.003 0 0 0 1.42-1.42L9.41 7.99 11.7 5.7c.18-.18.29-.43.29-.71m-4-5c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.68 6-6 6"];
})), pc, mc = o((() => {
	pc = ["M15.707.293a1 1 0 0 1 0 1.414L13.914 3.5l1.793 1.793a1 1 0 0 1-1.414 1.414L12.5 4.914l-1.793 1.793a1 1 0 0 1-1.414-1.414L11.086 3.5 9.293 1.707A1 1 0 1 1 10.707.293L12.5 2.086 14.293.293a1 1 0 0 1 1.414 0M0 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 0 2H2v2a1 1 0 0 1-2 0zm1 12a1 1 0 0 1-1-1v-3a1 1 0 1 1 2 0v2h2.5a1 1 0 1 1 0 2zm11 0a1 1 0 0 0 1-1v-3a1 1 0 1 0-2 0v2H9a1 1 0 1 0 0 2zM9 9.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"];
})), hc, gc = o((() => {
	hc = ["M8 0 0 16h16zM7 5l5 10H2z"];
})), B, _c = o((() => {
	B = ["M6.08 6.67h-.84c.24-.92.56-1.6.96-2.03.24-.27.48-.4.71-.4.05 0 .08.01.11.04s.04.06.04.1-.03.11-.1.21c-.06.1-.1.2-.1.29q0 .195.15.33c.1.09.23.14.39.14.17 0 .31-.06.42-.17A.58.58 0 0 0 8 4.73c0-.22-.09-.39-.26-.53-.17-.13-.44-.2-.81-.2q-.885 0-1.59.48c-.48.32-.93.85-1.36 1.59-.15.26-.29.42-.42.49s-.35.11-.64.1l-.19.65h.81l-1.19 4.37c-.2.72-.33 1.16-.4 1.33-.1.24-.26.45-.46.62-.08.07-.18.1-.3.1-.03 0-.06-.01-.08-.03l-.03-.04c0-.02.03-.06.09-.11.06-.06.09-.14.09-.26 0-.13-.05-.23-.14-.32a.6.6 0 0 0-.4-.13c-.21 0-.38.05-.51.16s-.21.25-.21.4c0 .16.08.3.23.42.16.12.4.18.74.18.53 0 .99-.13 1.4-.39s.76-.65 1.07-1.19c.3-.54.62-1.4.94-2.59l.68-2.53h.82zM15 0H8c-.55 0-1 .45-1 1v2h2V2h5v12H9v-1H7v2c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M8.3 9.94c.18.52.33.89.46 1.13s.28.4.44.51c.17.1.37.16.62.16.24 0 .49-.08.74-.25.33-.21.66-.58 1.01-1.09l-.21-.11c-.23.31-.41.5-.52.57a.44.44 0 0 1-.26.07q-.18 0-.36-.21c-.2-.24-.46-.91-.8-2q.45-.735.75-.96c.15-.11.3-.16.47-.16.06 0 .17.02.34.06.16.04.31.06.43.06.17 0 .31-.06.43-.17.1-.11.16-.25.16-.43 0-.19-.06-.33-.17-.44-.12-.11-.28-.16-.49-.16-.19 0-.37.04-.54.13s-.39.27-.65.56c-.2.21-.48.58-.87 1.11-.15-.66-.41-1.26-.78-1.81l-2.05.33-.04.21c.15-.03.28-.04.39-.04.2 0 .37.08.5.25.21.26.5 1.03.88 2.33q-.435.555-.6.72c-.18.18-.33.3-.44.36-.09.04-.19.07-.3.07-.09 0-.23-.04-.42-.13a.9.9 0 0 0-.36-.09c-.2 0-.36.06-.49.18a.59.59 0 0 0-.19.46c0 .17.06.32.18.43s.28.16.48.16.38-.04.55-.11c.17-.08.39-.24.65-.49.24-.27.6-.66 1.06-1.21"];
})), vc, yc = o((() => {
	vc = ["M9.1 8A1.1 1.1 0 0 0 8 9.1v2.898a1 1 0 0 0-.328-.739l-.036-.037-2.929-2.93a1 1 0 0 0-1.414 1.415L4.586 11H3a1 1 0 0 1-1-1V1a1 1 0 1 0-2 0v9a3 3 0 0 0 3 3h1.586l-1.293 1.293a1 1 0 1 0 1.414 1.414l2.93-2.93.035-.036A1 1 0 0 0 8 12.002V14.9A1.1 1.1 0 0 0 9.1 16h5.8a1.1 1.1 0 0 0 1.1-1.1V9.1A1.1 1.1 0 0 0 14.9 8zm4.9 6h-4v-4h4z"];
})), V, bc = o((() => {
	V = ["M15 0H1C.45 0 0 .45 0 1v10c0 .55.45 1 1 1h4.75l-.5 2H4c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1h-1.25l-.5-2H15c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 10H2V2h12z"];
})), H, xc = o((() => {
	H = ["M1 0h4a1 1 0 0 1 0 2H2v3a1 1 0 0 1-2 0V1a1 1 0 0 1 1-1M0 15v-4a1 1 0 1 1 2 0v3h3a1 1 0 1 1 0 2H1a1 1 0 0 1-1-1m16 0a1 1 0 0 1-1 1h-4a1 1 0 1 1 0-2h3v-3a1 1 0 1 1 2 0zm0-14v4a1 1 0 1 1-2 0V2h-3a1 1 0 1 1 0-2h4a1 1 0 0 1 1 1M5 4h6a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1m1 2v4h4V6z"];
})), Sc, Cc = o((() => {
	Sc = ["M3.2 1a1 1 0 0 1 .117 1.993L3.2 3H3v3a2 2 0 0 0 1.85 1.995L5 8a2 2 0 0 0 1.995-1.85L7 6V3h-.2a1 1 0 0 1-.993-.883L5.8 2a1 1 0 0 1 .883-.993L6.8 1H8a1 1 0 0 1 .993.883L9 2v4a4 4 0 0 1-3.007 3.876v.007L6 10a3 3 0 0 0 5.995.176L12 10V7.792a2.5 2.5 0 1 1 2 0V10a5 5 0 0 1-10 0q0-.063.008-.125A4 4 0 0 1 1.005 6.2L1 6V2a1 1 0 0 1 .883-.993L2 1z"];
})), wc, Tc = o((() => {
	wc = ["M15 8v3h-2V9H9v2H7V9H3v2H1V8a1 1 0 0 1 1-1h5V5h2v2h5a1 1 0 0 1 1 1M1 12h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1m12 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1m-6 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1M7 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1"];
})), Ec, Dc = o((() => {
	Ec = ["m16 1.99-16 6 16 6-4-6z"];
})), Oc, kc = o((() => {
	Oc = ["m16 7.99-16-6 4 6-4 6z"];
})), Ac, jc = o((() => {
	Ac = ["M7.99-.01c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m-6 8c0-3.31 2.69-6 6-6 1.3 0 2.49.42 3.47 1.12l-8.35 8.35c-.7-.98-1.12-2.17-1.12-3.47m6 6c-1.3 0-2.49-.42-3.47-1.12l8.35-8.35c.7.98 1.12 2.17 1.12 3.47 0 3.32-2.68 6-6 6"];
})), Mc, U = o((() => {
	Mc = ["M9 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0M5 7c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1zm3 5a1 1 0 1 0 0-2 1 1 0 0 0 0 2"];
})), Nc, Pc = o((() => {
	Nc = ["M9 0H3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V5zm3 14H4V2h4v4h4z"];
})), Fc, Ic = o((() => {
	Fc = ["M10 0H3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h2.752l-.876-.876-.079-.078c-.302-.3-.66-.656-.797-1.046V2h5v3h3v3.171a3.02 3.02 0 0 1 2-.002V4zm5.71 13.71-2 2a1.003 1.003 0 0 1-1.42-1.42l1.3-1.29-1.3-1.29a1.003 1.003 0 0 1 1.42-1.42l2 2c.18.18.29.43.29.71s-.11.53-.29.71M10 15c0-.28-.11-.53-.29-.71L8.41 13l1.3-1.29a1.003 1.003 0 0 0-1.42-1.42l-2 2c-.18.18-.29.43-.29.71s.11.53.29.71l2 2A1.003 1.003 0 0 0 10 15"];
})), Lc, Rc = o((() => {
	Lc = ["M3 0h7l4 4v3.533A4 4 0 0 0 12 7V5H9V2H4v12h3v1.405q0 .306.07.595H3c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1m11 12h.48c.275 0 .52.175.52.45v2.955c0 .27-.245.595-.52.595h-5c-.275 0-.48-.325-.48-.595V12.45c0-.275.205-.45.48-.45H10v-1.025C10 9.885 10.895 9 12 9s2 .885 2 1.975zm-3-1.015V12h2v-1.015A.993.993 0 0 0 12 10c-.55 0-1 .44-1 .985"];
})), zc, Bc = o((() => {
	zc = ["M6 12c0 .55.45 1 1 1s1-.45 1-1V8c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1s.45 1 1 1h1.59L1.3 12.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L6 10.41zm4-12H4c-.55 0-1 .45-1 1v4h2V2h4v4h4v8H5.24l-1.8 1.8c.16.12.35.2.56.2h10c.55 0 1-.45 1-1V5z"];
})), Vc, Hc = o((() => {
	Vc = ["M10 14H2V2h4v4h1c0-.83.36-1.55.91-2.09l-.03-.03.9-.9C8.3 2.45 8 1.77 8 1L7 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V8.22c-.53.48-1.23.78-2 .78zm5-14h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59l-3.3 3.29a1.003 1.003 0 0 0 1.42 1.42L14 3.41V5c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), Uc, Wc = o((() => {
	Uc = ["M12.83 9.51q-.15-.45-.45-.84c-.2-.26-.45-.49-.75-.7q-.45-.3-1.05-.48c-.16-.04-.43-.11-.8-.2-.35-.09-.73-.18-1.12-.28s-.74-.19-1.06-.27c-.31-.08-.49-.12-.54-.13-.43-.12-.78-.29-1.05-.52s-.4-.55-.4-.95q0-.435.21-.72c.14-.19.32-.34.54-.46q.33-.165.72-.24c.26-.05.52-.08.77-.08.74 0 1.35.15 1.83.46.48.3.75.83.81 1.56h2.14c0-.6-.13-1.13-.38-1.58s-.59-.84-1.02-1.15-.93-.54-1.49-.7c-.24-.06-.49-.1-.75-.14V1c0-.55-.45-1-1-1s-1 .45-1 1v1.08c-.23.03-.46.07-.68.13-.54.13-1.02.34-1.44.61q-.63.42-1.02 1.05-.39.645-.39 1.5c0 .3.04.59.13.88s.23.56.44.82.48.49.83.7.79.38 1.31.51c.85.21 1.56.38 2.14.52.58.13 1.08.28 1.52.42.25.09.48.23.69.44s.32.53.32.97c0 .21-.05.42-.14.63s-.24.39-.45.55-.47.29-.81.39q-.495.15-1.2.15c-.43 0-.84-.05-1.21-.14s-.7-.24-.99-.43c-.29-.2-.51-.45-.67-.76s-.24-.68-.24-1.12H3c.01.71.15 1.32.43 1.84.27.52.64.94 1.1 1.27s.99.58 1.61.74c.27.07.56.12.85.16V15c0 .55.45 1 1 1s1-.45 1-1v-1.05c.3-.03.61-.08.9-.15q.87-.195 1.56-.63t1.11-1.11c.28-.45.42-1 .42-1.64 0-.31-.05-.61-.15-.91"];
})), Gc, Kc = o((() => {
	Gc = ["M8 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6"];
})), qc, Jc = o((() => {
	qc = ["m13.71 7.29-3-3A1.003 1.003 0 0 0 9 5v6a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M6 4c-.28 0-.53.11-.71.29l-3 3C2.11 7.47 2 7.72 2 8s.11.53.29.71l3 3A1.003 1.003 0 0 0 7 11V5c0-.55-.45-1-1-1"];
})), W, G = o((() => {
	W = ["M5 7h6a1.003 1.003 0 0 0 .71-1.71l-3-3C8.53 2.11 8.28 2 8 2s-.53.11-.71.29l-3 3A1.003 1.003 0 0 0 5 7m6 2H5a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 11 9"];
})), K, q = o((() => {
	K = ["M7.29 8.71c.18.18.43.29.71.29s.53-.11.71-.29l4-4a1.003 1.003 0 0 0-1.42-1.42L8 6.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42zM12 8c-.28 0-.53.11-.71.29L8 11.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 12 8"];
})), Yc, Xc = o((() => {
	Yc = ["M4.41 8 7.7 4.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C2.11 7.47 2 7.72 2 8s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42zm5 0 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C7.11 7.47 7 7.72 7 8s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42z"];
})), J, Zc = o((() => {
	J = ["M9 8c0-.28-.11-.53-.29-.71l-4-4a1.003 1.003 0 0 0-1.42 1.42L6.59 8 3.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4C8.89 8.53 9 8.28 9 8m4.71-.71-4-4a1.003 1.003 0 0 0-1.42 1.42L11.59 8 8.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), Qc, $c = o((() => {
	Qc = ["M4 8c.28 0 .53-.11.71-.29L8 4.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-4-4C8.53 2.11 8.28 2 8 2s-.53.11-.71.29l-4 4A1.003 1.003 0 0 0 4 8m4.71-.71C8.53 7.11 8.28 7 8 7s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L8 9.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), el, tl = o((() => {
	el = ["M11.86 7h4.05C15.45 3.39 12.61.52 9 .07v4.07A4 4 0 0 1 11.86 7M12 8c0 2.21-1.79 4-4 4s-4-1.79-4-4 1.79-4 4-4V0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8z"];
})), nl, rl = o((() => {
	nl = ["M7.99-.01c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8M11.7 9.7l-3 3c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-3-3A1.003 1.003 0 0 1 5.7 8.28l1.29 1.29V3.99c0-.55.45-1 1-1s1 .45 1 1v5.59l1.29-1.29a1.003 1.003 0 0 1 1.71.71c0 .27-.11.52-.29.7"];
})), il, al = o((() => {
	il = ["M2 9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m4 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m8-2c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1m0 2c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m-4-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1M6 5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1"];
})), ol, sl = o((() => {
	ol = ["M6 9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m4-6c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1M6 13c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m4 8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0 8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1"];
})), cl, ll = o((() => {
	cl = ["M14.9 11c-.3 0-.5.1-.7.3l-3 3c-.2.2-.3.4-.3.7 0 .6.5 1 1 1 .3 0 .5-.1.7-.3l3-3c.2-.2.3-.4.3-.7 0-.5-.4-1-1-1m-1-1v-.2l-1-5c-.1-.3-.3-.6-.6-.7l-11-4-.3.3 5.8 5.8c.2-.1.4-.2.6-.2.8 0 1.5.7 1.5 1.5S8.3 9 7.4 9s-1.5-.7-1.5-1.5c0-.2.1-.4.2-.6L.3 1.1l-.3.3 4 11c.1.3.4.6.7.6l5 1h.2c.3 0 .5-.1.7-.3l3-3c.2-.2.3-.4.3-.7"];
})), ul, dl = o((() => {
	ul = ["M7 0a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zM6 2H2v12h4zm2 5h4.59L11.3 5.71A.97.97 0 0 1 11 5a1.003 1.003 0 0 1 1.71-.71l3 3c.18.18.29.43.29.71s-.11.53-.29.71l-3 3a1.003 1.003 0 0 1-1.42-1.42L12.59 9H8z"];
})), fl, pl = o((() => {
	fl = ["M1 0h6a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1m7 7h4.59L11.3 5.71A.97.97 0 0 1 11 5a1.003 1.003 0 0 1 1.71-.71l3 3c.18.18.29.43.29.71s-.11.53-.29.71l-3 3a1.003 1.003 0 0 1-1.42-1.42L12.59 9H8z"];
})), ml, hl = o((() => {
	ml = ["M15 0a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zm-1 2h-4v12h4zM8 7H3.41L4.7 5.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 7.47 0 7.72 0 8s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L3.41 9H8z"];
})), gl, _l = o((() => {
	gl = ["M9 0h6a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1M8 7H3.41L4.7 5.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 7.47 0 7.72 0 8s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L3.41 9H8z"];
})), vl, yl = o((() => {
	vl = ["M15.12 4.76h-1.05l-.76-2.12c-.19-.53-.76-1.08-1.27-1.24 0 0-1.32-.4-4.04-.4s-4.04.4-4.04.4c-.5.16-1.07.71-1.26 1.24l-.77 2.12H.88c-.48 0-.88.42-.88.94s.4.94.88.94h.38L1 7c-.03.69 0 1.44 0 2v5c0 .66.38 1 1 1s1-.34 1-1v-1h10v1c0 .66.38 1 1 1s1-.34 1-1V9c0-.56-.01-1.37 0-2l-.26-.37h.38c.48 0 .88-.42.88-.93 0-.52-.4-.94-.88-.94M5 10H3V8h2zm8 0h-2V8h2zm0-4H3c-.18 0-.06-.82 0-1l.73-1.63C3.79 3.19 3.82 3 4 3h8c.18 0 .21.19.27.37L13 5c.06.18.18 1 0 1"];
})), bl, xl = o((() => {
	bl = ["M10.127.102c.516-.46 1.696.718 2.626 1.93Q12.873 2 13 2a1 1 0 0 1 .976 1.219c1.236.965 2.421 2.212 1.897 2.68-.515.46-1.694-.72-2.625-1.931a1 1 0 0 1-.521-.007.82.82 0 0 1-.152.608c-2.432 3.26-2.433 3.602 0 6.863a.82.82 0 0 1 .152.606 1 1 0 0 1 .491-.014c.965-1.236 2.213-2.42 2.68-1.897.46.516-.718 1.695-1.93 2.625a1 1 0 0 1-1.187 1.224c-.964 1.236-2.212 2.421-2.68 1.897-.458-.516.72-1.695 1.931-2.625a1 1 0 0 1 .006-.521.82.82 0 0 1-.606-.153c-3.26-2.432-3.602-2.432-6.862 0a.82.82 0 0 1-.609.153 1 1 0 0 1 .015.492c1.237.965 2.421 2.212 1.897 2.68-.515.46-1.694-.72-2.625-1.931Q3.13 13.999 3 14a1 1 0 0 1-.975-1.219C.788 11.816-.397 10.57.127 10.101c.516-.46 1.696.719 2.626 1.93a1 1 0 0 1 .52.007.82.82 0 0 1 .153-.606c2.432-3.261 2.432-3.602 0-6.863a.82.82 0 0 1-.152-.608 1 1 0 0 1-.493.015C1.817 5.212.57 6.397.101 5.873c-.458-.516.72-1.695 1.931-2.625a1 1 0 0 1 1.186-1.224C4.183.788 5.431-.396 5.898.127c.46.516-.718 1.695-1.93 2.625a1 1 0 0 1-.007.521c.21-.03.429.019.609.153 3.26 2.432 3.601 2.432 6.862 0a.82.82 0 0 1 .606-.153 1 1 0 0 1-.013-.492C10.788 1.816 9.603.57 10.127.101"];
})), Sl, Cl = o((() => {
	Sl = ["M8 0c2.318 0 2 3 1 5v2l7 2v1H9v2.066L13 13v1H8.964l-.057 1H10v1H6v-1h1.093l-.057-1H3v-1l4-.934V10H0V9l7-2V5C6 3 5.683 0 8 0"];
})), wl, Tl = o((() => {
	wl = ["M15 0H5c-.55 0-1 .45-1 1v2h2V2h8v7h-1v2h2c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-4 4H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m-1 10H2V6h8z"];
})), El, Dl = o((() => {
	El = ["m3.25 10.26 2.47 2.47 6.69-6.69-2.46-2.48zM.99 14.99l3.86-1.39-2.46-2.44zm12.25-14c-.48 0-.92.2-1.24.51l-1.44 1.44 2.47 2.47 1.44-1.44c.32-.32.51-.75.51-1.24.01-.95-.77-1.74-1.74-1.74"];
})), Ol, kl = o((() => {
	Ol = ["M4 9h8a1.003 1.003 0 0 0 .71-1.71l-4-4C8.53 3.11 8.28 3 8 3s-.53.11-.71.29l-4 4A1.003 1.003 0 0 0 4 9m8 1H4c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1"];
})), Al, jl = o((() => {
	Al = ["M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0m0 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1M4 8c.228 2.262 2 4 4 4 1.938 0 3.77-1.738 3.984-3.8L12 8h1c-.128 2.888-2.317 5-5 5a5 5 0 0 1-4.995-4.783L3 8zm2-3a1 1 0 1 1 0 2 1 1 0 0 1 0-2m4 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"];
})), Ml, Nl = o((() => {
	Ml = ["M.594 15.394q.594.606 1.56.606.653 0 1.202-.295c.377-.197.61-.33.936-.62v.729H6v-4.52q0-1.601-.683-2.44Q4.648 8 3.282 8a4.5 4.5 0 0 0-1.633.295q-.757.295-1.367.7l.624 1.195q.49-.31.995-.528a2.7 2.7 0 0 1 1.054-.217q.372 0 .624.124a.9.9 0 0 1 .401.326q.164.202.223.482.075.264.09.559a12 12 0 0 0-1.946.357q-.802.233-1.337.575a2.2 2.2 0 0 0-.772.823Q0 13.157 0 13.763q0 1.01.594 1.631m2.911-1.01a1.5 1.5 0 0 1-.802.218q-.461 0-.757-.233-.297-.233-.297-.746 0-.279.133-.528.134-.248.446-.435.312-.202.817-.357a7.5 7.5 0 0 1 1.247-.249v1.71q-.416.403-.787.62m6.135 1.371q.548.245 1.079.245.64 0 1.234-.276T13 14.928q.453-.522.719-1.272.28-.766.281-1.731 0-.873-.203-1.578a3.4 3.4 0 0 0-.594-1.195 2.54 2.54 0 0 0-.953-.766 2.9 2.9 0 0 0-1.281-.276q-.594 0-1.172.26c-.375.174-.677.399-1 .675V5H7v10.816h1.797v-.62c.3.294.465.374.772.524zm1.985-1.854q-.515.644-1.281.643-.345 0-.75-.137c-.184-.065-.37-.246-.559-.43q-.118-.116-.238-.223V10.5c.583-.562 1.146-.935 1.687-.935q.876 0 1.266.629.39.628.39 1.761 0 1.287-.515 1.946m2.082-12.644a3.6 3.6 0 0 1-.707.069v1.028h1.737V8H16V0h-.94q-.06.366-.262.617a1.55 1.55 0 0 1-.475.412 2 2 0 0 1-.616.228"];
})), Pl, Fl = o((() => {
	Pl = ["m15.86 7.5-.81-1.42V4.5c0-.36-.19-.68-.49-.87l-1.37-.8-.81-1.41c-.19-.31-.51-.49-.86-.49H9.89L8.5.14a.95.95 0 0 0-1 0l-1.39.8H4.52a1 1 0 0 0-.86.49l-.8 1.37-1.44.83c-.3.19-.49.51-.49.87v1.65l-.8 1.37c-.08.15-.13.32-.13.49s.05.34.14.49l.8 1.37v1.65c0 .36.19.68.49.87l1.42.81.8 1.37c.19.31.51.49.86.49H6.1l1.39.8c.15.09.32.14.48.14s.34-.05.49-.14l1.39-.8h1.63a1 1 0 0 0 .86-.49l.81-1.41 1.37-.8c.3-.19.49-.51.49-.87V9.93l.81-1.42a.89.89 0 0 0 .04-1.01m-4.12-.82-4.01 4.01c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-2-2c-.18-.19-.3-.44-.3-.71a1.003 1.003 0 0 1 1.71-.71l1.3 1.3 3.3-3.3a1.003 1.003 0 0 1 1.71.71.95.95 0 0 1-.29.7"];
})), Il, Ll = o((() => {
	Il = ["M6.533 0H.467A.47.47 0 0 0 0 .467v4.066C0 4.79.243 5 .5 5h2.609l1.693 1.865a.468.468 0 0 0 .798-.331V5h.933C6.79 5 7 4.79 7 4.533V.467A.47.47 0 0 0 6.533 0m7.017 13.468c.93.378 1.98.805 2.236 1.39.285.65.208 1.06.194 1.131l-.001.01H5.027s-.131-.426.186-1.148c.256-.585 1.305-1.012 2.236-1.39.219-.09.431-.176.625-.26.904-.4.918-.662.935-.979l.008-.116.003-.072q.004-.036.004-.072a3.1 3.1 0 0 1-.84-1.239l-.006-.006q0-.006-.004-.01l-.003-.011a3 3 0 0 1-.103-.337c-.241-.041-.379-.296-.434-.537-.048-.096-.158-.33-.138-.591.035-.351.18-.51.344-.571v-.055c0-.44.035-1.067.117-1.48a2.56 2.56 0 0 1 .956-1.623C9.348 5.172 9.96 5 10.504 5c.543 0 1.156.179 1.596.502a2.53 2.53 0 0 1 .956 1.624c.076.412.117 1.045.117 1.479v.062c.151.062.29.22.323.564a1.1 1.1 0 0 1-.137.598c-.048.234-.186.489-.42.537-.027.11-.062.227-.103.33a3.1 3.1 0 0 1-.832 1.259q-.002.084.006.158.006.072.008.139c.01.306.02.565.908.955.193.085.406.172.625.26"];
})), Rl, zl = o((() => {
	Rl = ["M0 3.06v9.88L4.94 8zM14.94 2H1.06L8 8.94zm-6.41 8.53c-.14.14-.32.22-.53.22s-.39-.08-.53-.22L6 9.06 1.06 14h13.88L10 9.06zM11.06 8 16 12.94V3.06z"];
})), Bl, Vl = o((() => {
	Bl = ["M3 5h10a1 1 0 0 1 0 2H3a1 1 0 1 1 0-2m0 4h10a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2"];
})), Y, Hl = o((() => {
	Y = ["m8.06 13.91 7.63-7.44c.41-.4.41-1.05 0-1.45L10.86.3c-.41-.4-1.08-.4-1.49 0L.31 9.13c-.41.4-.41 1.05 0 1.45l5.58 5.44h8.12v-.01c.55 0 1-.45 1-1s-.45-1-1-1H7.96zm-2.17.06L1.67 9.85l4.22-4.11 4.22 4.11z"];
})), Ul, Wl = o((() => {
	Ul = ["M7.99-.01c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m1 13h-2v-2h2zm0-3h-2v-7h2z"];
})), Gl, Kl = o((() => {
	Gl = ["M6.52 3.18c.51-.27 1.12-.4 1.83-.4.48 0 .91.06 1.27.18.37.12.68.29.96.51.18.14.3.33.44.51l1.53-1.53c-.12-.11-.23-.22-.36-.32a5.6 5.6 0 0 0-1.74-.83Q9.46 1 8.35 1c-.99 0-1.88.18-2.66.53-.79.35-1.45.82-2 1.41-.55.58-.96 1.27-1.26 2.06H2c-.55 0-1 .45-1 1s.45 1 1 1h.04c-.01.17-.04.33-.04.5s.03.33.04.5H2c-.55 0-1 .45-1 1s.45 1 1 1h.43c0 .01 0 .02.01.02a6.2 6.2 0 0 0 1.25 2.07 5.8 5.8 0 0 0 2 1.4c.78.34 1.67.51 2.66.51.81 0 1.54-.12 2.21-.36s1.25-.59 1.75-1.03l.03-.03-1.55-1.33c-.01.01-.02.03-.03.04q-.435.45-1.02.69c-.4.17-.85.25-1.37.25-.71 0-1.32-.13-1.83-.4s-.93-.62-1.25-1.07c-.19-.24-.34-.49-.46-.76H9c.55 0 1-.45 1-1s-.45-1-1-1H4.35c-.01-.17-.03-.33-.03-.5s.02-.34.03-.5H10c.55 0 1-.45 1-1s-.45-1-1-1H4.83c.13-.27.27-.52.44-.76.32-.44.74-.8 1.25-1.06M14 8.98v.01z"];
})), ql, Jl = o((() => {
	ql = ["M1.722 1.111A1 1 0 0 1 3.064.425L5.99 1.596a1 1 0 0 1 .523 1.376L6 4 3 3 2 8h3l-2.237 2.11a.94.94 0 0 1-.948.221C.782 9.973.045 9.424.002 8.124A1 1 0 0 1 .03 7.88zM14.22 6a1 1 0 0 1 .97.757l.5 2A1 1 0 0 1 14.72 10H8a1 1 0 0 1-1-1V5.303a1 1 0 0 1 .168-.555l1.535-2.303A1 1 0 0 1 9.535 2H12a1 1 0 0 1 1 1v3zm-3.89-2L9 6h2V4zM5.5 11h8a2.5 2.5 0 0 1 0 5h-8a2.5 2.5 0 0 1 0-5m0 2a.5.5 0 0 0 0 1h8a.5.5 0 0 0 0-1z"];
})), Yl, Xl = o((() => {
	Yl = ["M1.99 5.99c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.89-2-2-2m4.15 1.86a.495.495 0 1 0 .7-.7L5.7 5.99h5.79c.28 0 .5-.22.5-.5s-.22-.5-.5-.5H5.7l1.15-1.15a.495.495 0 1 0-.7-.7l-2 2c-.1.09-.16.21-.16.35s.06.26.15.35zm7.85-1.86c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.89-2-2-2M9.85 8.14a.53.53 0 0 0-.36-.15.495.495 0 0 0-.35.85l1.15 1.15h-5.8c-.28 0-.5.22-.5.5s.22.5.5.5h5.79l-1.15 1.15a.495.495 0 1 0 .7.7l2-2c.09-.09.15-.22.15-.35s-.06-.26-.15-.35z"];
})), Zl, Ql = o((() => {
	Zl = ["M0 10a1.003 1.003 0 0 0 1.71.71L3 9.41l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L4.41 8 5.7 6.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L3 6.59l-1.29-1.3A1.003 1.003 0 0 0 .29 6.71L1.59 8 .29 9.29C.11 9.47 0 9.72 0 10m1-7h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 10H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m-1-7H9c-1.1 0-2 .9-2 2s.9 2 2 2h5c1.1 0 2-.9 2-2s-.9-2-2-2"];
})), $l, eu = o((() => {
	$l = ["M4 7c.28 0 .53-.11.71-.29L8 3.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-4-4C8.53 1.11 8.28 1 8 1s-.53.11-.71.29l-4 4A1.003 1.003 0 0 0 4 7m8 2c-.28 0-.53.11-.71.29L8 12.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 12 9"];
})), tu, nu = o((() => {
	tu = ["M8 0a8 8 0 0 1 8 8v8H8A8 8 0 1 1 8 0M6 9a1 1 0 0 1 1 1v2.49a.51.51 0 0 0 .948.26l2.986-5.039a.47.47 0 0 0-.405-.71H10a1 1 0 0 1-1-1V3.51a.51.51 0 0 0-.948-.26L5.066 8.289A.471.471 0 0 0 5.47 9z"];
})), ru, iu = o((() => {
	ru = ["M4 6c.28 0 .53-.11.71-.29L7 3.41V11c0 .55.45 1 1 1s1-.45 1-1V3.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-4-4C8.53.11 8.28 0 8 0s-.53.11-.71.29l-4 4A1.003 1.003 0 0 0 4 6m11 5c-.55 0-1 .45-1 1v2H2v-2c0-.55-.45-1-1-1s-1 .45-1 1v3c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1"];
})), au, ou = o((() => {
	au = ["M16 7.97V7.9a.67.67 0 0 0-.17-.36c-.49-.63-1.07-1.2-1.65-1.72l-3.16 2.26a2.98 2.98 0 0 1-2.98 2.9c-.31 0-.6-.06-.88-.15L5.09 12.3c.44.19.9.36 1.37.47.97.23 1.94.24 2.92.05.88-.17 1.74-.54 2.53-.98 1.25-.7 2.39-1.67 3.38-2.75.18-.2.37-.41.53-.62.09-.1.15-.22.17-.36v-.1c.01-.02.01-.03.01-.04m-.43-4.17c.25-.18.43-.46.43-.8 0-.55-.45-1-1-1-.22 0-.41.08-.57.2l-.01-.01-2.67 1.91c-.69-.38-1.41-.69-2.17-.87a6.8 6.8 0 0 0-2.91-.05c-.88.18-1.74.54-2.53.99-1.25.7-2.39 1.67-3.38 2.75-.18.2-.37.41-.53.62-.23.29-.23.63-.01.92.51.66 1.11 1.25 1.73 1.79.18.16.38.29.56.44l-2.09 1.5.01.01c-.25.18-.43.46-.43.8 0 .55.45 1 1 1 .22 0 .41-.08.57-.2l.01.01 14-10zm-10.41 5a3 3 0 0 1-.11-.8 2.99 2.99 0 0 1 2.99-2.98c.62 0 1.19.21 1.66.53z"];
})), su, cu = o((() => {
	su = ["M10.29 6.7c.18.18.43.29.71.29s.53-.11.71-.29l4-4c.17-.18.29-.43.29-.7a1.003 1.003 0 0 0-1.71-.71L11 4.58 9.71 3.29A1 1 0 0 0 9 3c-.55 0-1 .44-1 1a1 1 0 0 0 .3.7zM16 7.96v-.07a.64.64 0 0 0-.17-.36c-.3-.4-.65-.76-1-1.12l-1.7 1.7c-.55.55-1.3.88-2.13.88-.06 0-.11-.01-.17-.02C10.42 10.15 9.32 11 8.01 11A3.005 3.005 0 0 1 6.4 5.46c-.24-.43-.39-.93-.39-1.46 0-.26.04-.5.1-.74-.7.2-1.37.5-2.01.86-1.26.7-2.4 1.68-3.4 2.77-.18.21-.36.41-.53.63-.22.29-.22.64 0 .93.51.67 1.12 1.27 1.73 1.81 1.33 1.17 2.85 2.15 4.53 2.55.97.23 1.95.24 2.92.05.89-.18 1.74-.54 2.54-.99 1.25-.71 2.4-1.69 3.39-2.78.18-.2.37-.41.54-.63.09-.1.15-.23.17-.37v-.1c.01-.01.01-.02.01-.03M8.01 9c.48 0 .87-.35.96-.81a.6.6 0 0 1-.07-.09l-.02.01L7.8 7.03c-.45.1-.79.48-.79.96 0 .56.45 1.01 1 1.01"];
})), lu, uu = o((() => {
	lu = ["M8.002 7.003a1.003 1.003 0 0 0 0 2.005 1.003 1.003 0 0 0 0-2.005m7.988.972v-.07a.7.7 0 0 0-.17-.36c-.509-.673-1.118-1.264-1.737-1.806-1.328-1.173-2.846-2.155-4.523-2.546a6.7 6.7 0 0 0-2.925-.06c-.889.18-1.738.541-2.546.992C2.84 4.837 1.692 5.81.694 6.902c-.18.211-.36.411-.53.632a.74.74 0 0 0 0 .932c.51.672 1.119 1.264 1.738 1.805 1.328 1.173 2.846 2.156 4.523 2.547.968.23 1.947.24 2.925.04.889-.18 1.738-.542 2.546-.993 1.248-.712 2.397-1.684 3.395-2.777.18-.2.37-.411.54-.632.09-.1.149-.23.169-.36v-.1c0-.01-.01-.01-.01-.02m-7.988 3.038a3 3 0 0 1-2.995-3.008 3 3 0 0 1 2.995-3.008 3 3 0 0 1 2.996 3.008 3 3 0 0 1-2.996 3.008"];
})), du, fu = o((() => {
	du = ["M14 3c-.24 0-.44.09-.62.23l-.01-.01L9 6.72V4c0-.55-.45-1-1-1-.24 0-.44.09-.62.23v-.01l-5 4 .01.01C2.16 7.41 2 7.68 2 8s.16.59.38.77v.01l5 4 .01-.01c.17.14.37.23.61.23.55 0 1-.45 1-1V9.28l4.38 3.5.01-.01c.17.14.37.23.61.23.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), pu, mu = o((() => {
	pu = ["M15 8c0-.32-.16-.59-.38-.77l.01-.01-5-4-.01.01A1 1 0 0 0 9 3c-.55 0-1 .45-1 1v2.72l-4.38-3.5v.01A1 1 0 0 0 3 3c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1 .24 0 .44-.09.62-.23l.01.01L8 9.28V12c0 .55.45 1 1 1 .24 0 .44-.09.62-.23l.01.01 5-4-.01-.01c.22-.18.38-.45.38-.77"];
})), hu, gu = o((() => {
	hu = ["M1.99 11.99c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.89-2-2-2m1-4c-.55 0-1 .45-1 1s.45 1 1 1c1.66 0 3 1.34 3 3 0 .55.45 1 1 1s1-.45 1-1c0-2.76-2.24-5-5-5m0-4c-.55 0-1 .45-1 1s.45 1 1 1c3.87 0 7 3.13 7 7 0 .55.45 1 1 1s1-.45 1-1a9 9 0 0 0-9-9m0-4c-.55 0-1 .45-1 1s.45 1 1 1c6.08 0 11 4.92 11 11 0 .55.45 1 1 1s1-.45 1-1c0-7.18-5.82-13-13-13"];
})), _u, vu = o((() => {
	_u = ["M3 2c1.06 0 2.08.16 3.06.45.13-.71.52-1.32 1.05-1.76C5.82.25 4.44 0 3 0c-.55 0-1 .45-1 1s.45 1 1 1M2 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m8.32-6.33a.99.99 0 0 0 1.4 0l3.98-3.98c.19-.18.3-.42.3-.7 0-.55-.45-.99-1-.99-.28 0-.52.11-.7.29l-3.28 3.28-1.29-1.29a1 1 0 0 0-.7-.29 1 1 0 0 0-1 .99c0 .27.11.52.29.7zm3.73.53-.93.93-.02-.02c-.17.17-.35.33-.56.45C13.47 9.16 14 11.02 14 13c0 .55.45 1 1 1s1-.45 1-1c0-2.5-.73-4.82-1.95-6.8M3 8c-.55 0-1 .45-1 1s.45 1 1 1c1.66 0 3 1.34 3 3 0 .55.45 1 1 1s1-.45 1-1c0-2.76-2.24-5-5-5m5.91-.91-.03.03-2-2 .03-.03c-.11-.11-.23-.2-.33-.33A8.9 8.9 0 0 0 3 4c-.55 0-1 .45-1 1s.45 1 1 1c3.87 0 7 3.13 7 7 0 .55.45 1 1 1s1-.45 1-1c0-1.87-.57-3.61-1.55-5.06-.61-.11-1.13-.42-1.54-.85"];
})), yu, bu = o((() => {
	yu = ["M11.693 2.693a.5.5 0 0 0 .654.047L15.44.42c.093-.07.21.047.14.14l-2.32 3.093a.5.5 0 0 0 .047.654l.34.34a.5.5 0 0 1 0 .707l-1.47 1.47a.5.5 0 0 0-.142.423l.93 6.506a.5.5 0 0 1-.142.424l-.59.59a.5.5 0 0 1-.54.11L7.275 13.11a.2.2 0 0 0-.274.185v2.011a.5.5 0 0 1-.658.475L4.42 15.14a.5.5 0 0 1-.332-.573l.392-1.962a.2.2 0 0 0-.055-.18L4 12l-.424-.424a.2.2 0 0 0-.181-.055l-1.962.392a.5.5 0 0 1-.573-.332L.22 9.658A.5.5 0 0 1 .693 9h2.01a.2.2 0 0 0 .186-.274l-1.768-4.42a.5.5 0 0 1 .111-.54l.59-.59a.5.5 0 0 1 .424-.14l6.506.929a.5.5 0 0 0 .424-.142l1.47-1.47a.5.5 0 0 1 .707 0z"];
})), xu, Su = o((() => {
	xu = ["M15 1h-5v2H6V1H1c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h5v-2h4v2h5c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M4 13H2v-2h2zm0-3H2V8h2zm0-3H2V5h2zm0-3H2V2h2zm6 6H6V5h4zm4 3h-2v-2h2zm0-3h-2V8h2zm0-3h-2V5h2zm0-3h-2V2h2z"];
})), Cu, wu = o((() => {
	Cu = ["M13.99.99h-12a1.003 1.003 0 0 0-.71 1.71l4.71 4.71V14a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71V7.41L14.7 2.7a1.003 1.003 0 0 0-.71-1.71"];
})), Tu, Eu = o((() => {
	Tu = ["M15 10c-.28 0-.53.11-.71.29L12 12.59l-1.29-1.29A.97.97 0 0 0 10 11a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 15 10m-3-8c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L4 6.41V12a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71V6.41l3.71-3.71c.18-.17.29-.42.29-.7"];
})), Du, Ou = o((() => {
	Du = ["M9 8c0 .55.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1h-5c-.55 0-1 .45-1 1m3-6c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L4 6.41V12a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71V6.41l3.71-3.71c.18-.17.29-.42.29-.7m3 8h-5c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m0 3h-5c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1"];
})), ku, Au = o((() => {
	ku = ["M15.707 10.293a1 1 0 0 1 0 1.414l-3 3c-.63.63-1.707.184-1.707-.707V8c0-.89 1.077-1.337 1.707-.707zM12 2c0 .28-.11.53-.29.7L8 6.41V10c0 .28-.11.53-.29.71l-2 2A1.003 1.003 0 0 1 4 12V6.41L.29 2.71A1.003 1.003 0 0 1 1 1h10c.55 0 1 .45 1 1"];
})), ju, Mu = o((() => {
	ju = ["M12 2c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L4 6.41V12a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71V6.41l3.71-3.71c.18-.17.29-.42.29-.7m2.41 10 1.29-1.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L13 10.59 11.71 9.3A.97.97 0 0 0 11 9a1.003 1.003 0 0 0-.71 1.71l1.3 1.29-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l1.29-1.3 1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), Nu, Pu = o((() => {
	Nu = ["M16 2c0 .28-.11.53-.29.7L12 6.41V10c0 .28-.11.53-.29.71l-2 2A1.003 1.003 0 0 1 8 12V6.41l-3.71-3.7A1.003 1.003 0 0 1 5 1h10c.55 0 1 .45 1 1M5 12.005c-.28 0-.53-.11-.71-.29l-.29-.29v3.576c0 .55-.45 1-1 1s-1-.45-1-1v-3.585l-.29.29a1.002 1.002 0 0 1-1.42-1.418l2-1.998C2.47 8.11 2.72 8 3 8s.53.11.71.29l2 1.997c.18.18.29.43.29.71 0 .559-.45 1.008-1 1.008"];
})), Fu, Iu = o((() => {
	Fu = ["M16 2c0 .28-.11.53-.29.7L12 6.41V10c0 .28-.11.53-.29.71l-2 2A1.003 1.003 0 0 1 8 12V6.41l-3.71-3.7A1.003 1.003 0 0 1 5 1h10c.55 0 1 .45 1 1M5 11.995c-.28 0-.53.11-.71.29l-.29.29V8.998C4 8.449 3.55 8 3 8s-1 .45-1 1v3.585l-.29-.29a1.002 1.002 0 0 0-1.42 1.418l2 1.999c.18.18.43.29.71.29s.53-.11.71-.29l2-1.998c.18-.18.29-.43.29-.71 0-.558-.45-1.008-1-1.008"];
})), Lu, Ru = o((() => {
	Lu = ["M2.99 2.99c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1s1-.45 1-1v-11c0-.55-.45-1-1-1m0-3c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m2 3.03v7.23c2.07-2.11 5.92 1.75 9 0V3.02c-3 2.07-6.94-2.03-9 0"];
})), zu, Bu = o((() => {
	zu = ["M9.217 0q0 2.052 1.104 3.282Q14 6.154 14 9.846 14 13.948 9.585 16c2.165-2.4 1.84-3.385-.368-6.4-2.342 1.2-1.967 2-1.592 3.6-.786 0-1.5 0-1.875-.4 0 .547.898 2 1.464 3.2-2.943-.82-6.092-5.744-4.988-6.154q1.104-.41 2.575.41Q2.962 2.872 9.217 0"];
})), Vu, Hu = o((() => {
	Vu = ["M4 8c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1m4-4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1S7 .45 7 1v2c0 .55.45 1 1 1M3.79 5.21a1.003 1.003 0 0 0 1.42-1.42l-1.5-1.5a1.003 1.003 0 0 0-1.42 1.42zm.71 5.29c-.28 0-.53.11-.71.29l-1.5 1.5a1.003 1.003 0 0 0 1.42 1.42l1.5-1.5a1.003 1.003 0 0 0-.71-1.71m7-5c.28 0 .53-.11.71-.29l1.5-1.5a1.003 1.003 0 0 0-1.42-1.42l-1.5 1.5a1.003 1.003 0 0 0 .71 1.71m.71 5.29a1.003 1.003 0 0 0-1.42 1.42l1.5 1.5a1.003 1.003 0 0 0 1.42-1.42zM15 7h-2c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1s-.45-1-1-1M8 5C6.34 5 5 6.34 5 8s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3m0 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m0 3c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1"];
})), Uu, Wu = o((() => {
	Uu = ["M1 5.326q.411 0 .8-.069.388-.069.697-.228a1.7 1.7 0 0 0 .537-.412q.23-.25.297-.617h1.063v8H2.966V6.354H1zM12.172 4.01q.825 0 1.342.385.528.375.814.968.297.583.396 1.287.11.704.11 1.364t-.11 1.364q-.099.704-.396 1.298-.285.583-.814.968-.517.375-1.342.374-.825 0-1.353-.374a2.74 2.74 0 0 1-.814-.968 4.6 4.6 0 0 1-.396-1.298 10 10 0 0 1-.099-1.364q0-.66.099-1.364.11-.704.396-1.287.297-.594.814-.968.528-.385 1.353-.385m0 6.963q.407 0 .682-.231.274-.242.429-.638.165-.407.231-.946t.066-1.144-.066-1.133a3.7 3.7 0 0 0-.231-.946 1.5 1.5 0 0 0-.429-.638 1 1 0 0 0-.682-.242q-.418 0-.693.242a1.66 1.66 0 0 0-.429.638 4 4 0 0 0-.22.946q-.066.528-.066 1.133t.066 1.144.22.946q.165.396.429.638.274.231.693.231M8.089 10.5H6.5v1.543h1.589z"];
})), Gu, Ku = o((() => {
	Gu = ["m15.71 2.29-2-2A1 1 0 0 0 13 0h-1v6H4V0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V3c0-.28-.11-.53-.29-.71M14 15H2V9c0-.55.45-1 1-1h10c.55 0 1 .45 1 1zM11 1H9v4h2z"];
})), qu, Ju = o((() => {
	qu = ["M10.643 6.595c.22.418.344.894.344 1.399 0 .439-.094.855-.263 1.231l3.265 3.462-.002-1.75a.97.97 0 0 1 .314-.68.99.99 0 0 1 1.388.048c.186.2.316.46.3.715l-.009 4.03a.96.96 0 0 1-.3.68.97.97 0 0 1-.698.266l-4.053.002a.97.97 0 0 1-.679-.314 1.03 1.03 0 0 1 .05-1.42.97.97 0 0 1 .698-.266l1.7-.001-3.305-3.35a2.998 2.998 0 0 1-4.228-1.653H.999a1 1 0 0 1 0-2h4.166a3 3 0 0 1 4.06-1.735l3.449-3.268-1.745.002a.979.979 0 0 1-.631-1.692c.199-.186.459-.316.713-.3l4.025.009c.247.008.493.1.679.3s.274.451.265.7l.002 4.046a.97.97 0 0 1-.313.68 1.03 1.03 0 0 1-1.42-.05.97.97 0 0 1-.266-.7V3.295z"];
})), Yu, Xu = o((() => {
	Yu = ["M9.702 7.31c.176.176.293.41.293.684a.98.98 0 0 1-.283.695q-2.832 2.864-3.011 3.027c-.179.164-.42.284-.693.284a.995.995 0 0 1-.997-.985c0-.274.112-.541.292-.72q.18-.18 1.514-1.293H.98c-.536 0-.975-.47-.975-1.008 0-.537.439-.996.975-.996h5.837Q5.474 5.87 5.303 5.694a1.03 1.03 0 0 1-.292-.705A1 1 0 0 1 6 4c.272 0 .52.108.695.294A536 536 0 0 0 9.702 7.31M13 11.002c-1.657 0-3-1.347-3-3.008a3.004 3.004 0 0 1 3-3.007c1.657 0 3 1.346 3 3.007a3.004 3.004 0 0 1-3 3.008"];
})), Zu, Qu = o((() => {
	Zu = ["M4.16 9.002H.977C.44 9.002 0 8.532 0 7.994c0-.537.44-.99.978-.99h3.18A3.01 3.01 0 0 1 6.995 5a3.01 3.01 0 0 1 2.839 2.004h2.98q-1.347-1.134-1.518-1.31a1.03 1.03 0 0 1-.293-.705c0-.538.454-.989.992-.989a.95.95 0 0 1 .697.294q.177.186 3.014 3.016a.96.96 0 0 1 .293.684.98.98 0 0 1-.284.695l-3.018 3.027a.97.97 0 0 1-.694.284.996.996 0 0 1-.707-1.705l1.518-1.293H9.833A3.01 3.01 0 0 1 6.996 11 3.01 3.01 0 0 1 4.16 9.002"];
})), $u, ed = o((() => {
	$u = ["M5.175 7.004a3 3 0 0 1 2.83-2.001c1.305 0 2.416.835 2.83 2.001h1.985q-1.344-1.134-1.515-1.31a1.03 1.03 0 0 1-.292-.705c0-.538.453-.989.99-.989a.95.95 0 0 1 .696.294q.176.186 3.008 3.016c.176.176.293.41.293.684a.98.98 0 0 1-.283.695l-3.013 3.027a.995.995 0 0 1-1.691-.702c0-.273.116-.544.292-.72l1.515-1.292h-1.98a3 3 0 0 1-2.835 2.016A3 3 0 0 1 5.17 9.002H3.18l1.515 1.292c.176.176.292.447.292.72a.995.995 0 0 1-1.69.702L.282 8.69A.98.98 0 0 1 0 7.994a.96.96 0 0 1 .293-.684A536 536 0 0 0 3.3 4.294.95.95 0 0 1 3.997 4a1 1 0 0 1 .99.989c0 .273-.12.528-.292.705q-.172.176-1.515 1.31z"];
})), td, nd = o((() => {
	td = ["M10.392 10.647A3.002 3.002 0 0 1 6.16 8.995H3.37l1.338 1.318c.172.178.287.41.282.683-.01.536-.524.995-.99.995s-.63-.187-.747-.294L.281 8.682A.96.96 0 0 1 0 7.994a.97.97 0 0 1 .294-.687l3.01-3.028a.97.97 0 0 1 .697-.27c.536.01.998.485.989 1.021a.97.97 0 0 1-.295.687L3.37 6.997h2.79a3 3 0 0 1 4.106-1.716l2.416-2.277-1.732.004a1 1 0 0 1-.679-.329.98.98 0 0 1 .05-1.378c.199-.186.459-.315.714-.3l4.012.005a.96.96 0 0 1 .944.999L15.99 6.05a.97.97 0 0 1-.314.679 1.03 1.03 0 0 1-1.421-.048.97.97 0 0 1-.265-.699V4.29l-2.34 2.312c.219.416.343.89.343 1.394 0 .451-.1.88-.279 1.263L14 11.68l-.004-1.73a.98.98 0 0 1 .323-.68.98.98 0 0 1 1.378.049c.187.2.316.46.3.714l-.004 4.011a.98.98 0 0 1-.3.691.97.97 0 0 1-.7.265l-4.046-.001a1 1 0 0 1-.679-.326 1.017 1.017 0 0 1 .048-1.41.97.97 0 0 1 .699-.265h1.693z"];
})), rd, id = o((() => {
	rd = ["M13.5 6a2.5 2.5 0 0 0-2.45 2h-1.3L5.74 4l-.75.75L8.25 8h-3.3a2.5 2.5 0 1 0 0 1h3.3l-3.26 3.25.75.75 4.01-4h1.3a2.5 2.5 0 1 0 2.45-3"];
})), ad, od = o((() => {
	ad = ["M-.01 14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V7h-16zm15-10H7.41L5.7 2.3a.97.97 0 0 0-.71-.3h-4c-.55 0-1 .45-1 1v3h16V5c0-.55-.45-1-1-1"];
})), sd, cd = o((() => {
	sd = ["M10.165 7a3 3 0 0 0 2.827 2 3 3 0 0 0 2.827-2H16v7c0 .55-.45 1-1 1H1.01c-.55 0-1-.45-1-1V7zM8.76 6H0V3c0-.55.45-1 1-1h1.998c.28 0 .53.11.71.29L5.417 4h2.578c0 .768.29 1.469.765 2m6.23-3c.55 0 1 .45 1 1s-.45 1-1 1h-.999v1c0 .55-.45 1-1 1-.549 0-.998-.45-.998-1V5h-1c-.55 0-1-.45-1-1s.45-1 1-1h1V2c0-.55.45-1 .999-1 .55 0 1 .45 1 1v1z"];
})), ld, ud = o((() => {
	ld = ["M2.06 6.69c.14-.4.5-.69.94-.69h11V5c0-.55-.45-1-1-1H6.41l-1.7-1.71A1 1 0 0 0 4 2H1c-.55 0-1 .45-1 1v9.84l2.05-6.15zM16 8c0-.55-.45-1-1-1H4a.99.99 0 0 0-.94.69l-2 6c-.04.09-.06.2-.06.31 0 .55.45 1 1 1h11c.44 0 .81-.29.94-.69l2-6c.04-.09.06-.2.06-.31"];
})), dd, fd = o((() => {
	dd = ["M8.76 5.98c-.47-.53-.77-1.22-.77-1.99h-.58L5.7 2.29a.97.97 0 0 0-.71-.3h-4c-.55 0-1 .45-1 1v3h8.76zm6.23-2.99h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59l-3.3 3.3a1 1 0 0 0-.29.7 1.003 1.003 0 0 0 1.71.71l3.29-3.29V8c0 .55.45 1 1 1s1-.45 1-1V4c0-.56-.45-1.01-1-1.01m-1.98 7.23-.9.9-.01-.01c-.54.55-1.28.89-2.11.89-1.66 0-3-1.34-3-3 0-.77.3-1.47.78-2H-.01v7c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-3.18c-.31.11-.65.18-1 .18-.76-.01-1.45-.31-1.98-.78"];
})), pd, md = o((() => {
	pd = ["m13.02 10.22-.9.9-.01-.01c-.54.55-1.28.89-2.11.89-1.66 0-3-1.34-3-3 0-.77.3-1.47.78-2H4a.99.99 0 0 0-.94.69l-2 6c-.04.09-.06.2-.06.31 0 .55.45 1 1 1h11c.44 0 .81-.29.94-.69l1.11-3.32c-.01 0-.03.01-.05.01-.77 0-1.45-.3-1.98-.78M2.06 6.69c.14-.4.5-.69.94-.69h5.76l.01-.01C8.3 5.46 8 4.77 8 4H6.41l-1.7-1.71A1 1 0 0 0 4 2H1c-.55 0-1 .45-1 1v9.84l2.05-6.15zM15 3h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59l-3.3 3.29a1.003 1.003 0 0 0 1.42 1.42L14 6.41V8c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1"];
})), hd, gd = o((() => {
	hd = ["M9.37 12.69c-1.2-.53-1.04-.85-1.08-1.29-.01-.06-.01-.12-.01-.19.41-.37.75-.87.97-1.44 0 0 .01-.03.01-.04q.075-.195.12-.39c.28-.06.44-.36.5-.63.06-.11.19-.39.16-.7-.04-.4-.2-.59-.38-.67v-.07c0-.52-.05-1.26-.14-1.74a3 3 0 0 0-.09-.43 3 3 0 0 0-1.04-1.51C7.87 3.2 7.15 3 6.5 3c-.64 0-1.36.2-1.87.59-.5.38-.87.92-1.05 1.51-.04.13-.07.27-.09.4-.09.49-.14 1.24-.14 1.75v.06c-.19.07-.36.26-.4.68-.03.31.1.59.16.7.06.28.23.59.51.64.04.14.08.27.13.39 0 .01.01.02.01.02v.01c.22.59.57 1.1.99 1.46 0 .06-.01.12-.01.17-.04.44.08.76-1.12 1.29S.61 13.77.24 14.62C-.13 15.5.02 16 .02 16h12.96s.15-.5-.22-1.36c-.38-.85-2.19-1.42-3.39-1.95m6.33-10.4-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H9.99c-.55 0-1 .45-1 1s.45 1 1 1h2.58l-.29.29a1.003 1.003 0 0 0 1.42 1.42l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), _d, vd = o((() => {
	_d = ["M9.37 12.69c-1.2-.53-1.04-.85-1.08-1.29-.01-.06-.01-.12-.01-.19.41-.37.75-.87.97-1.44 0 0 .01-.03.01-.04q.075-.195.12-.39c.28-.06.44-.36.5-.63.06-.11.19-.39.16-.7-.04-.4-.2-.59-.38-.67v-.07c0-.52-.05-1.26-.14-1.74a3 3 0 0 0-.09-.43 3 3 0 0 0-1.04-1.51C7.87 3.2 7.15 3 6.5 3c-.64 0-1.36.2-1.87.59-.5.38-.87.92-1.05 1.51-.04.13-.07.27-.09.4-.09.49-.14 1.24-.14 1.75v.06c-.19.07-.36.26-.4.68-.03.31.1.59.16.7.06.28.23.59.51.64.04.14.08.27.13.39 0 .01.01.02.01.02v.01c.22.59.57 1.1.99 1.46 0 .06-.01.12-.01.17-.04.44.08.76-1.12 1.29S.61 13.77.24 14.62C-.13 15.5.02 16 .02 16h12.96s.15-.5-.22-1.36c-.38-.85-2.19-1.42-3.39-1.95M14.99 2h-2.58l.29-.29A1.003 1.003 0 0 0 11.28.29l-2 2c-.17.18-.29.43-.29.71s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L12.41 4h2.58c.55 0 1-.45 1-1s-.45-1-1-1"];
})), yd, bd = o((() => {
	yd = ["M8 2a1 1 0 0 1 .928.629l3.992 9.979q.079.182.08.392a1 1 0 0 1-1.937.35l-.94-2.35H5.877l-.94 2.35a1 1 0 1 1-1.857-.742l3.992-9.98A1 1 0 0 1 8 2M6.677 9h2.646L8 5.693z"];
})), xd, Sd = o((() => {
	xd = ["M13.7 9.29a1.003 1.003 0 0 0-1.42 1.42l.29.29H11.4l-5-5h6.17l-.29.29a1.003 1.003 0 0 0 1.42 1.42l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l.29.29H.99c-.55 0-1 .45-1 1s.45 1 1 1h2.59l6.71 6.71c.18.18.43.29.71.29h1.59l-.29.29a1.003 1.003 0 0 0 1.42 1.42l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71z"];
})), Cd, wd = o((() => {
	Cd = ["M12.293 2.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 .25.414l.015.062q.027.111.028.231a1 1 0 0 1-.209.608 1 1 0 0 1-.084.099l-2 2a1 1 0 1 1-1.414-1.414L12.586 6h-1.172l-6.707 6.707a1 1 0 0 1-.297.203l-.026.012-.052.02-.04.014-.062.016-.034.008-.031.004q-.03.007-.062.011L4 13H1a1 1 0 0 1 0-2h2.586l5-5H1a1 1 0 0 1 0-2h11.586l-.293-.293a1 1 0 0 1 0-1.414"];
})), Td, Ed = o((() => {
	Td = ["M2 11v2h2v-2zM1 9h4c.55 0 1 .45 1 1v4c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1v-4c0-.55.45-1 1-1m9-6h5c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1M6 1a1.003 1.003 0 0 1 .71 1.71l-3 4C3.53 6.89 3.28 7 3 7s-.53-.11-.71-.29l-2-2a1.003 1.003 0 0 1 1.42-1.42L3 4.59l2.29-3.3C5.47 1.11 5.72 1 6 1m4 10h5c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1"];
})), Dd, Od = o((() => {
	Dd = ["M8.002 16a6.8 6.8 0 0 1-2.732-.556 7.1 7.1 0 0 1-2.221-1.509 7.2 7.2 0 0 1-1.498-2.237A6.9 6.9 0 0 1 1 8.947q0-1.468.551-2.748a7.1 7.1 0 0 1 1.503-2.234 7.2 7.2 0 0 1 2.225-1.51A6.8 6.8 0 0 1 8.01 1.9h.111l-.47-.474a.8.8 0 0 1-.244-.583q0-.339.233-.583A.8.8 0 0 1 8.228 0a.78.78 0 0 1 .588.24l1.93 1.945a.97.97 0 0 1 .294.7q0 .402-.294.697l-1.93 1.946a.78.78 0 0 1-.588.24.8.8 0 0 1-.588-.249.82.82 0 0 1-.238-.578.78.78 0 0 1 .238-.577l.491-.496h-.12q-2.105 0-3.581 1.478T2.954 8.944t1.469 3.604Q5.89 14.031 8 14.031t3.577-1.478q1.47-1.477 1.47-3.598 0-.41.284-.698a.94.94 0 0 1 .692-.287q.407 0 .692.287t.285.698q0 1.455-.551 2.741a7.1 7.1 0 0 1-1.498 2.239 7.1 7.1 0 0 1-2.219 1.51 6.75 6.75 0 0 1-2.73.555M9 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1m1 1H9v3h1zm-5-.5a.5.5 0 0 1 .5-.5H6a1 1 0 0 1 1 1v3.5a.5.5 0 0 1-1 0V8h-.5a.5.5 0 0 1-.5-.5"];
})), kd, Ad = o((() => {
	kd = ["m12.21 7.29-2.5-2.5a1.003 1.003 0 0 0-1.42 1.42l.8.79H4.5c-.55 0-1 .45-1 1s.45 1 1 1h4.59l-.79.79c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2.5-2.5c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M13 14h3v2h-3c-1.1 0-2-.9-2-2v-2.67l1.92-1.91c.03-.03.05-.06.08-.09zm3-12h-3v4.67c-.03-.03-.05-.06-.08-.09L11 4.67V2c0-1.1.9-2 2-2h3zM3 9.32c.37.41.9.68 1.5.68H5v4c0 1.1-.9 2-2 2H0v-2h3zM3 0c1.1 0 2 .9 2 2v4h-.5c-.6 0-1.13.26-1.5.68V2H0V0z"];
})), jd, Md = o((() => {
	jd = ["M1.949 1H0v2h2c.31 0 .6.161.762.426l1.965 3.193-1.352 1.08A1 1 0 0 0 3 8.482V13.9c0 .607.448 1.1 1 1.1h11c.552 0 1-.492 1-1.1V2s0-1-1-1H9c-.5 0-1 .5-1 1v2L6.388 5.29 4.455 2.35A3 3 0 0 0 1.95 1M14 3v1h-4V3z"];
})), Nd, Pd = o((() => {
	Nd = ["M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0"];
})), Fd, Id = o((() => {
	Fd = ["M13 12h1c.55 0 1-.45 1-1V8h-3v3c0 .55.45 1 1 1M10 2c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v3h3zm0 4H7v3h3zm5-4c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v2h3zm0 3h-3v2h3zM5 5H2v3h3zm-2 7h1c.55 0 1-.45 1-1V9H2v2c0 .55.45 1 1 1m12 1H2c-.55 0-1 .45-1 1s.45 1 1 1h13c.55 0 1-.45 1-1s-.45-1-1-1M5 2c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v2h3zm3 10h1c.55 0 1-.45 1-1v-1H7v1c0 .55.45 1 1 1"];
})), Ld, Rd = o((() => {
	Ld = ["M3.41 2H5c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v4c0 .55.45 1 1 1s1-.45 1-1V3.41L5.29 6.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM6 9c-.28 0-.53.11-.71.29L2 12.59V11c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.41l3.29-3.29c.19-.18.3-.43.3-.71 0-.55-.45-1-1-1m9 1c-.55 0-1 .45-1 1v1.59L10.71 9.3A.97.97 0 0 0 10 9a1.003 1.003 0 0 0-.71 1.71l3.3 3.29H11c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1m0-10h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59l-3.3 3.29a1.003 1.003 0 0 0 1.42 1.42L14 3.41V5c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), zd, Bd = o((() => {
	zd = ["M8.12 4.74H6.98c.33-1.29.75-2.24 1.28-2.84.33-.37.64-.56.95-.56.06 0 .11.02.15.05q.06.06.06.15c0 .05-.04.15-.13.29s-.13.28-.13.4c0 .18.07.33.2.46.14.13.31.19.52.19.22 0 .41-.08.56-.23.15-.16.23-.37.23-.63 0-.3-.11-.55-.34-.74S9.74 1 9.24 1c-.78 0-1.49.22-2.12.67-.64.45-1.24 1.2-1.81 2.23-.2.36-.38.59-.56.69s-.46.15-.85.15l-.26.9h1.08l-1.59 6.12c-.27 1.01-.44 1.63-.54 1.86-.14.34-.34.63-.62.87-.11.1-.24.15-.4.15a.15.15 0 0 1-.11-.04l-.04-.05c0-.03.04-.08.12-.16q.12-.12.12-.36c0-.18-.06-.33-.19-.44q-.18-.18-.54-.18c-.28 0-.51.08-.68.23-.16.14-.25.32-.25.53 0 .22.1.42.31.59s.53.25.97.25c.7 0 1.32-.18 1.87-.54.54-.36 1.02-.92 1.42-1.67.41-.75.82-1.96 1.25-3.63l.91-3.54h1.1zm5.43 1.52c.2-.15.41-.23.62-.23q.12 0 .45.09t.57.09c.23 0 .42-.08.57-.23.16-.16.24-.36.24-.61 0-.26-.08-.47-.23-.62s-.37-.23-.66-.23c-.25 0-.5.06-.72.18-.23.12-.51.38-.86.78-.26.3-.64.81-1.15 1.55-.2-.91-.55-1.75-1.05-2.51l-2.72.46-.06.29q.3-.06.51-.06c.27 0 .49.11.67.34.28.36.67 1.45 1.17 3.26-.39.52-.66.85-.8 1.01-.24.26-.44.42-.59.5-.12.06-.25.09-.41.09-.11 0-.3-.06-.56-.18q-.27-.12-.48-.12c-.27 0-.48.08-.66.25-.17.17-.26.38-.26.64 0 .25.08.44.24.6.16.15.37.23.64.23.26 0 .5-.05.73-.16s.52-.34.86-.69c.35-.35.82-.9 1.43-1.67.23.73.44 1.25.61 1.58s.37.57.59.71c.22.15.5.22.83.22.32 0 .65-.11.98-.34.44-.3.88-.81 1.34-1.53l-.26-.15c-.31.43-.54.7-.69.8-.1.07-.22.1-.35.1q-.24 0-.48-.3c-.27-.34-.62-1.27-1.06-2.8.4-.68.73-1.13 1-1.34"];
})), Vd, Hd = o((() => {
	Vd = ["M12.5 1a1 1 0 1 1 0 2h-1.831a1 1 0 0 0-.983.821L9.335 6H11a1 1 0 1 1 0 2H9.013l-.727 4.517-.004.02A3 3 0 0 1 5.332 15H4a1 1 0 1 1 0-2h1.331a1 1 0 0 0 .983-.821L6.987 8H5a1 1 0 0 1 0-2h2.309l.405-2.517.004-.02a3 3 0 0 1 2.95-2.462z"];
})), Ud, Wd = o((() => {
	Ud = ["M10 10c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1h-4c-.55 0-1 .45-1 1M6 7c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1m9 5H2V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M4 5h3c.55 0 1-.45 1-1s-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1"];
})), Gd, Kd = o((() => {
	Gd = ["M7 11a1 1 0 0 0-1-1H4.8a.8.8 0 0 1-.706-1.176L8.588.397A.75.75 0 0 1 10 .75V5a1 1 0 0 0 1 1h1.2a.8.8 0 0 1 .706 1.176l-4.494 8.427A.75.75 0 0 1 7 15.25z"];
})), qd, Jd = o((() => {
	qd = ["M6 9c.55 0 1 .45 1 1v4c0 .55-.45 1-1 1s-1-.45-1-1v-1.59l-3.29 3.3A1.003 1.003 0 0 1 0 15c0-.28.11-.53.3-.71L3.59 11H2c-.55 0-1-.45-1-1s.45-1 1-1ZM9.088.004l.097.013.097.024.057.018.1.042.054.029.095.061.052.04 6 5 .05.046.076.08.053.07.06.095.051.11a1 1 0 0 1 .067.446l-.014.105-.037.143-.035.087-.043.083-4 7-.034.056-.059.08-.038.044-.096.092-.114.082-.116.062-.086.034-.109.03-.1.017-.069.006H8.83q.133-.376.163-.79L9 13v-3a3 3 0 0 0-2.824-2.995L6 7H3c-.351 0-.689.06-1.002.171L2 5l.002-.07.013-.1.015-.073.025-.085.043-.104.056-.101.045-.066.079-.093.084-.078.083-.062 6-4 .07-.043.12-.056.111-.036.108-.022.083-.01h.031a1 1 0 0 1 .12.003"];
})), Yd, Xd = o((() => {
	Yd = ["m-.01 6.66 7.34 2 2 7.33 6.66-16z"];
})), Zd, Qd = o((() => {
	Zd = ["M8.82 12.4h.66c.23 0 .36-.17.36-.4v-1.48l.19-.18c-.27.03-.55.06-.83.06s-.56-.03-.84-.07c.02.04.05.08.07.13V12c0 .23.15.4.39.4M6.4 15.1A5.51 5.51 0 0 1 .9 9.6c0-.49.06-.98.18-1.43.03 0 .05-.01.08-.01h.08v.44c0 .19.17.34.36.34.03 0 .07-.01.1-.01l.71.7c.07.07.19.07.26 0s.07-.19 0-.26l-.7-.72c0-.02.03-.03.03-.05v-.11c0-.15.08-.2.23-.33h.42c.08 0 .15-.01.22-.04h.02c.02-.02.03-.02.04-.04.01-.01.01-.01.02-.01l.02-.01.9-.9c-.13-.26-.24-.52-.34-.8h-.5v-.43c0-.01.05.05.04-.08h.31c-.03-.13-.06-.26-.08-.39h-.57c.16-.12.34-.24.51-.36-.02-.23-.04-.46-.04-.7 0-.12.01-.23.02-.34A6.39 6.39 0 0 0 0 9.6C0 13.13 2.87 16 6.4 16c3.1 0 5.67-2.22 6.26-5.15l-.78-.88c-.21 2.85-2.58 5.13-5.48 5.13m-1.7-2.93v-.28h.12c.23 0 .39-.19.39-.42v-.54s.01-.01 0-.01L3.77 9.45h-.62c-.23 0-.38.19-.38.42v1.6c0 .23.14.42.38.42h.26v1.61c0 .23.22.41.45.41s.45-.18.45-.41v-.97H4.3c.24 0 .4-.13.4-.36m11.07-2.34-2.94-2.94c.11-.17.21-.34.3-.52.01-.03.03-.06.04-.09.08-.18.16-.36.22-.55v-.01c.06-.19.1-.38.14-.58.01-.05.01-.09.02-.14.03-.2.05-.4.05-.61a4.4 4.4 0 0 0-4.4-4.4C6.77 0 4.8 1.97 4.8 4.4s1.97 4.4 4.4 4.4c.21 0 .41-.02.61-.05.04 0 .09-.01.14-.02.2-.03.39-.08.58-.14h.01c.19-.06.37-.14.55-.22.03-.01.06-.03.09-.04.18-.09.35-.19.52-.3l2.94 2.94a.8.8 0 0 0 .57.23c.44 0 .8-.36.8-.8a.9.9 0 0 0-.24-.57M9.2 7.6C7.43 7.6 6 6.17 6 4.4s1.43-3.2 3.2-3.2 3.2 1.43 3.2 3.2-1.43 3.2-3.2 3.2m1.54 4.26v-.52c0-.09-.1-.17-.19-.17s-.19.07-.19.17v.52c0 .09.1.17.19.17s.19-.07.19-.17"];
})), $d, ef = o((() => {
	$d = ["M12.444 6C10.544 6 9 7.494 9 9.331 9 11.175 12.444 16 12.444 16s3.443-4.825 3.443-6.669C15.881 7.494 14.345 6 12.445 6m.056 5a1.5 1.5 0 1 1 .001-3.001A1.5 1.5 0 0 1 12.5 11M0 6c0-3.315 2.685-6 6-6a6 6 0 0 1 5.923 5.036 4.6 4.6 0 0 0-1.454.433A4.505 4.505 0 0 0 6 1.5 4.504 4.504 0 0 0 1.5 6a4.504 4.504 0 0 0 6.58 3.99c.093.425.265.913.488 1.435A6 6 0 0 1 6 12c-3.315 0-6-2.685-6-6m6.75-2.25v1.943l1.283 1.275a.752.752 0 0 1-1.065 1.065l-1.5-1.5A.75.75 0 0 1 5.25 6V3.75c0-.412.338-.75.75-.75s.75.338.75.75"];
})), tf, nf = o((() => {
	tf = ["M6.788.915A3.121 3.121 0 0 0 1.801 4.54H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-.8A3.122 3.122 0 0 0 9.211.915l-1 .999q-.11.11-.212.23a4 4 0 0 0-.213-.23zm5.424 3-.626.626H9.02a2.14 2.14 0 0 1 .606-1.213l.999-1a1.121 1.121 0 1 1 1.586 1.587m-5.233.626H4.414l-.626-.626a1.121 1.121 0 1 1 1.586-1.586l1 1c.329.329.54.755.605 1.212M6 9.54H1v5a1 1 0 0 0 1 1h4zm9 0h-5v6h4a1 1 0 0 0 1-1zm-8 0h2v6H7z"];
})), rf, af = o((() => {
	rf = ["M12 1c-1.66 0-3 1.34-3 3 0 1.25.76 2.32 1.85 2.77A2.02 2.02 0 0 1 9 8H7c-.73 0-1.41.2-2 .55V5.82C6.16 5.4 7 4.3 7 3c0-1.66-1.34-3-3-3S1 1.34 1 3c0 1.3.84 2.4 2 2.82v4.37c-1.16.4-2 1.51-2 2.81 0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.04-.53-1.95-1.32-2.49.35-.31.81-.51 1.32-.51h2c1.92 0 3.52-1.35 3.91-3.15A2.996 2.996 0 0 0 12 1M4 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 12c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m8-9c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), of, sf = o((() => {
	of = ["M15 7h-3.14c-.45-1.72-2-3-3.86-3S4.59 5.28 4.14 7H1c-.55 0-1 .45-1 1s.45 1 1 1h3.14c.45 1.72 2 3 3.86 3s3.41-1.28 3.86-3H15c.55 0 1-.45 1-1s-.45-1-1-1m-7 3c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2"];
})), cf, lf = o((() => {
	cf = ["M12 6c-1.3 0-2.4.84-2.82 2H9c-1.62 0-3-.96-3.63-2.34C6.33 5.16 7 4.16 7 3c0-1.66-1.34-3-3-3S1 1.34 1 3c0 1.3.84 2.4 2 2.81v4.37C1.84 10.6 1 11.7 1 13c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.3-.84-2.4-2-2.82V8.43A5.9 5.9 0 0 0 9 10h.18A2.996 2.996 0 0 0 15 9c0-1.66-1.34-3-3-3m-8 8c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M4 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m8 6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), uf, df = o((() => {
	uf = ["M14 2h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1m-3.18 4.8C10.51 7.51 9.82 8 9 8H7c-.73 0-1.41.2-2 .55V5.82C6.16 5.4 7 4.3 7 3c0-1.66-1.34-3-3-3S1 1.34 1 3c0 1.3.84 2.4 2 2.82v4.37c-1.16.4-2 1.51-2 2.81 0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.04-.53-1.95-1.32-2.49.35-.31.81-.51 1.32-.51h2c1.9 0 3.49-1.33 3.89-3.11-.29.07-.58.11-.89.11-.41 0-.8-.08-1.18-.2M4 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 12c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), ff, pf = o((() => {
	ff = ["M3 1C1.34 1 0 2.34 0 4c0 1.3.84 2.4 2 2.82v3.37C.84 10.6 0 11.7 0 13c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.3-.84-2.4-2-2.82V6.82C5.16 6.4 6 5.3 6 4c0-1.66-1.34-3-3-3m0 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m0-9c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m11 5.18V6c0-1.66-1.34-3-3-3H9.41l1.29-1.29c.19-.18.3-.43.3-.71A1.003 1.003 0 0 0 9.29.29l-3 3C6.11 3.47 6 3.72 6 4s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L9.41 5H11c.55 0 1 .45 1 1v4.18A2.996 2.996 0 0 0 13 16c1.66 0 3-1.34 3-3 0-1.3-.84-2.4-2-2.82M13 14c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), mf, hf = o((() => {
	mf = ["M4 6h1V5H4zm9 3c0-.28-.11-.53-.29-.71l-3-3C9.53 5.11 9.28 5 9 5s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L8 8.41V15c0 .55.45 1 1 1s1-.45 1-1V8.41l1.29 1.29c.18.19.43.3.71.3.55 0 1-.45 1-1M5 3H4v1h1zm10-3H1C.45 0 0 .45 0 1v13c0 .55.45 1 1 1h5v-2H2v-1h4v-1H3V2h11v9h-2v1h2v1h-2v2h3c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), gf, _f = o((() => {
	gf = ["M3 1a2.998 2.998 0 0 1 1 5.825V10c0 .51.159.705.266.794.139.116.383.206.734.206h1.586l-.793-.793a1 1 0 0 1 1.414-1.414l2.5 2.5.064.071a1 1 0 0 1 .205.415l.014.083q.007.045.009.09v.096l-.006.052a1 1 0 0 1-.181.482l-.037.049-.068.076-2.5 2.5a1 1 0 0 1-1.414-1.414L6.586 13H5c-.649 0-1.405-.16-2.016-.669C2.341 11.795 2 10.991 2 10V6.825A2.998 2.998 0 0 1 3 1M8.793.793a1 1 0 1 1 1.414 1.414L9.414 3H11c.649 0 1.405.16 2.016.669.643.536.984 1.34.984 2.331v3.174A2.998 2.998 0 0 1 13 15a3 3 0 0 1-1-5.826V6c0-.51-.159-.705-.266-.794C11.595 5.09 11.351 5 11 5H9.414l.793.793a1 1 0 1 1-1.414 1.414l-2.5-2.5a1 1 0 0 1-.287-.607L6 4.048V3.95q.002-.045.009-.089l.014-.083a1 1 0 0 1 .204-.416l.065-.07zM13 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2M3 3a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), vf, yf = o((() => {
	vf = ["M5 9H4v1h1zm10-9H1C.45 0 0 .45 0 1v13c0 .55.45 1 1 1h3v1l2-1 2 1v-1h7c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M4 13H2v-1h2zm10 0H8v-1h6zm0-2H3V2h11zM5 3H4v1h1zm0 4H4v1h1zm0-2H4v1h1z"];
})), bf, xf = o((() => {
	bf = ["M2 0v4c0 2.97 2.16 5.43 5 5.91V14H5c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1H9V9.91c2.84-.48 5-2.94 5-5.91V0z"];
})), Sf, Cf = o((() => {
	Sf = ["M4.45 7.83c-.26 0-.41.21-.41.46v1.75c0 .26.16.46.41.46h.29v1.77c0 .25.24.45.49.45s.49-.2.49-.45V11.2h-.01c.26 0 .44-.14.44-.4v-.3h.14c.26 0 .43-.2.43-.46v-.59s.01-.01 0-.01l-1.58-1.6h-.69zM8.51 3.9h.22c.06 0 .12-.01.12-.07s-.05-.07-.12-.07h-.22c-.06 0-.12.01-.12.07.01.06.06.07.12.07m-2.33-.05c.07-.07.07-.19 0-.26l-.5-.5a.187.187 0 0 0-.26 0c-.07.07-.07.19 0 .26l.5.5c.07.07.19.07.26 0m3.06.89c.07 0 .14-.06.14-.12v-.31c0-.07-.07-.12-.14-.12s-.14.06-.14.12v.31c0 .07.07.12.14.12M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6 0-.55.1-1.07.23-1.57h.11v.47c0 .2.18.37.39.37.03 0 .08-.01.11-.02l.78.77c.08.08.2.08.28 0s.08-.2 0-.28l-.75-.78c0-.02.04-.04.04-.06v-.12c0-.16.09-.22.25-.36h.46c.09 0 .17-.01.24-.05h.02c.02-.01.03-.02.05-.03.01-.01.01-.01.02-.01l.02-.02 1.59-1.58c.18-.18.18-.46 0-.64s-.47-.15-.65.03l-.3.34h-.57v-.48c0-.01.05.05.05-.09h.64c.12 0 .22-.09.22-.21s-.1-.21-.22-.21H4.1c.18-.15.34-.31.54-.44l.01-.01c.21-.14.45-.25.68-.37.15-.07.29-.15.44-.21.17-.07.35-.11.53-.17.18-.05.35-.12.53-.16a6.05 6.05 0 0 1 3.47.35c.05.02.1.05.16.08.25.11.48.24.71.39.25.16.49.34.71.55H10.6s0-.03-.01-.03c-.04 0-.09 0-.13.03l-.51.51a.17.17 0 0 0 0 .23c.06.06.17.06.23 0l.42-.44.01-.02h.25c0 .14-.07.09-.07.12v.07c0 .22-.15.37-.36.37h-.38c-.19 0-.38.21-.38.4v.17h-.1c-.12 0-.2.06-.2.18v.25h-.23c-.17 0-.3.11-.3.28s.13.26.3.26c.07 0 .14.03.19-.11l.04.01.49-.46h.17l.39.37c.03.03.08.02.12-.01.03-.03.03-.12 0-.15l-.32-.35h.23l.09.12c.18.18.48.17.66-.01l.09-.1h.4c.02 0 .08.05.08.05v.24l-.05-.01h-.36c-.11 0-.21.1-.21.21s.09.21.21.21h.41v.15c-.14.21-.24.42-.45.42h-.94v-.01l-.44-.44a.47.47 0 0 0-.66 0l-.42.43v.01H8.6c-.26 0-.49.21-.49.46v.92c0 .26.23.45.49.45h.9c.34.14.57.35.72.69v1.68c0 .26.17.44.42.44h.72c.26 0 .4-.18.4-.44V9l.89-.86.03-.02.02-.01h.03c.07-.08.15-.19.15-.31v-.91c0-.18-.16-.32-.31-.46H13c.01.28.21.42.46.42h.42c.08.37.12.76.12 1.15 0 3.31-2.69 6-6 6m4.54-4.27c-.1 0-.21.08-.21.18v.57c0 .1.11.18.21.18s.21-.08.21-.18v-.57c0-.1-.11-.18-.21-.18M8.37 3.19c0-.25-.2-.42-.46-.42h-.54c-.25 0-.42.18-.42.43 0 .03-.1.04.05.08v.47c0 .15.06.27.21.27s.21-.12.21-.27v-.14h.5c.24 0 .45-.16.45-.42"];
})), wf, Tf = o((() => {
	wf = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m5.17 5h-2.44c-.21-1.11-.51-2.03-.91-2.69 1.43.46 2.61 1.43 3.35 2.69M10 8c0 .73-.05 1.39-.12 2H6.12C6.05 9.39 6 8.73 6 8s.05-1.39.12-2h3.76c.07.61.12 1.27.12 2M8 2c.67 0 1.36 1.1 1.73 3H6.27C6.64 3.1 7.33 2 8 2m-1.82.31c-.4.66-.71 1.58-.91 2.69H2.83a6.03 6.03 0 0 1 3.35-2.69M2 8c0-.7.13-1.37.35-2h2.76C5.04 6.62 5 7.28 5 8s.04 1.38.11 2H2.35C2.13 9.37 2 8.7 2 8m.83 3h2.44c.21 1.11.51 2.03.91 2.69A6.03 6.03 0 0 1 2.83 11M8 14c-.67 0-1.36-1.1-1.73-3h3.46c-.37 1.9-1.06 3-1.73 3m1.82-.31c.4-.66.7-1.58.91-2.69h2.44a6.03 6.03 0 0 1-3.35 2.69M13.65 10h-2.76c.07-.62.11-1.28.11-2s-.04-1.38-.11-2h2.76c.22.63.35 1.3.35 2s-.13 1.37-.35 2"];
})), Ef, Df = o((() => {
	Ef = ["M6.693 5a2.4 2.4 0 0 0 .767 1H6.12C6.05 6.61 6 7.27 6 8s.05 1.39.12 2h3.76a18 18 0 0 0 .111-1.472 2.4 2.4 0 0 0 .964.76q-.026.365-.065.712h2.76c.159-.454.27-.93.32-1.422A2.53 2.53 0 0 0 14.5 7v-.5h.5c.28 0 .563-.042.834-.131q.165.79.166 1.631c0 4.42-3.58 8-8 8s-8-3.58-8-8A7.998 7.998 0 0 1 9.631.166 2.7 2.7 0 0 0 9.5 1v.5H9C7.476 1.5 6.5 2.77 6.5 4v.048q-.13.435-.23.952zM5.27 5c.2-1.11.51-2.03.91-2.69A6.03 6.03 0 0 0 2.83 5zM2.35 6C2.13 6.63 2 7.3 2 8s.13 1.37.35 2h2.76C5.04 9.38 5 8.72 5 8s.04-1.38.11-2zm2.92 5H2.83a6.03 6.03 0 0 0 3.35 2.69c-.4-.66-.7-1.58-.91-2.69m1 0c.37 1.9 1.06 3 1.73 3s1.36-1.1 1.73-3zm4.46 0c-.21 1.11-.51 2.03-.91 2.69A6.03 6.03 0 0 0 13.17 11zM9 5c-.6 0-1-.4-1-1 0-.5.4-1 1-1h2V1c0-.6.4-1 1-1s1 .4 1 1v2h2c.6 0 1 .4 1 1s-.4 1-1 1h-2v2c0 .6-.4 1-1 1s-1-.4-1-1V5z"];
})), Of, kf = o((() => {
	Of = ["M14 3c-1.06 0-1.92.83-1.99 1.88l-1.93.97A2.95 2.95 0 0 0 8 5c-.56 0-1.08.16-1.52.43L3.97 3.34C3.98 3.23 4 3.12 4 3c0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.24 0 .47-.05.68-.13l2.51 2.09C5.08 7.29 5 7.63 5 8c0 .96.46 1.81 1.16 2.35l-.56 1.69c-.91.19-1.6.99-1.6 1.96 0 1.1.9 2 2 2s2-.9 2-2c0-.51-.2-.97-.51-1.32l.56-1.69A2.99 2.99 0 0 0 11 8c0-.12-.02-.24-.04-.36l1.94-.97c.32.21.69.33 1.1.33 1.1 0 2-.9 2-2s-.9-2-2-2"];
})), Af, jf = o((() => {
	Af = ["m12.89 8.11-.01.01-.38-.38-.38.38-.02-.02c-.54.55-1.27.9-2.1.9-1.66 0-3-1.34-3-3 0-.83.35-1.56.9-2.1l-.02-.02.38-.38-.38-.38.01-.01C7.35 2.57 7 1.83 7 1c0-.34.07-.65.17-.96A8.004 8.004 0 0 0 0 8c0 4.42 3.58 8 8 8 4.14 0 7.54-3.14 7.96-7.17-.31.1-.62.17-.96.17-.83 0-1.57-.35-2.11-.89m1.02-4.61 1.79-1.79c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-1.79 1.8L10.71.3A.97.97 0 0 0 10 0a1.003 1.003 0 0 0-.71 1.71l1.79 1.79-1.79 1.79a1.003 1.003 0 0 0 1.42 1.42l1.79-1.79 1.79 1.79a1.003 1.003 0 0 0 1.42-1.42z"];
})), Mf, Nf = o((() => {
	Mf = ["M2.713 5.958a1 1 0 0 1 .574-1.916l10 3c.95.285.95 1.63 0 1.916l-10 3a1 1 0 0 1-.574-1.916L9.52 8z"];
})), Pf, Ff = o((() => {
	Pf = ["M2.713 3.958a1 1 0 0 1 .574-1.916l10 3c.95.285.95 1.63 0 1.916l-10 3a1 1 0 0 1-.574-1.916L9.52 6zM3 12h10a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2"];
})), If, Lf = o((() => {
	If = ["M15 9c.55 0 1-.45 1-1s-.45-1-1-1h-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1H9V1c0-.55-.45-1-1-1S7 .45 7 1v1H4V1c0-.55-.45-1-1-1S2 .45 2 1v1H1c-.55 0-1 .45-1 1s.45 1 1 1h1v3H1c-.55 0-1 .45-1 1s.45 1 1 1h1v3H1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1v-1h3v1c0 .55.45 1 1 1s1-.45 1-1v-1h3v1c0 .55.45 1 1 1s1-.45 1-1v-1h1c.55 0 1-.45 1-1s-.45-1-1-1h-1V9zm-8 3H4V9h3zm0-5H4V4h3zm5 5H9V9h3zm0-5H9V4h3z"];
})), Rf, zf = o((() => {
	Rf = ["M0 1v6h7V0H1C.45 0 0 .45 0 1m0 14c0 .55.45 1 1 1h6V9H0zM15 0H9v7h7V1c0-.55-.45-1-1-1M9 16h6c.55 0 1-.45 1-1V9H9z"];
})), Bf, Vf = o((() => {
	Bf = ["M8.602 3.121a1 1 0 0 0 0 1.415l2.828 2.828a1 1 0 0 0 1.415 0l2.828-2.828a1 1 0 0 0 0-1.415L12.845.293a1 1 0 0 0-1.415 0zM0 1.005a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm2 4v-3h3v3zm8 4a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1zm1 2v3h3v-3zm-11-1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm2 4v-3h3v3z"];
})), Hf, Uf = o((() => {
	Hf = ["M5 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6-3H5C2.24 3 0 5.24 0 8s2.24 5 5 5h6c2.76 0 5-2.24 5-5s-2.24-5-5-5m0 9H5c-2.21 0-4-1.79-4-4s1.79-4 4-4h6c2.21 0 4 1.79 4 4s-1.79 4-4 4m0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Wf, Gf = o((() => {
	Wf = ["M10 12c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1s-1 .45-1 1v8c0 .55.45 1 1 1m3 0c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55.45 1 1 1m2 1H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m-9-1c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1s-1 .45-1 1v3c0 .55.45 1 1 1m-3 0c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1v9c0 .55.45 1 1 1"];
})), Kf, qf = o((() => {
	Kf = ["M15 5c0-.55-.45-1-1-1-.41 0-.76.24-.91.59v.01s0 .01-.01.01L11.57 8h-.36l.78-4.84C12 3.11 12 3.05 12 3a1 1 0 0 0-1.99-.16v.01L9.18 8H9V1c0-.55-.45-1-1-1S7 .45 7 1v7h-.09l-.93-5.18A1 1 0 0 0 5 2c-.55 0-1 .45-1 1 0 .05 0 .11.01.16L5.26 11h-.04L2.83 7.44C2.65 7.18 2.35 7 2 7c-.55 0-1 .45-1 1 0 .17.04.33.12.47l3 5.69h.01v.01A5.002 5.002 0 0 0 13 11v-.59l1.93-5.05c.05-.11.07-.23.07-.36"];
})), Jf, Yf = o((() => {
	Jf = ["M14.72 7.87c-1.54-.67-2.99-2.68-3.7-3.95C10.11 1.95 9.93 0 6.14 0 4.05 0 2.71.61 1.92 2.12 1.27 3.36 1 5.21 1 7.83v.79c0 .65.6 1.18 1.35 1.18.34 0 .64-.11.88-.29.17.48.68.84 1.29.84.41 0 .78-.16 1.03-.42.23.37.67.63 1.19.63.57 0 1.05-.31 1.25-.74l.01.63v4.05c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5V7.9c.58.41 1.55 1.21 2.47 1.29 1.57.14 1.82-1.07 1.25-1.32"];
})), Xf, Zf = o((() => {
	Xf = ["M12.08 4.97c-1.26-.71-3.27-2.15-3.95-3.7C7.88.7 6.67.96 6.81 2.52c.09.93.89 1.9 1.3 2.48H1.5C.67 5 0 5.67 0 6.5S.67 8 1.5 8h4.05l.63.01c-.44.2-.75.69-.75 1.25 0 .52.26.96.63 1.19-.26.25-.42.61-.42 1.03 0 .61.35 1.12.84 1.29-.18.24-.29.54-.29.88 0 .75.54 1.35 1.19 1.35h.79c2.62 0 4.47-.28 5.71-.92 1.51-.79 2.12-2.14 2.12-4.22 0-3.79-1.95-3.97-3.92-4.89"];
})), Qf, $f = o((() => {
	Qf = ["M14.5 5H7.89c.41-.58 1.21-1.55 1.3-2.47C9.34.97 8.12.71 7.87 1.28c-.67 1.54-2.68 2.99-3.95 3.7C1.95 5.89 0 6.07 0 9.86c0 2.09.61 3.43 2.12 4.22 1.24.65 3.09.92 5.71.92h.79c.65 0 1.18-.6 1.18-1.35 0-.34-.11-.64-.29-.88.48-.17.84-.68.84-1.29 0-.41-.16-.78-.42-1.03.37-.23.63-.67.63-1.19 0-.57-.31-1.05-.74-1.25l.63-.01h4.05c.83 0 1.5-.67 1.5-1.5S15.33 5 14.5 5"];
})), ep, tp = o((() => {
	ep = ["M13.65 6.19c-.34 0-.64.11-.88.29-.17-.48-.68-.84-1.29-.84-.41 0-.78.16-1.03.42-.23-.37-.67-.63-1.19-.63-.57 0-1.05.31-1.25.74L8 5.55V1.5C8 .67 7.33 0 6.5 0S5 .67 5 1.5v6.61c-.58-.41-1.55-1.21-2.48-1.3C.96 6.67.7 7.88 1.28 8.13c1.54.67 2.99 2.68 3.7 3.95C5.89 14.05 6.07 16 9.86 16c2.09 0 3.43-.61 4.22-2.12.64-1.24.92-3.09.92-5.71v-.79c0-.65-.6-1.19-1.35-1.19"];
})), np, rp = o((() => {
	np = ["M15 10c.495 0 .933.379.993.882L16 11v.505c0 1.461-3.524 2.45-7.707 2.493L8 14c-4.31 0-8-1-8-2.495V11c0-.561.466-1 1-1 .895 0 3 1 7 1l.381-.003C12.135 10.937 14.134 10 15 10m-4-8q1.695 0 2.671 6.46c-1.063.266-2.644.652-4.887.727l-.403.01L8 9.2c-2.664 0-4.488-.444-5.673-.74Q3.306 2 5 2c2 0 1.329 2 3 2s1-2 3-2"];
})), ip, ap = o((() => {
	ip = ["M12 2c-.55 0-1 .45-1 1v4H5V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1s1-.45 1-1V9h6v4c0 .55.45 1 1 1s1-.45 1-1V3c0-.55-.45-1-1-1"];
})), op, sp = o((() => {
	op = ["M14.06 8c-.04.23-.12.44-.25.61s-.29.3-.48.41c-.18.11-.39.18-.62.23-.23.04-.46.07-.71.07v1.03h1.74V16H15V8zM7 2c-.56 0-1 .45-1 1v4H2V3c0-.55-.45-1-1-1-.56 0-1 .45-1 1v10c0 .55.45 1 1 1 .56 0 1-.45 1-1V9h4v4c0 .55.45 1 1 1 .56 0 1-.45 1-1V3c0-.54-.45-1-1-1"];
})), cp, lp = o((() => {
	cp = ["M1 2c-.56 0-1 .45-1 1v10c0 .54.45 1 1 1 .56 0 1-.45 1-1V9h4v4c0 .54.45 1 1 1 .56 0 1-.45 1-1V3c0-.54-.45-1-1-1-.56 0-1 .45-1 1v4H2V3c0-.54-.45-1-1-1m13.71 9.73c.41.08.72.3.95.651.23.35.34.772.34 1.273 0 .371-.07.702-.2.973-.14.29-.32.54-.55.741s-.5.361-.8.472-.62.16-.96.16c-.41 0-.77-.06-1.08-.19a2 2 0 0 1-.77-.542 2.4 2.4 0 0 1-.47-.852c-.11-.33-.16-.702-.17-1.103h1.14c-.01.471.09.862.32 1.173s.57.471 1.02.471c.39 0 .71-.12.97-.36q.39-.361.39-1.023c0-.3-.05-.531-.16-.712-.11-.17-.25-.31-.43-.4a1.6 1.6 0 0 0-.59-.171c-.22-.02-.44-.03-.67-.02v-.933c.19.01.38 0 .57-.04.19-.03.36-.1.51-.19.14-.09.26-.22.35-.381.09-.16.14-.361.14-.592 0-.33-.1-.591-.31-.792-.2-.2-.47-.3-.79-.3a1 1 0 0 0-.53.13c-.15.09-.27.21-.37.36-.1.151-.17.322-.22.512s-.07.381-.06.582h-1.15c.01-.381.08-.722.19-1.043s.27-.602.47-.832c.19-.23.44-.421.72-.552.28-.13.6-.2.96-.2.28 0 .55.04.82.13.27.08.51.21.72.381.21.17.38.381.51.642.13.26.19.561.19.902q0 .587-.24 1.023c-.16.29-.42.5-.76.631z"];
})), up, dp = o((() => {
	up = ["M1 2c-.56 0-1 .45-1 1v10c0 .54.45 1 1 1 .56 0 1-.45 1-1V9h4v4c0 .54.45 1 1 1 .56 0 1-.45 1-1V3c0-.54-.45-1-1-1-.56 0-1 .45-1 1v4H2V3c0-.54-.45-1-1-1m12.154 11.944.016-.014c.18-.14.36-.28.57-.42l.63-.45c.21-.16.41-.33.61-.51s.37-.38.52-.59.28-.45.37-.7.13-.54.13-.85c0-.25-.04-.51-.12-.79-.07-.29-.2-.55-.39-.79a2.2 2.2 0 0 0-.73-.6c-.29-.15-.66-.23-1.11-.23-.4 0-.76.08-1.07.23-.31.16-.58.37-.79.62-.22.27-.38.59-.49.96s-.16.77-.16 1.2h1.19c.01-.27.03-.53.08-.77.04-.24.11-.45.21-.62.09-.18.22-.32.38-.42s.35-.15.59-.15c.26 0 .47.05.63.14.15.09.28.21.37.35q.135.21.18.45c.03.16.05.31.05.45-.01.31-.08.58-.22.82-.14.23-.32.45-.53.65-.22.21-.46.39-.71.57q-.39.27-.75.54c-.5.36-.89.78-1.17 1.27S11.01 15.35 11 16h4.99v-1.14h-3.55c.05-.17.14-.33.27-.49.126-.145.28-.281.444-.426"];
})), fp, pp = o((() => {
	fp = ["M14.85 6.34C14.18 2.72 11.37 0 8 0S1.82 2.72 1.15 6.34C.47 6.9 0 8.1 0 9.5 0 11.43.9 13 2 13c0 1.1.9 2 2 2h2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1H7c-.55 0-1 .45-1 1H4c-.55 0-1-.45-1-1 .55 0 1-.45 1-1V7c0-.45-.3-.81-.71-.94C3.97 3.7 5.81 2 8 2s4.03 1.7 4.71 4.06c-.41.13-.71.49-.71.94v5c0 .55.45 1 1 1h1c1.1 0 2-1.57 2-3.5 0-1.4-.47-2.6-1.15-3.16"];
})), mp, hp = o((() => {
	mp = ["M16 5.095c0-2.255-1.88-4.083-4.2-4.083-1.682 0-3.13.964-3.8 2.352a4.21 4.21 0 0 0-3.8-2.352C1.88 1.012 0 2.84 0 5.095c0 .066.007.13.01.194H.004c.001.047.01.096.014.143l.013.142c.07.8.321 1.663.824 2.573C2.073 10.355 4.233 12.018 8 15c3.767-2.982 5.926-4.647 7.144-6.853.501-.906.752-1.767.823-2.563q.01-.083.016-.164c.003-.043.012-.088.013-.13h-.006c.003-.066.01-.13.01-.195"];
})), gp, _p = o((() => {
	gp = ["M7.71 8.87 6.17 6.55l.02-.01A.9.9 0 0 1 6 6c0-.07.03-.13.04-.19h-.02l.78-3.92C6.09 1.34 5.19 1 4.2 1 1.88 1 0 2.83 0 5.09c0 .07.01.13.01.19H0c0 .05.01.1.01.14 0 .05.01.1.01.14.07.8.32 1.66.82 2.57 1.07 1.94 2.88 3.47 5.86 5.84l-.68-2.74h.02C6.03 11.16 6 11.08 6 11c0-.28.11-.53.29-.71zM16 5.09C16 2.83 14.12 1 11.8 1c-1.2 0-2.27.5-3.04 1.28l-.7 3.51 1.77 2.66-.01.01c.1.15.18.33.18.54 0 .28-.11.53-.29.71l-1.6 1.6.75 3.01c3.23-2.56 5.16-4.15 6.28-6.18.5-.91.75-1.77.82-2.56.01-.05.01-.11.02-.16 0-.04.01-.09.01-.13h-.01c.01-.07.02-.14.02-.2"];
})), vp, yp = o((() => {
	vp = ["M0 10h5V7H0zm1-2h3v1H1zm14-5h-4v3h5V4c0-.55-.45-1-1-1m0 2h-3V4h3zM0 4v2h5V3H1c-.55 0-1 .45-1 1m0 9c0 .55.45 1 1 1h4v-3H0zm6-7h4V3H6zm0 8h4v-3H6zm1-2h2v1H7zm4 2h4c.55 0 1-.45 1-1v-2h-5zm0-4h5V7h-5zm-5 0h4V7H6z"];
})), bp, xp = o((() => {
	bp = ["M2 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m11-7c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m3 4.5A2.5 2.5 0 0 0 13.5 6c-.98 0-1.82.57-2.23 1.39-.6-.78-1.51-1.3-2.56-1.36.18-.49.29-.99.29-1.53C9 2.01 6.99 0 4.5 0S0 2.01 0 4.5 2.01 9 4.5 9c.19 0 .37-.03.56-.06-.03.19-.06.37-.06.56C5 11.43 6.57 13 8.5 13c1.63 0 2.98-1.11 3.37-2.62.44.38 1 .62 1.63.62A2.5 2.5 0 0 0 16 8.5M14.5 13c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5"];
})), Sp, Cp = o((() => {
	Sp = ["M.5 2a.5.5 0 0 1 .5.5V4h7V3H2.5a.5.5 0 0 1 0-1h13a.5.5 0 0 1 0 1H10v1h1c2.26 0 4 1.79 4 4 0 1.87-1.247 3.44-3 3.878V13h.382l1.894-.947a.5.5 0 1 1 .448.894L12.618 14H4.5a.5.5 0 0 1 0-1H7v-2.306C5.749 9.736 5 8.368 5 7L1 6v1.5a.5.5 0 0 1-1 0v-5A.5.5 0 0 1 .5 2M8 11.316V13h3v-1a6.7 6.7 0 0 1-3-.684M11 5v3h3a3 3 0 0 0-3-3"];
})), wp, Tp = o((() => {
	wp = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m1 13H7v-2h2zm1.93-6.52c-.14.32-.35.64-.62.97L9.25 8.83c-.12.15-.24.29-.28.42s-.09.3-.09.52V10H7.12V8.88s.05-.51.21-.71L8.4 6.73c.22-.26.35-.49.44-.68s.12-.38.12-.58c0-.3-.1-.55-.28-.75-.18-.19-.44-.28-.76-.28-.33 0-.59.1-.78.29s-.33.46-.4.81c-.03.11-.1.15-.2.14l-1.7-.25c-.12-.01-.16-.08-.14-.19.12-.82.46-1.47 1.03-1.94q.855-.72 2.25-.72c.47 0 .9.07 1.29.22s.72.34 1 .59.49.55.65.89c.15.35.22.72.22 1.12s-.07.75-.21 1.08"];
})), Ep, Dp = o((() => {
	Ep = ["M13 5h-2v2h2zm0 6h-2v2h2zm0-3h-2v2h2zm2-8H1C.4 0 0 .4 0 1v14c0 .6.4 1 1 1h14c.6 0 1-.4 1-1V1c0-.6-.4-1-1-1m-1 14H2V2h12zm-7-3H5v2h2zm3 0H8v2h2z"];
})), Op, kp = o((() => {
	Op = ["m3.63 14.496-3.496-6a.98.98 0 0 1 0-.992l3.495-6c.182-.312.52-.504.885-.504h6.972c.366 0 .703.192.885.504l3.495 6a.98.98 0 0 1 0 .992l-3.495 6c-.182.312-.52.504-.885.504H4.514c-.366 0-.703-.192-.885-.504m6.377-2.996H5.993L3.954 8l2.04-3.5h4.013L12.046 8zm-4.9 1.5h5.788l2.913-5-2.913-5H5.106L2.193 8zM8 9c.563 0 1.02-.448 1.02-1S8.562 7 8 7s-1.02.448-1.02 1S7.438 9 8 9"];
})), Ap, jp = o((() => {
	Ap = ["M9 14v2H7v-2zm1-14L9 12H7L6 0z"];
})), Mp, Np = o((() => {
	Mp = ["M6 0h4a1 1 0 0 1 1 1v3h2V3h-.5a.5.5 0 0 1 0-1h2a.5.5 0 0 1 0 1H14v1a1 1 0 1 1 0 2v1h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1h.5V6h-2v9a1 1 0 1 1-2 0V6H7v9a1 1 0 1 1-2 0V6H3v1h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H2V6a1 1 0 0 1 0-2V3h-.5a.5.5 0 0 1 0-1h2a.5.5 0 0 1 0 1H3v1h2V1a1 1 0 0 1 1-1m1 2v2h2V2z"];
})), Pp, Fp = o((() => {
	Pp = ["m9.12 11.07 2-2.02.71.71 4-4.04L10.17 0l-4 4.04.71.71-2 2.02zM2 12.97h4c.28 0 .53-.11.71-.3l1-1.01-3.42-3.45-3 3.03c-.18.18-.29.44-.29.72 0 .55.45 1.01 1 1.01m13 1.01H1c-.55 0-1 .45-1 1.01S.45 16 1 16h14c.55 0 1-.45 1-1.01s-.45-1.01-1-1.01"];
})), Ip, Lp = o((() => {
	Ip = ["M8 3c-.55 0-1 .45-1 1v4c0 .28.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L9 7.59V4c0-.55-.45-1-1-1m0-3a7.95 7.95 0 0 0-6 2.74V1c0-.55-.45-1-1-1S0 .45 0 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.54C4.64 2.78 6.23 2 8 2c3.31 0 6 2.69 6 6 0 2.61-1.67 4.81-4 5.63v-.01c-.63.23-1.29.38-2 .38-3.31 0-6-2.69-6-6 0-.55-.45-1-1-1s-1 .45-1 1c0 4.42 3.58 8 8 8 .34 0 .67-.03 1-.07.02 0 .04-.01.06-.01C12.98 15.4 16 12.06 16 8c0-4.42-3.58-8-8-8"];
})), Rp, zp = o((() => {
	Rp = ["M2 10v5c0 .55.45 1 1 1h3v-5h4v5h3c.55 0 1-.45 1-1v-5L8 4zm13.71-2.71L14 5.59V2c0-.55-.45-1-1-1s-1 .45-1 1v1.59L8.71.29C8.53.11 8.28 0 8 0s-.53.11-.71.29l-7 7a1.003 1.003 0 0 0 1.42 1.42L8 2.41l6.29 6.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), Bp, Vp = o((() => {
	Bp = ["M4 5h7c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1M1 1c-.55 0-1 .45-1 1v13c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1m14 6H4c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h11c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-6 5H4c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1"];
})), Hp, Up = o((() => {
	Hp = ["M1 3h5c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m0 4h7c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 6H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M1 11h10c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), Wp, Gp = o((() => {
	Wp = ["M15 1H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M8 9H1c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1m-2 4H1c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m5-8H1c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Kp, qp = o((() => {
	Kp = ["M2 0c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m13 0c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m-5 2H7c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), Jp, Yp = o((() => {
	Jp = ["M0 16V0h1a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1zM15 0h1v16h-1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1M6.707 6.707a1 1 0 0 0-1.414-1.414l-2 2a1 1 0 0 0 0 1.414l2 2a1 1 0 0 0 1.414-1.414L5.414 8zm4-1.414a1 1 0 0 0-1.414 1.414L10.586 8 9.293 9.293a1 1 0 1 0 1.414 1.414l2-2a1 1 0 0 0 0-1.414z"];
})), Xp, Zp = o((() => {
	Xp = ["M3.5 12q.14 0 .277-.005a5.98 5.98 0 0 1-1.771-3.99L2 8l.001-.139L2 7.733c0-1.134.314-2.193.86-3.098A7 7 0 0 1 9 1c2.494 0 6 .5 7 4-.925-.463-2.4-.926-3.296-.992a5.97 5.97 0 0 1 1.29 3.988L14 8a7 7 0 0 1-7 7c-2.494 0-6-.5-7-4 1 .5 2.64 1 3.5 1M8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4"];
})), Qp, $p = o((() => {
	Qp = ["M2 5v7h12V5zm0-2h12c1.1 0 2 .9 2 2v7c0 1.1-.9 2-2 2H2c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2m5.9 7.48c-.14-.33-.84-.55-1.3-.75s-.4-.33-.42-.5v-.07c.16-.14.29-.33.37-.56 0 0 0-.01.01-.02.02-.05.03-.1.05-.15.1-.01.16-.13.19-.23.03-.04.07-.15.06-.27-.02-.16-.08-.24-.15-.26v-.03c0-.2-.02-.48-.05-.67-.01-.05-.02-.1-.03-.16-.07-.23-.21-.44-.4-.58-.2-.15-.48-.23-.73-.23s-.53.08-.72.23c-.19.14-.33.35-.4.58-.02.05-.03.1-.03.16-.05.18-.06.47-.06.67v.03c-.07.03-.14.1-.15.26-.02.12.03.22.06.27.02.1.09.22.2.24.01.05.03.1.05.15v.01c.08.23.22.42.38.56v.07c-.02.17.03.29-.43.5-.46.2-1.16.42-1.3.75s-.09.52-.09.52H8c-.01 0 .05-.19-.1-.52M10 6h2c.55 0 1 .45 1 1s-.45 1-1 1h-2c-.55 0-1-.45-1-1s.45-1 1-1m0 3h2c.55 0 1 .45 1 1s-.45 1-1 1h-2c-.55 0-1-.45-1-1s.45-1 1-1"];
})), em, tm = o((() => {
	em = ["M13 2h-1.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C8.11 2.47 8 2.72 8 3s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H13c.55 0 1 .45 1 1v3c0 .55.45 1 1 1s1-.45 1-1V5c0-1.66-1.34-3-3-3m-5.5 9c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5M10 7H1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-1 6.33L7 12l-1 1-2-3-2 2.67V9h7z"];
})), nm, rm = o((() => {
	nm = ["m5.71 5.71 2-2C7.89 3.53 8 3.28 8 3s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H3C1.34 2 0 3.34 0 5v3c0 .55.45 1 1 1s1-.45 1-1V5c0-.55.45-1 1-1h1.59l-.3.29a1.003 1.003 0 0 0 1.42 1.42M12.5 11c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5M15 7H6c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-1 6.33L12 12l-1 1-2-3-2 2.67V9h7z"];
})), im, am = o((() => {
	im = ["M7.29 11.71c.18.18.43.29.71.29s.53-.11.71-.29l4-4a1.003 1.003 0 0 0-1.42-1.42L9 8.59V1c0-.55-.45-1-1-1S7 .45 7 1v7.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42zM15 11c-.55 0-1 .45-1 1v2H2v-2c0-.55-.45-1-1-1s-1 .45-1 1v3c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1"];
})), om, sm = o((() => {
	om = ["M13.91 2.6c-.16-.36-.51-.61-.92-.61h-10c-.41 0-.77.25-.92.61L-.01 7.45v5.54c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V7.45zm-1.92 5.39c-.55 0-1 .45-1 1v1h-6v-1c0-.55-.45-1-1-1H1.94l1.71-4h8.68l1.71 4z"];
})), cm, lm = o((() => {
	cm = ["M6.432 2q.141.211.324.394L8.42 4H3.66L1.95 8H4c.55 0 1 .45 1 1v1h6.557c.693 0 1.363-.262 1.837-.736l.103-.102.85-1.14a2.56 2.56 0 0 0 .623-1.682V5.058L16 7.46V13c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V7.46l2.08-4.85C2.23 2.25 2.59 2 3 2zm9.048-2c.31 0 .52.26.52.57 0 .16-.06.3-.17.41l-2.86 2.73v2.63c0 .16-.06.3-.17.41l-.82 1.1c-.1.1-.25.17-.41.17-.31 0-.57-.26-.57-.57V3.71L8.17.98A.57.57 0 0 1 8 .57c0-.31.26-.57.57-.57z"];
})), um, dm = o((() => {
	um = ["M6.341 2A6 6 0 0 0 6 4H3.66L1.95 8H4c.55 0 1 .45 1 1v1h7a5.98 5.98 0 0 0 4-1.528V13c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V7.46l2.08-4.85C2.23 2.25 2.59 2 3 2zm3.679 2.145c0-.125.075-.23.205-.225h.345l.79.8c.005 0 0 .005 0 .005v.295c0 .13-.085.23-.215.23h-.07v.15c0 .13-.09.2-.215.2v.535c0 .125-.12.225-.245.225s-.245-.1-.245-.225V5.25h-.145c-.125 0-.205-.1-.205-.23zm2.235-2.195c-.03 0-.055-.005-.06-.035 0-.03.03-.035.06-.035h.11c.035 0 .06.005.06.035s-.03.035-.06.035zm-1.165-.025a.094.094 0 0 1-.13 0l-.25-.25a.094.094 0 0 1 0-.13.094.094 0 0 1 .13 0l.25.25a.094.094 0 0 1 0 .13m1.53.445c-.035 0-.07-.025-.07-.06v-.155c0-.03.035-.06.07-.06s.07.025.07.06v.155c0 .03-.035.06-.07.06M12 0c2.21 0 4 1.79 4 4s-1.79 4-4 4-4-1.79-4-4 1.79-4 4-4m0 7c1.655 0 3-1.345 3-3 0-.195-.02-.39-.06-.575h-.21c-.125 0-.225-.07-.23-.21h-.215c.075.07.155.14.155.23V3.9c0 .06-.04.115-.075.155h-.015l-.01.005-.015.01-.445.43v.815c0 .13-.07.22-.2.22h-.36c-.125 0-.21-.09-.21-.22v-.84a.63.63 0 0 0-.36-.345h-.45c-.13 0-.245-.095-.245-.225v-.46c0-.125.115-.23.245-.23l.13-.005.21-.215c.09-.09.24-.09.33 0l.22.225h.47c.105 0 .155-.105.225-.21v-.075h-.205a.106.106 0 0 1-.105-.105.11.11 0 0 1 .105-.105h.18l.025.005v-.12s-.03-.025-.04-.025h-.2l-.045.05a.235.235 0 0 1-.33.005l-.045-.06h-.115l.16.175c.015.015.015.06 0 .075-.02.015-.045.02-.06.005l-.195-.185h-.085l-.245.23-.02-.005c-.025.07-.06.055-.095.055-.085 0-.15-.045-.15-.13s.065-.14.15-.14h.115v-.125c0-.06.04-.09.1-.09h.05V2.36c0-.095.095-.2.19-.2h.19c.105 0 .18-.075.18-.185V1.94c0-.015.035.01.035-.06h-.125l-.005.01-.21.22a.085.085 0 0 1-.115 0 .085.085 0 0 1 0-.115l.255-.255c.02-.015.045-.015.065-.015.005 0 .005.015.005.015h.64a2.3 2.3 0 0 0-.355-.275 2.5 2.5 0 0 0-.355-.195q-.044-.024-.08-.04a3.03 3.03 0 0 0-1.735-.175c-.09.02-.175.055-.265.08-.09.03-.18.05-.265.085-.075.03-.145.07-.22.105-.115.06-.235.115-.34.185l-.005.005c-.1.065-.18.145-.27.22h.455c.06 0 .11.045.11.105s-.05.105-.11.105h-.32c0 .07-.025.04-.025.045v.24h.285l.15-.17c.09-.09.235-.105.325-.015s.09.23 0 .32l-.795.79-.01.01c-.005 0-.005 0-.01.005l-.025.015h-.01a.24.24 0 0 1-.12.025h-.23c-.08.07-.125.1-.125.18v.06c0 .01-.02.02-.02.03l.375.39c.04.04.04.1 0 .14s-.1.04-.14 0l-.39-.385a.2.2 0 0 1-.055.01c-.105 0-.195-.085-.195-.185v-.235h-.055A3 3 0 0 0 9 4c0 1.655 1.345 3 3 3m2.27-2.135c.05 0 .105.04.105.09v.285c0 .05-.055.09-.105.09s-.105-.04-.105-.09v-.285c0-.05.055-.09.105-.09m-2.085-3.27c0 .13-.105.21-.225.21h-.25v.07c0 .075-.03.135-.105.135s-.105-.06-.105-.135V1.64c-.075-.02-.025-.025-.025-.04 0-.125.085-.215.21-.215h.27c.13 0 .23.085.23.21"];
})), fm, pm = o((() => {
	fm = ["M5.639 2a5.4 5.4 0 0 0-.144 2H3.66L1.95 8H4c.55 0 1 .45 1 1v1h6V9q0-.133.033-.255c.12-.007.238-.019.39-.038.154-.008.252-.03.442-.077a5 5 0 0 0 .24-.05h.05l.122-.04 1.266 1.271c.425.47 1.116.769 1.847.769q.316-.001.61-.071V13c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V7.46l2.08-4.85C2.23 2.25 2.59 2 3 2zM15.82 7.53c.1.12.17.27.18.44 0 .34-.27.61-.61.61a.57.57 0 0 1-.43-.18l-2.24-2.25c-.13.08-.26.16-.4.23-.02.01-.05.02-.07.03-.14.06-.27.12-.42.17h-.01c-.14.05-.29.08-.44.11-.04.01-.08.02-.11.02-.15.02-.3.04-.46.04-1.85 0-3.35-1.51-3.35-3.37S8.96.01 10.81 0c1.85 0 3.35 1.51 3.35 3.37 0 .16-.02.31-.04.47-.01.04-.01.07-.02.11-.02.15-.05.29-.1.44v.01c-.05.15-.11.28-.17.42-.01.02-.02.05-.03.07-.07.14-.14.27-.23.4zm-5.01-1.94c1.22 0 2.21-.99 2.21-2.22s-.99-2.22-2.21-2.22-2.21.99-2.21 2.22c0 1.22.99 2.22 2.21 2.22"];
})), mm, hm = o((() => {
	mm = ["M8.1 2a5 5 0 0 0 0 2H3.66L1.95 8H4c.55 0 1 .45 1 1v1h6V9c0-.55.45-1 1-1h2.05c.708 0 1.352-.241 1.905-.645L16 7.46V13c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V7.46l2.08-4.85C2.23 2.25 2.59 2 3 2zM13 6a3 3 0 1 1 0-6 3 3 0 0 1 0 6"];
})), gm, _m = o((() => {
	gm = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8M7 3h2v2H7zm3 10H6v-1h1V7H6V6h3v6h1z"];
})), vm, ym = o((() => {
	vm = ["M5 8c0 1.66 1.34 3 3 3h4.59L11.3 9.71A.97.97 0 0 1 11 9a1.003 1.003 0 0 1 1.71-.71l3 3c.18.18.29.43.29.71s-.11.53-.29.71l-3 3a1.003 1.003 0 0 1-1.42-1.42l1.3-1.29H8c-2.76 0-5-2.24-5-5H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1zM2 2v4h4V2z"];
})), bm, xm = o((() => {
	bm = ["M1 7c.51 0 .935.388.993.884L2 8v3c0 .51.388.935.884.993L3 12h1.59l-.3-.29a1.003 1.003 0 0 1 1.324-1.504l.096.084 2 2c.18.18.29.43.29.71a1 1 0 0 1-.206.614l-.084.096-2 2A1.003 1.003 0 0 1 4 15c0-.24.08-.458.224-.629l.076-.081.29-.29H3a2.996 2.996 0 0 1-2.995-2.823L0 11V8c0-.55.45-1 1-1m5.388-7c.629 0 1.338.21 1.838.6.48.38.85.91 1.019 1.52.04.13.07.27.09.4.09.48.14 1.22.14 1.73v.07c.18.08.34.27.37.67.03.32-.09.59-.16.71-.06.28-.21.58-.48.63q-.045.195-.12.39c0 .01-.01.04-.01.04-.22.58-.55 1.08-.949 1.45v.18c.04.45-.12.77 1.059 1.3s2.947 1.09 3.307 1.95c.37.86.22 1.36.22 1.36H9c0-.539-.21-1.045-.583-1.417l-2-2A2 2 0 0 0 5 9q-.223 0-.442-.045c.099-.19.082-.37.101-.575 0-.05.01-.11.01-.17-.41-.35-.75-.86-.969-1.45v-.01s-.01-.01-.01-.02c-.04-.12-.09-.26-.12-.39-.28-.05-.44-.36-.5-.64-.06-.12-.19-.39-.16-.71.04-.41.21-.6.39-.68v-.06c0-.51.05-1.26.14-1.74.02-.13.05-.27.09-.4.17-.6.54-1.13 1.02-1.51C5.048.21 5.757 0 6.387 0m4.625 2.04c.49 0 1.05.16 1.439.46.38.29.67.7.8 1.17.03.1.05.21.07.31.07.37.11.94.11 1.33v.05c.139.06.269.21.289.51.02.25-.07.45-.13.54-.05.21-.16.44-.38.48a1.7 1.7 0 0 1-.1.33c-.17.44-.43.83-.749 1.11v.14c.03.35-.09.59.83 1 .929.41 2.317.84 2.597 1.5.29.66.17 1.04.17 1.04H13.66v.01c-.05-.24-.14-.5-.25-.76-.36-.86-1.119-1.33-2.687-2-.14-.06-.59-.25-.6-.25-.21-.09-.36-.15-.5-.22.02-.1.02-.2.03-.31 0-.04.01-.08.01-.13-.07-.06-.13-.12-.19-.19q.33-.48.54-1.05c.02-.06.02-.06.03-.1.29-.23.48-.57.59-.96.16-.33.25-.73.21-1.16-.03-.4-.16-.76-.37-1.03-.02-.53-.07-1.13-.15-1.54-.01-.06-.02-.12-.03-.19.23-.06.48-.09.72-.09"];
})), Sm, Cm = o((() => {
	Sm = ["M6.6 3.3C5.3 4.4 4.5 6.1 4.5 8s.8 3.6 2.1 4.7c-.5.2-1 .3-1.6.3-2.8 0-5-2.2-5-5s2.2-5 5-5c.6 0 1.1.1 1.6.3m-1.96 8.68C3.92 10.83 3.5 9.46 3.5 8s.42-2.83 1.14-3.98C2.6 4.2 1 5.91 1 8s1.6 3.8 3.64 3.98M8 4c-1.2.9-2 2.4-2 4s.8 3.1 2 4c1.2-.9 2-2.3 2-4s-.8-3.1-2-4m3-1c2.8 0 5 2.2 5 5s-2.2 5-5 5c-.6 0-1.1-.1-1.6-.3 1.3-1.1 2.1-2.9 2.1-4.7s-.8-3.5-2.1-4.7c.5-.2 1-.3 1.6-.3m.35 1.02c.73 1.15 1.14 2.52 1.14 3.98s-.42 2.83-1.14 3.98c2.04-.18 3.64-1.9 3.64-3.98s-1.6-3.8-3.64-3.98"];
})), wm, Tm = o((() => {
	wm = ["M8 16c4.41 0 8-3.582 8-8.005S12.41 0 8 0c-.94 0-1.86.16-2.74.48-.52.19-.79.76-.6 1.281s.76.79 1.28.6a6.007 6.007 0 0 1 8.05 5.644 6.007 6.007 0 0 1-8.05 5.643.997.997 0 0 0-1.28.6 1 1 0 0 0 .6 1.282c.88.32 1.8.47 2.74.47m3.71-8.705c.18.18.29.43.29.71s-.11.53-.29.71l-3 3.002a1.003 1.003 0 0 1-1.71-.71c0-.28.11-.53.3-.71l1.29-1.291H1c-.55 0-1-.45-1-1.001s.45-1 1-1h7.59l-1.3-1.291a1.003 1.003 0 0 1 1.42-1.42z"];
})), Em, Dm = o((() => {
	Em = ["M5 9h2v2c0 .6.4 1 1 1s1-.4 1-1V9h2c.6 0 1-.4 1-1s-.4-1-1-1H9V5c0-.6-.4-1-1-1s-1 .4-1 1v2H5c-.6 0-1 .4-1 1s.4 1 1 1m10-9H1C.4 0 0 .4 0 1v14c0 .6.4 1 1 1h14c.6 0 1-.4 1-1V1c0-.6-.4-1-1-1m-1 14H2V2h12z"];
})), Om, km = o((() => {
	Om = ["M8 7c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.46-1-1-1m4.988.976v-.042a.4.4 0 0 0-.107-.216 7.6 7.6 0 0 0-1.087-1.082c-.83-.703-1.78-1.292-2.824-1.527a4.3 4.3 0 0 0-1.818-.024 5.6 5.6 0 0 0-1.593.595c-.781.427-1.5 1.01-2.125 1.665-.112.12-.225.246-.33.379a.43.43 0 0 0 0 .558c.318.403.699.758 1.086 1.082.831.703 1.78 1.292 2.824 1.527a4.4 4.4 0 0 0 1.831.024c.556-.108 1.087-.325 1.593-.595a8.7 8.7 0 0 0 2.118-1.665c.113-.12.232-.246.338-.379A.4.4 0 0 0 13 8.06V8c-.012-.012-.012-.018-.012-.024M8 10c-1.107 0-2-.893-2-2s.893-2 2-2 2 .893 2 2-.893 2-2 2M7 1a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v5a1 1 0 0 0 2 0V2h4a1 1 0 0 0 1-1m2 0a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0V2h-4a1 1 0 0 1-1-1m0 14a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-5a1 1 0 1 0-2 0v4h-4a1 1 0 0 0-1 1m-2 0a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-5a1 1 0 0 1 2 0v4h4a1 1 0 0 1 1 1"];
})), Am, jm = o((() => {
	Am = ["M10 3c-.92 0-1.76.26-2.5.69C6.76 3.26 5.92 3 5 3 2.24 3 0 5.24 0 8s2.24 5 5 5c.92 0 1.76-.26 2.5-.69.74.43 1.58.69 2.5.69 2.76 0 5-2.24 5-5s-2.24-5-5-5m-4.1 7.85c-.29.09-.59.15-.9.15-1.66 0-3-1.34-3-3s1.34-3 3-3c.31 0 .61.06.9.15C5.33 5.96 5 6.94 5 8s.33 2.04.9 2.85M10 11c-.31 0-.61-.06-.9-.15.57-.81.9-1.79.9-2.85s-.33-2.04-.9-2.85c.29-.09.59-.15.9-.15 1.66 0 3 1.34 3 3s-1.34 3-3 3"];
})), Mm, Nm = o((() => {
	Mm = ["M5 2.66C5 4.14 8 8 8 8s3-3.86 3-5.34C10.99 1.2 9.66 0 8 0S5 1.2 5 2.66M7 3c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1m3.5 7H8v5h1v-4h1v1H9v1h2v-3zM2 9h12c.55 0 1 .45 1 1v5c0 .55-.45 1-1 1H2c-.55 0-1-.45-1-1v-5c0-.55.45-1 1-1m4 1v5h1v-5z"];
})), Pm, Fm = o((() => {
	Pm = ["M8 16A8 8 0 1 1 8 0a8 8 0 0 1 0 16m0-2A6 6 0 1 0 8 2a6 6 0 0 0 0 12m1-2H7v-2h2zm0-3H7V4h2z"];
})), Im, Lm = o((() => {
	Im = ["M9.296.104a3 3 0 0 0-1.003.664 3 3 0 0 0-.75 1.25 6 6 0 1 0 6.28 4.527q.064-.059.127-.12l1.456-1.456A8 8 0 1 1 9.296.105m2.532 5.2a1 1 0 0 1-.707-.294L9.707 3.596a1 1 0 0 1 1.414-1.414l.707.707 1.768-1.768a1 1 0 1 1 1.414 1.415L12.536 5.01a1 1 0 0 1-.708.293M9 12H7v-2h2zm0-3H7V4h2z"];
})), Rm, zm = o((() => {
	Rm = ["M10.568.421q-.014.06-.026.121a2.51 2.51 0 0 0-1.85 1.497 6 6 0 1 0 5.27 5.273 2.51 2.51 0 0 0 1.496-1.854l.121-.026A8 8 0 1 1 10.568.421M9 12H7v-2h2zm0-3H7V4h2zm1-6c0-.55.45-1 1-1h1V1c0-.55.45-1 1-1s1 .45 1 1v1h1c.55 0 1 .45 1 1s-.45 1-1 1h-1v1.005c0 .55-.45 1-1 1s-1-.45-1-1V4h-1c-.55 0-1-.45-1-1"];
})), Bm, Vm = o((() => {
	Bm = ["M9.8 4H11c.5 0 1-.4 1-1s-.4-1-1-1H7c-.5 0-1 .4-1 1s.4 1 1 1h.8l-1.6 8H5c-.5 0-1 .4-1 1s.4 1 1 1h4c.5 0 1-.4 1-1s-.4-1-1-1h-.8z"];
})), Hm, Um = o((() => {
	Hm = ["M15 5h-3V2c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h3v3c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-5-1v2H6V4zm0 6H6V7h4zM2 4h3v2H2zm0 5V7h3v2zm4 4v-2h4v2zm8 0h-3v-2h3zm0-3h-3V8h3z"];
})), Wm, Gm = o((() => {
	Wm = ["M11 0C8.24 0 6 2.24 6 5c0 1.02.31 1.96.83 2.75L.29 14.29a1.003 1.003 0 0 0 1.42 1.42L3 14.41l1.29 1.29c.18.19.43.3.71.3s.53-.11.71-.29l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71L6.41 11l1.83-1.83c.8.52 1.74.83 2.76.83 2.76 0 5-2.24 5-5s-2.24-5-5-5m0 8c-.23 0-.45-.03-.66-.08-.01 0-.02-.01-.03-.01q-.315-.075-.6-.21a3.01 3.01 0 0 1-1.62-2c0-.01-.01-.02-.01-.03C8.03 5.45 8 5.23 8 5c0-1.66 1.34-3 3-3s3 1.34 3 3-1.34 3-3 3"];
})), Km, qm = o((() => {
	Km = ["M15 2H6c-.28 0-.53.11-.71.29l-5 5C.11 7.47 0 7.72 0 8s.11.53.29.71l5 5c.18.18.43.29.71.29h9c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m-2.29 7.29a1.003 1.003 0 0 1-1.42 1.42L10 9.41 8.71 10.7c-.18.19-.43.3-.71.3a1.003 1.003 0 0 1-.71-1.71L8.59 8l-1.3-1.29a1.003 1.003 0 0 1 1.42-1.42L10 6.59l1.29-1.29c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71L11.41 8z"];
})), Jm, Ym = o((() => {
	Jm = ["M12 9h-1V7h1c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3v1H7V4c0-1.66-1.34-3-3-3S1 2.34 1 4s1.34 3 3 3h1v2H4c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3v-1h2v1c0 1.66 1.34 3 3 3s3-1.34 3-3-1.34-3-3-3m0-6c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1M4 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m0-8c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m5 4H7V7h2zm3 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), Xm, Zm = o((() => {
	Xm = ["m12.71 5.29-4-4C8.53 1.11 8.28 1 8 1s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L8 3.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), Qm, $m = o((() => {
	Qm = ["m15.71 7.29-5-5A1 1 0 0 0 10 2H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h9c.28 0 .53-.11.71-.29l5-5c.18-.18.29-.43.29-.71s-.11-.53-.29-.71m-7 2a1.003 1.003 0 0 1-1.42 1.42L6 9.41 4.71 10.7c-.18.19-.43.3-.71.3a1.003 1.003 0 0 1-.71-1.71L4.59 8l-1.3-1.29a1.003 1.003 0 0 1 1.42-1.42L6 6.59 7.29 5.3c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71L7.41 8z"];
})), eh, th = o((() => {
	eh = ["M14 2c-.55 0-1 .45-1 1v3c0 1.66-1.34 3-3 3H4.41L5.7 7.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3c-.18.18-.29.43-.29.71s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L4.41 11H10c2.76 0 5-2.24 5-5V3c0-.55-.45-1-1-1"];
})), nh, rh = o((() => {
	nh = ["M2 7c.55 0 1-.45 1-1V4.41L7.29 8.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L4.41 3H6c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1m7-5.9v2A5 5 0 1 1 3.1 9h-2c.49 3.39 3.38 6 6.9 6 3.87 0 7-3.13 7-7 0-3.52-2.61-6.41-6-6.9"];
})), ih, ah = o((() => {
	ih = ["M11 4h4c.55 0 1-.45 1-1s-.45-1-1-1h-4c-.55 0-1 .45-1 1s.45 1 1 1m4 8h-3.43L5.86 2.49h-.02A.98.98 0 0 0 5 2H1c-.55 0-1 .45-1 1s.45 1 1 1h3.43l5.71 9.51.01-.01c.18.3.49.5.85.5h4c.55 0 1-.45 1-1s-.45-1-1-1"];
})), oh, sh = o((() => {
	oh = ["m13.71 7.29-5-5C8.53 2.11 8.28 2 8 2s-.53.11-.71.29l-5 5A1.003 1.003 0 0 0 3 9h2v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V9h2a1.003 1.003 0 0 0 .71-1.71"];
})), ch, lh = o((() => {
	ch = ["M15 10H4.41L5.7 8.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L2 9.59V8c0-.55-.45-1-1-1s-1 .45-1 1v6c0 .55.45 1 1 1s1-.45 1-1v-1.59l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L4.41 12H15c.55 0 1-.45 1-1s-.45-1-1-1m0-9c-.55 0-1 .45-1 1v1.59L11.71 1.3A.97.97 0 0 0 11 1a1.003 1.003 0 0 0-.71 1.71L11.59 4H1c-.55 0-1 .45-1 1s.45 1 1 1h10.59L10.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L14 6.41V8c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1"];
})), uh, dh = o((() => {
	uh = ["M15 3a1 1 0 0 0-.707.293L12 5.586l-1.293-1.293a1 1 0 1 0-1.414 1.414l2 2a.997.997 0 0 0 1.414 0l3-3A1 1 0 0 0 15 3m-.879 6.121-.007-.007A3 3 0 0 1 13 9.816V10h-2v-.184c-.424-.15-.8-.395-1.112-.704l-.01.01-2-2 .012-.012A3 3 0 0 1 7.184 6H3c-.176 0-.06-.824 0-1l.73-1.63C3.79 3.192 3.823 3 4 3h3.78c.548-.61 1.335-1 2.22-1 .768 0 1.461.293 1.987.77l.844-.844c-.238-.244-.524-.442-.794-.524C12.037 1.402 10.72 1 8 1s-4.037.402-4.037.402c-.508.155-1.078.711-1.268 1.237l-.763 2.117H.88c-.484 0-.88.423-.88.939s.396.939.88.939h.375L1 7c-.034.685 0 1.436 0 2v5c0 .657.384 1 1 1s1-.343 1-1v-1h10v1c0 .657.384 1 1 1s1-.343 1-1V9l-.003-.754zM5.001 10H3V8h2z"];
})), fh, ph = o((() => {
	fh = ["M11 1a1 1 0 0 1 0 2v3l3 7v1.25a.75.75 0 0 1-.75.75H2.75a.75.75 0 0 1-.75-.75V13l3-7V3a1 1 0 1 1 0-2zM9 3H7v3l-1.714 4h5.428L9 6z"];
})), mh, hh = o((() => {
	mh = ["M11 2H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V7zm3 10H2V4h8v2H3v1h7v1h4zm-3-5V4l3 3zm-8 3h10V9H3z"];
})), gh, _h = o((() => {
	gh = ["M16 8c0-.37-.21-.68-.51-.85l.01-.01-7-4-.01.01C8.34 3.06 8.18 3 8 3s-.34.06-.49.15l-.01-.02-7 4 .01.01C.21 7.32 0 7.63 0 8s.21.68.51.85l-.01.01 7 4 .01-.01c.15.09.31.15.49.15s.34-.06.49-.15l.01.01 7-4-.01-.01c.3-.17.51-.48.51-.85"];
})), vh, yh = o((() => {
	vh = ["m7.504 3.132-7 4a1 1 0 0 0 0 1.736l7 4a1 1 0 0 0 .992 0l7-4a1 1 0 0 0 0-1.736l-7-4a1 1 0 0 0-.992 0M8 5.152 12.983 8 8 10.847 3.016 8z"];
})), bh, xh = o((() => {
	bh = ["m.55 4.89 7 3c.14.07.29.11.45.11s.31-.04.45-.11l7-3a.998.998 0 0 0-.06-1.81L8.4.08a1 1 0 0 0-.79 0l-6.99 3a.992.992 0 0 0-.07 1.81M15 11c-.16 0-.31.04-.45.11L8 14l-6.55-2.9c-.14-.06-.29-.1-.45-.1-.55 0-1 .45-1 1 0 .39.23.73.55.89l7 3c.14.07.29.11.45.11s.31-.04.45-.11l7-3c.32-.16.55-.5.55-.89 0-.55-.45-1-1-1m0-4c-.16 0-.31.04-.45.11L8 10 1.45 7.11A1 1 0 0 0 1 7c-.55 0-1 .45-1 1 0 .39.23.73.55.89l7 3c.14.07.29.11.45.11s.31-.04.45-.11l7-3c.32-.16.55-.5.55-.89 0-.55-.45-1-1-1"];
})), Sh, Ch = o((() => {
	Sh = ["M14 4c-1.1 0-2 .9-2 2 0 .47.17.9.44 1.24l-.68.91A1.996 1.996 0 0 0 9.07 9.5H7.93C7.71 8.64 6.93 8 6 8c-.47 0-.9.17-1.24.44l-.91-.68c.1-.23.15-.49.15-.76 0-.37-.11-.71-.28-1.01l2.27-2.27c.3.17.64.28 1.01.28 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .37.11.71.28 1.01L3.01 5.28C2.71 5.11 2.37 5 2 5 .9 5 0 5.9 0 7s.9 2 2 2c.47 0 .9-.17 1.24-.44l.91.68c-.1.23-.15.49-.15.76 0 .37.11.71.28 1.01l-1.27 1.27C2.71 12.11 2.37 12 2 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2c0-.37-.11-.71-.28-1.01l1.27-1.27c.3.17.64.28 1.01.28.93 0 1.71-.64 1.93-1.5h1.14c.22.86 1 1.5 1.93 1.5 1.1 0 2-.9 2-2 0-.47-.17-.9-.44-1.24l.68-.91c.23.1.49.15.76.15 1.1 0 2-.9 2-2s-.9-2-2-2"];
})), wh, Th = o((() => {
	wh = ["M14 9.5c-.56 0-1.06.23-1.42.59L8.99 8l3.59-2.09A2.002 2.002 0 0 0 16 4.5c0-1.1-.9-2-2-2s-2 .9-2 2c0 .19.03.37.08.54L8.5 7.13v-3.2c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S6 .9 6 2c0 .93.64 1.71 1.5 1.93v3.2L3.92 5.04c.05-.17.08-.35.08-.54 0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.56 0 1.06-.23 1.42-.59L7.01 8l-3.59 2.09A2.002 2.002 0 0 0 0 11.5c0 1.1.9 2 2 2s2-.9 2-2c0-.19-.03-.37-.08-.54L7.5 8.87v3.2c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93v-3.2l3.58 2.09c-.05.17-.08.35-.08.54 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2"];
})), Eh, Dh = o((() => {
	Eh = ["M14 11c-.2 0-.38.04-.56.09L12.42 9.4c.36-.36.58-.85.58-1.4s-.22-1.04-.58-1.4l1.01-1.69c.19.05.37.09.57.09 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .55.22 1.04.58 1.4l-1.01 1.69C11.38 6.04 11.2 6 11 6c-.93 0-1.71.64-1.93 1.5H6.93C6.71 6.64 5.93 6 5 6c-.2 0-.38.04-.56.09L3.42 4.4C3.78 4.04 4 3.55 4 3c0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.2 0 .38-.04.56-.09L3.58 6.6C3.22 6.96 3 7.45 3 8s.22 1.04.58 1.4l-1.01 1.69C2.38 11.04 2.2 11 2 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2c0-.55-.22-1.04-.58-1.4l1.01-1.69c.19.05.37.09.57.09.93 0 1.71-.64 1.93-1.5h2.14c.22.86 1 1.5 1.93 1.5.2 0 .38-.04.56-.09l1.01 1.69c-.35.36-.57.85-.57 1.4 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2"];
})), Oh, kh = o((() => {
	Oh = ["M7 9a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1zM1 9a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1zm12 0a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1zM1 0a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V1a1 1 0 0 0-1-1z"];
})), Ah, jh = o((() => {
	Ah = ["M6 9a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1zm9 0a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1zm0-9a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1z"];
})), Mh, Nh = o((() => {
	Mh = ["M14.16 6.02c-.12-.36-.26-.7-.43-1.03.17-.29.27-.63.27-.99 0-1.1-.9-2-2-2-.36 0-.7.1-.99.27-.33-.17-.67-.31-1.03-.43A1.987 1.987 0 0 0 8 0C6.95 0 6.1.81 6.02 1.84c-.36.12-.7.26-1.03.43C4.7 2.1 4.36 2 4 2c-1.1 0-2 .9-2 2 0 .36.1.7.27.99-.17.33-.31.67-.43 1.03C.81 6.1 0 6.95 0 8s.81 1.9 1.84 1.98c.12.36.26.7.43 1.03-.17.29-.27.63-.27.99 0 1.1.9 2 2 2 .36 0 .7-.1.99-.27.33.17.67.32 1.03.43C6.1 15.19 6.95 16 8 16s1.9-.81 1.98-1.84c.36-.12.7-.26 1.03-.43.29.17.63.27.99.27 1.1 0 2-.9 2-2 0-.36-.1-.7-.27-.99.17-.33.31-.67.43-1.03C15.19 9.9 16 9.05 16 8s-.81-1.9-1.84-1.98m-.99 3.79c-.05.16-.11.31-.17.46-.3-.17-.64-.27-1-.27-1.1 0-2 .9-2 2 0 .36.1.7.27 1-.15.07-.3.12-.46.17C9.5 12.48 8.81 12 8 12s-1.5.48-1.81 1.17c-.16-.06-.32-.11-.46-.17.17-.3.27-.64.27-1 0-1.1-.9-2-2-2-.36 0-.7.1-1 .27-.07-.15-.12-.3-.17-.46C3.52 9.5 4 8.81 4 8s-.48-1.5-1.17-1.81c.06-.16.11-.32.17-.46.3.17.64.27 1 .27 1.1 0 2-.9 2-2 0-.36-.1-.7-.27-1 .15-.07.3-.12.46-.17C6.5 3.52 7.19 4 8 4s1.5-.48 1.81-1.17c.16.06.32.11.46.17-.17.3-.27.64-.27 1 0 1.1.9 2 2 2 .36 0 .7-.1 1-.27.07.15.12.3.17.46C12.48 6.5 12 7.19 12 8s.48 1.5 1.17 1.81"];
})), Ph, Fh = o((() => {
	Ph = ["M2 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-6C.9 6 0 6.9 0 8s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-6C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m12 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M8 0C6.9 0 6 .9 6 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M8 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Ih, Lh = o((() => {
	Ih = ["M2 6C.9 6 0 6.9 0 8s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 5c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m12-7c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2M2 1C.9 1 0 1.9 0 3s.9 2 2 2 2-.9 2-2-.9-2-2-2m7 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m5 3c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Rh, zh = o((() => {
	Rh = ["M14.5 12.07V9.93c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2-.93 0-1.71.64-1.93 1.5H9.93c-.18-.7-.73-1.25-1.43-1.43V3.93c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S6 .9 6 2c0 .93.64 1.71 1.5 1.93v2.14c-.7.18-1.25.73-1.43 1.43H3.93C3.71 6.64 2.93 6 2 6 .9 6 0 6.9 0 8c0 .93.64 1.71 1.5 1.93v2.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93V9.93c.7-.18 1.25-.73 1.43-1.43h2.14c.18.7.73 1.25 1.43 1.43v2.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93V9.93c.7-.18 1.25-.73 1.43-1.43h2.14c.18.7.73 1.25 1.43 1.43v2.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93"];
})), Bh, Vh = o((() => {
	Bh = ["M7 7a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zm0-6a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zm0 12a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zm9-12a1 1 0 0 0-1-1h-5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1z"];
})), Hh, Uh = o((() => {
	Hh = ["M7 1a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zm0 9a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zm9-9a1 1 0 0 0-1-1h-5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1z"];
})), Wh, Gh = o((() => {
	Wh = ["M14 6c-.93 0-1.71.64-1.93 1.5H9.93C9.71 6.64 8.93 6 8 6s-1.71.64-1.93 1.5H3.93C3.71 6.64 2.93 6 2 6 .9 6 0 6.9 0 8s.9 2 2 2c.93 0 1.71-.64 1.93-1.5h2.13C6.29 9.36 7.07 10 8 10s1.71-.64 1.93-1.5h2.13c.22.86 1 1.5 1.93 1.5 1.1 0 2-.9 2-2C16 6.9 15.1 6 14 6"];
})), Kh, qh = o((() => {
	Kh = ["M9 7a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zm0-6a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zm0 12a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), Jh, Yh = o((() => {
	Jh = ["M9 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zm0 9a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), Xh, Zh = o((() => {
	Xh = ["M2 6C.9 6 0 6.9 0 8s.9 2 2 2 2-.9 2-2-.9-2-2-2m12-2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2M2 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 9c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6-3c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M8 3c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 9c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Qh, $h = o((() => {
	Qh = ["M2 6C.9 6 0 6.9 0 8s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m12 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M8 9c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), eg, tg = o((() => {
	eg = ["M12 1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1zM6 1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), ng, rg = o((() => {
	ng = ["M15 12a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1zm0-6a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1zm0-6a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1z"];
})), ig, ag = o((() => {
	ig = ["M7 7a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1zM1 7a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1zm12 0a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1zM1 16a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1z"];
})), og, sg = o((() => {
	og = ["M10 7a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1zM1 7a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1zm0 9a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1z"];
})), cg, lg = o((() => {
	cg = ["M9 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), ug, dg = o((() => {
	ug = ["M0 10a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0-9a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), fg, pg = o((() => {
	fg = ["M8.441 1.104a.99.99 0 0 0-.882 0L.365 5c-.487.253-.487.747 0 1L7.56 9.896a.99.99 0 0 0 .882 0L15.635 6c.487-.253.487-.747 0-1zM14 5.5l.016 4.514c.002.548.447.99.994.99a.99.99 0 0 0 .99-.99V5.5zM3.371 9.047l4.387 2.432a.5.5 0 0 0 .485 0l4.39-2.432a.25.25 0 0 1 .371.218v2.955a.25.25 0 0 1-.134.222l-4.635 2.436a.5.5 0 0 1-.466 0l-4.635-2.436A.25.25 0 0 1 3 12.22V9.265a.25.25 0 0 1 .371-.218"];
})), mg, hg = o((() => {
	mg = ["M6.6 3.3C6.1 3.1 5.6 3 5 3 2.2 3 0 5.2 0 8s2.2 5 5 5c.6 0 1.1-.1 1.6-.3C5.3 11.6 4.5 9.9 4.5 8s.8-3.6 2.1-4.7M8 4c-1.2.9-2 2.4-2 4s.8 3.1 2 4c1.2-.9 2-2.3 2-4s-.8-3.1-2-4m3-1c2.8 0 5 2.2 5 5s-2.2 5-5 5c-.6 0-1.1-.1-1.6-.3 1.3-1.1 2.1-2.9 2.1-4.7s-.8-3.5-2.1-4.7c.5-.2 1-.3 1.6-.3m.35 1.02c.73 1.15 1.14 2.52 1.14 3.98s-.42 2.83-1.14 3.98c2.04-.18 3.64-1.9 3.64-3.98s-1.6-3.8-3.64-3.98"];
})), gg, _g = o((() => {
	gg = ["M1 9h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m4 3H1c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1m7-1c0 .28.11.53.29.71l.3.29H9c-.55 0-1 .45-1 1s.45 1 1 1h3.59l-.29.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2A1.003 1.003 0 0 0 12 11M1 4h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), vg, yg = o((() => {
	vg = ["M13.287 5.958a1 1 0 0 0-.574-1.916l-10 3c-.95.285-.95 1.631 0 1.916l10 3a1 1 0 0 0 .574-1.916L6.48 8z"];
})), bg, xg = o((() => {
	bg = ["M13.287 3.958a1 1 0 0 0-.575-1.916l-10 3c-.95.285-.95 1.63 0 1.916l10 3a1 1 0 0 0 .575-1.916L6.48 6zM13 12H3a1 1 0 0 0 0 2h10a1 1 0 0 0 0-2"];
})), Sg, Cg = o((() => {
	Sg = ["M9.405 11.746C8.968 11.91 8.495 12 8 12c-.494 0-.968-.09-1.405-.254l-.702 1.873C6.548 13.865 7.258 14 8 14s1.452-.135 2.107-.38zm2.341-2.341 1.873.702C13.865 9.452 14 8.742 14 8s-.135-1.452-.38-2.107l-1.874.702c.164.437.254.91.254 1.405 0 .494-.09.968-.254 1.405M9.405 4.254l.702-1.873A6 6 0 0 0 8 2c-.742 0-1.452.135-2.107.38l.702 1.874C7.032 4.09 7.505 4 8 4c.494 0 .968.09 1.405.254M4.254 6.595 2.38 5.893A6 6 0 0 0 2 8c0 .742.135 1.452.38 2.107l1.874-.702A4 4 0 0 1 4 8c0-.494.09-.968.254-1.405M8 16A8 8 0 1 1 8 0a8 8 0 0 1 0 16m0-6a2 2 0 1 0 0-4 2 2 0 0 0 0 4"];
})), wg, Tg = o((() => {
	wg = ["M9.01 14h-2c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1s-.44-1-1-1m1-3h-4c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1s-.44-1-1-1m-2-11C5.26 0 3.03 1.95 3.03 4.35c0 2.37 1.63 2.64 1.94 5.22 0 .24.22.44.5.44h5.09c.28 0 .5-.19.5-.44C11.37 6.99 13 6.72 13 4.35 13 1.95 10.77 0 8.01 0"];
})), Eg, Dg = o((() => {
	Eg = ["M7 9H5a1 1 0 0 1-1-1L4.89.876A1 1 0 0 1 5.884 0h4.27a.847.847 0 0 1 .793 1.144L9.125 6h2.05a.825.825 0 0 1 .754 1.16L8.16 15.64A.606.606 0 0 1 7 15.394z"];
})), Og, kg = o((() => {
	Og = ["M4.99 11.99c.28 0 .53-.11.71-.29l6-6a1.003 1.003 0 0 0-1.42-1.42l-6 6a1.003 1.003 0 0 0 .71 1.71m3.85-2.02L6.4 12.41l-1 1-.01-.01c-.36.36-.85.6-1.4.6-1.1 0-2-.9-2-2 0-.55.24-1.04.6-1.4l-.01-.01 1-1 2.44-2.44c-.33-.1-.67-.16-1.03-.16-1.1 0-2.09.46-2.81 1.19l-.02-.02-1 1 .02.02c-.73.72-1.19 1.71-1.19 2.81 0 2.21 1.79 4 4 4 1.1 0 2.09-.46 2.81-1.19l.02.02 1-1-.02-.02c.73-.72 1.19-1.71 1.19-2.81 0-.35-.06-.69-.15-1.02m7.15-5.98c0-2.21-1.79-4-4-4-1.1 0-2.09.46-2.81 1.19l-.02-.02-1 1 .02.02c-.72.72-1.19 1.71-1.19 2.81 0 .36.06.69.15 1.02l2.44-2.44 1-1 .01.01c.36-.36.85-.6 1.4-.6 1.1 0 2 .9 2 2 0 .55-.24 1.04-.6 1.4l.01.01-1 1-2.43 2.45c.33.09.67.15 1.02.15 1.1 0 2.09-.46 2.81-1.19l.02.02 1-1-.02-.02a3.92 3.92 0 0 0 1.19-2.81"];
})), Ag, jg = o((() => {
	Ag = ["M2 3v6a1 1 0 0 1 0 2h-.75C.56 11 0 10.44 0 9.75v-7.5C0 1.56.56 1 1.25 1h9.5c.69 0 1.25.56 1.25 1.25v7.5c0 .69-.56 1.25-1.25 1.25H8a1 1 0 1 1 0-2h2V3zm12 10V7a1 1 0 1 1 0-2h.75c.69 0 1.25.56 1.25 1.25v7.5c0 .69-.56 1.25-1.25 1.25h-9.5C4.56 15 4 14.44 4 13.75v-7.5C4 5.56 4.56 5 5.25 5H8a1 1 0 1 1 0 2H6v6z"];
})), Mg, Ng = o((() => {
	Mg = ["M1 3h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 10H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m0-4H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m0-4H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Pg, Fg = o((() => {
	Pg = ["M6 1c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1zm9-12c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1zm0 4c.55 0 1 .45 1 1s-.45 1-1 1h-5c-.55 0-1-.45-1-1s.45-1 1-1z"];
})), Ig, Lg = o((() => {
	Ig = ["M6 9H1c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m0 4H1c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m9-12h-5c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M6 5H1c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m0-4H1c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Rg, zg = o((() => {
	Rg = ["M15 7h-.09A6.98 6.98 0 0 0 9 1.1V1c0-.55-.45-1-1-1S7 .45 7 1v.09A6.98 6.98 0 0 0 1.1 7H1c-.55 0-1 .45-1 1s.45 1 1 1h.1A6.97 6.97 0 0 0 7 14.91V15c0 .55.45 1 1 1s1-.45 1-1v-.09A6.98 6.98 0 0 0 14.9 9h.1c.55 0 1-.45 1-1s-.45-1-1-1m-6.02 5.9c-.05-.5-.46-.9-.98-.9s-.93.4-.98.9A5.02 5.02 0 0 1 3.1 8.98c.5-.05.9-.46.9-.98s-.4-.93-.9-.98A5.02 5.02 0 0 1 7.02 3.1c.05.5.46.9.98.9s.93-.4.98-.9c1.97.39 3.52 1.95 3.92 3.92-.5.05-.9.46-.9.98s.4.93.9.98a5.02 5.02 0 0 1-3.92 3.92M8 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Bg, Vg = o((() => {
	Bg = ["M13.96 7H12V3.95C12 1.77 10.21 0 8 0S4 1.77 4 3.95V7H1.96c-.55 0-.96.35-.96.9v6.91c0 .54.41 1.19.96 1.19h12c.55 0 1.04-.65 1.04-1.19V7.9c0-.55-.49-.9-1.04-.9M6 7V3.95c0-1.09.9-1.97 2-1.97s2 .88 2 1.97V7z"];
})), Hg, Ug = o((() => {
	Hg = ["M0 2a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v4h3V4L9.854 2.854A.5.5 0 0 1 10.207 2h3.586a.5.5 0 0 1 .353.854L13 4v2c1.833 1 4.4 3.6 0 6l1.488 1.488a.3.3 0 0 1-.212.512h-.982a.53.53 0 0 1-.444-.253c-.898-1.423-2.854-3.06-4.701-.004a.52.52 0 0 1-.443.257h-.412a.53.53 0 0 1-.444-.253c-.898-1.423-2.854-3.06-4.701-.004a.52.52 0 0 1-.443.257H0zm1 5h3V2H1zm6 0V2H5v5zm-2.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3m0-1a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1m7.5-.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m-1 0a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0"];
})), Wg, Gg = o((() => {
	Wg = ["M11 8c0-.28-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L7.59 7H1c-.55 0-1 .45-1 1s.45 1 1 1h6.59L6.3 10.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71m4-8H9c-.55 0-1 .45-1 1s.45 1 1 1h5v12H9c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), Kg, qg = o((() => {
	Kg = ["M7 14H2V2h5c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1m8.71-6.71-3-3a1.003 1.003 0 0 0-1.42 1.42L12.59 7H6c-.55 0-1 .45-1 1s.45 1 1 1h6.59l-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), Jg, Yg = o((() => {
	Jg = ["M8 0a1 1 0 0 0-1 1v1H3v-.5a.5.5 0 0 0-1 0V2a1 1 0 0 0 0 2v1h-.5a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1H3V4h4v11a1 1 0 1 0 2 0V4h4v1h-.5a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1H14V4a1 1 0 1 0 0-2v-.5a.5.5 0 0 0-1 0V2H9V1a1 1 0 0 0-1-1"];
})), Xg, Zg = o((() => {
	Xg = ["M15.99 1.13c-.02-.41-.33-.77-.78-.87C12.26-.36 9.84.13 8 1.7 6.16.13 3.74-.36.78.26.33.35.03.72.01 1.13H0v12c0 .08 0 .17.02.26.12.51.65.82 1.19.71 2.63-.55 4.59-.04 6.01 1.57.02.03.06.04.08.06s.03.04.05.06c.04.03.09.04.13.07.05.03.09.05.14.07.11.04.23.07.35.07h.04c.12 0 .24-.03.35-.07.05-.02.09-.05.14-.07.04-.02.09-.04.13-.07.02-.02.03-.04.05-.06.03-.02.06-.03.08-.06 1.42-1.6 3.39-2.12 6.01-1.57.54.11 1.07-.21 1.19-.71.04-.09.04-.18.04-.26zM7 12.99c-1.4-.83-3.07-1.14-5-.93V1.96c2.11-.28 3.75.2 5 1.46zm7-.92c-1.93-.21-3.6.1-5 .93V3.42c1.25-1.26 2.89-1.74 5-1.46z"];
})), Qg, $g = o((() => {
	Qg = ["M1 8h3.76l2-2H1c-.55 0-1 .45-1 1s.45 1 1 1m14.49-4.01c.31-.32.51-.76.51-1.24C16 1.78 15.22 1 14.25 1c-.48 0-.92.2-1.24.51l-1.44 1.44 2.47 2.47zM1 4h7.76l2-2H1c-.55 0-1 .45-1 1s.45 1 1 1m0 6c-.55 0-1 .45-1 1 0 .48.35.86.8.96L2.76 10zm9.95-6.43-6.69 6.69 2.47 2.47 6.69-6.69zm4.25 2.47L13.24 8H15c.55 0 1-.45 1-1 0-.48-.35-.86-.8-.96M2 15l3.86-1.39-2.46-2.44zm13-5h-3.76l-2 2H15c.55 0 1-.45 1-1s-.45-1-1-1"];
})), e_, t_ = o((() => {
	e_ = ["M3 3a1 1 0 1 0 0 2 1 1 0 0 0 0-2m3 1q0 .07-.003.14c.255.081.538.209.832.41.406.28.8.676 1.171 1.225.37-.549.765-.945 1.171-1.224a3.1 3.1 0 0 1 .832-.411L10 4a3 3 0 1 1 .773 2.01 1.04 1.04 0 0 0-.47.19c-.291.2-.752.672-1.227 1.8.475 1.128.936 1.6 1.227 1.8.183.126.336.173.47.19a3 3 0 1 1-.77 1.87 3.1 3.1 0 0 1-.832-.41c-.406-.28-.8-.676-1.171-1.225-.37.549-.765.945-1.171 1.224-.294.202-.577.33-.832.411Q6 11.93 6 12a3 3 0 1 1-.773-2.01c.134-.017.287-.064.47-.19.291-.2.752-.672 1.227-1.8-.475-1.128-.936-1.6-1.227-1.8a1.04 1.04 0 0 0-.47-.19A3 3 0 1 1 6 4m6 0a1 1 0 1 0 2 0 1 1 0 0 0-2 0m-9 7a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 1a1 1 0 1 0 2 0 1 1 0 0 0-2 0"];
})), n_, r_ = o((() => {
	n_ = ["M3 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2m0-2c1.385 0 2.551.94 2.896 2.215q.253.066.51.158c1.076.394 2.237 1.242 2.575 2.93.161.809.664 1.211 1.293 1.443a3 3 0 1 1 0 2.508c-.629.232-1.132.634-1.293 1.442-.338 1.69-1.499 2.537-2.575 2.93a5 5 0 0 1-.51.159A3.001 3.001 0 0 1 0 13a3 3 0 0 1 5.726-1.254c.629-.232 1.132-.634 1.293-1.442.216-1.076.765-1.81 1.413-2.304-.648-.493-1.197-1.228-1.413-2.304-.161-.808-.664-1.21-1.293-1.442A3 3 0 1 1 3 0m1 13a1 1 0 1 0-2 0 1 1 0 0 0 2 0m8-5a1 1 0 1 0 2 0 1 1 0 0 0-2 0"];
})), i_, a_ = o((() => {
	i_ = ["m15.55 3.17-4.49-3A.98.98 0 0 0 9.99.15L5.53 2.82 1.56.17A1.003 1.003 0 0 0 0 1v11c0 .35.18.65.45.83l4.49 3a.98.98 0 0 0 1.07.02l4.46-2.67 3.97 2.65A1.003 1.003 0 0 0 16 15V4c0-.35-.18-.65-.45-.83M5 13.46l-3-2v-8.6l2.94 1.96c.02.02.04.03.06.04zm5-2.32s-.01 0-.01.01L6 13.53V4.86s.01 0 .01-.01L10 2.47zm4 1.99-2.94-1.96c-.02-.01-.04-.02-.05-.03v-8.6l3 2v8.59z"];
})), o_, s_ = o((() => {
	o_ = ["M14 6.82v6.32l-2.94-1.96c-.02-.01-.04-.02-.05-.03V6.22c-.08-.07-.15-.16-.22-.24-.28-.02-.54-.08-.79-.16v5.32s-.01 0-.01.01L6 13.53V4.86s.01 0 .01-.01l2.05-1.23C8.02 3.42 8 3.21 8 3c0-.98.47-1.84 1.2-2.39l-3.67 2.2L1.56.17A1.003 1.003 0 0 0 0 1v11c0 .35.18.65.45.83l4.49 3a.98.98 0 0 0 1.07.02l4.46-2.67 3.97 2.65A1.003 1.003 0 0 0 16 15V5.82c-.25.09-.52.14-.8.16-.33.36-.73.67-1.2.84m-9 6.64-3-2v-8.6l2.94 1.96c.02.02.04.03.06.04zM11 4h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), c_, l_ = o((() => {
	c_ = ["M8 0C4.96 0 2.49 2.39 2.49 5.33 2.49 8.28 8 16 8 16s5.51-7.72 5.51-10.67C13.5 2.39 11.04 0 8 0m0 8a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5"];
})), u_, d_ = o((() => {
	u_ = ["M14 2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM8 5.848c0-.693-.875-.943-1.257-.427l-.07.113L5.5 7.882 4.326 5.534l-.07-.113C3.877 4.905 3 5.155 3 5.848V10.5a.5.5 0 0 0 1 0V7.118l.605 1.211a1 1 0 0 0 1.79 0L7 7.12v3.38a.5.5 0 0 0 1 0zM11.5 5a.5.5 0 0 0-.5.5v3.793l-.646-.647-.079-.064a.5.5 0 0 0-.693.693l.064.079 1.43 1.43a.6.6 0 0 0 .848 0l1.43-1.43a.5.5 0 1 0-.707-.708L12 9.293V5.5a.5.5 0 0 0-.5-.5"];
})), f_, p_ = o((() => {
	f_ = ["M5.99 8.99c-.28 0-.53.11-.71.29l-3.29 3.29v-1.59c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.41L6.7 10.7a1.003 1.003 0 0 0-.71-1.71m9-9h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59l-3.3 3.3a1 1 0 0 0-.29.7 1.003 1.003 0 0 0 1.71.71l3.29-3.29V5c0 .55.45 1 1 1s1-.45 1-1V1c0-.56-.45-1.01-1-1.01"];
})), m_, h_ = o((() => {
	m_ = ["M11.99 6.99c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1m3-5h-14c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-10c0-.55-.45-1-1-1m-1 9-5-3-1 2-3-4-3 5v-7h12z"];
})), g_, __ = o((() => {
	g_ = ["M1 4h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 8H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m0-5H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), v_, y_ = o((() => {
	v_ = ["M14.99 6.99h-9c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1m-12-2c-.28 0-.53.11-.71.29l-2 2a1.014 1.014 0 0 0 0 1.42l2 2a1.003 1.003 0 0 0 1.71-.71v-4c0-.55-.45-1-1-1m3-1h9c.55 0 1-.45 1-1s-.45-1-1-1h-9c-.55 0-1 .45-1 1s.45 1 1 1m9 8h-9c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1"];
})), b_, x_ = o((() => {
	b_ = ["M9.99 11.99h-9c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1m0-5h-9c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1m0-5h-9c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1m5.71 5.3-2-2a1.003 1.003 0 0 0-1.71.71v4a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), S_, C_ = o((() => {
	S_ = ["M5.71 5.29a1.003 1.003 0 0 0-1.42 1.42l.3.29H2V2h3v1.51c.52.06.99.29 1.34.65l.66.66V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-3.82l-.66.66c-.35.35-.82.59-1.34.65V14H2V9h2.59l-.3.29a1.003 1.003 0 0 0 1.42 1.42l2-2C7.89 8.53 8 8.28 8 8s-.11-.53-.29-.71zM15 0h-5c-.55 0-1 .45-1 1v3.82l.66-.66c.35-.35.82-.59 1.34-.65V2h3v5h-2.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C8.11 7.47 8 7.72 8 8s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H14v5h-3v-1.51c-.52-.06-.99-.29-1.34-.65L9 11.18V15c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), w_, T_ = o((() => {
	w_ = ["M8 7c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m6 3c-.93 0-1.71.64-1.93 1.5H11V3c0-1.66-1.34-3-3-3S5 1.34 5 3v4.5H3.93C3.71 6.64 2.93 6 2 6 .9 6 0 6.9 0 8s.9 2 2 2c.93 0 1.71-.64 1.93-1.5H5V13c0 1.66 1.34 3 3 3s3-1.34 3-3V8.5h1.07c.22.86 1 1.5 1.93 1.5 1.1 0 2-.9 2-2s-.9-2-2-2m-4 7c0 1.1-.9 2-2 2s-2-.9-2-2V3c0-1.1.9-2 2-2s2 .9 2 2z"];
})), E_, D_ = o((() => {
	E_ = ["M8 0a3 3 0 0 0-3 3v4a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3M3 5a1 1 0 0 1 1 1v2a3 3 0 0 0 3 3h2a3 3 0 0 0 3-3V6a1 1 0 1 1 2 0v2a5 5 0 0 1-5 5v1h1a1 1 0 1 1 0 2H6a1 1 0 1 1 0-2h1v-1a5 5 0 0 1-5-5V6a1 1 0 0 1 1-1"];
})), O_, k_ = o((() => {
	O_ = ["M15.99.99a1.003 1.003 0 0 0-1.71-.71l-3.29 3.29V1.99c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H12.4l3.3-3.29c.18-.18.29-.43.29-.71m-10 8h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59L.29 14.28a1.003 1.003 0 0 0 1.42 1.42L5 12.41V14c0 .55.45 1 1 1s1-.45 1-1v-4a1.02 1.02 0 0 0-1.01-1.01"];
})), A_, j_ = o((() => {
	A_ = ["M13 7H3c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1"];
})), M_, N_ = o((() => {
	M_ = ["M12 0H4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h8c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M8 15c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m3-3H5V3h6z"];
})), P_, F_ = o((() => {
	P_ = ["M15 4c-.28 0-.53.11-.71.29L12 6.59V4c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V9.41l2.29 2.29c.18.19.43.3.71.3.55 0 1-.45 1-1V5c0-.55-.45-1-1-1"];
})), I_, L_ = o((() => {
	I_ = ["M15 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm-1 4H2v8h12zm-3-3H9v2h2zm3 0h-2v2h2z"];
})), R_, z_ = o((() => {
	R_ = ["M15 1H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1m1 4H0V3h16zm-3-2h-2V1h2z"];
})), B_, V_ = o((() => {
	B_ = ["M14.745 14H1.255A1.25 1.25 0 0 1 0 12.704C.058 11.21.223 8.66.7 6.42c.255-1.196.599-2.303 1.063-3.111C2.24 2.48 2.823 2 3.53 2c.752 0 1.322.305 1.777.775.455.469.79 1.094 1.078 1.72.08.175.166.37.248.56l.003.006c.192.443.372.854.539 1.151.113.202.25.413.424.57.159.141.32.218.528.218.707 0 1.12-.436 1.505-.88l.003-.004.107-.122c.222-.249.461-.499.771-.685.308-.186.686-.309 1.19-.309.575 0 1.107.325 1.591.878.48.545.9 1.298 1.265 2.127.66 1.504 1.13 3.254 1.41 4.468A1.25 1.25 0 0 1 14.744 14"];
})), H_, U_ = o((() => {
	H_ = ["M15 11.38A7.84 7.84 0 0 1 7.85 16C3.51 16 0 12.49 0 8.15 0 4.97 1.89 2.23 4.62 1c-.45.99-.7 2.08-.7 3.23a7.85 7.85 0 0 0 7.85 7.85c1.15 0 2.24-.25 3.23-.7"];
})), W_, G_ = o((() => {
	W_ = ["M2 6a2 2 0 1 1 0 4 2 2 0 0 1 0-4m6 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m6 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4"];
})), K_, q_ = o((() => {
	K_ = ["M16 13H3l6-9h1l2 2h1zm-2.5-3.5-1-2.5h-1l-2-2-3 4.5L9 8l1 1 1-1zM5.94 7l-4.122 6H0l5-6z"];
})), J_, Y_ = o((() => {
	J_ = ["m15.71 7.29-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H9V3.41l.29.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-2-2C8.53.11 8.28 0 8 0s-.53.11-.71.29l-2 2a1.003 1.003 0 0 0 1.42 1.42l.29-.3V7H3.41l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C.11 7.47 0 7.72 0 8s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L3.41 9H7v3.59l-.29-.29A.97.97 0 0 0 6 12a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2a1.003 1.003 0 0 0-1.42-1.42l-.29.3V9h3.59l-.29.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), X_, Z_ = o((() => {
	X_ = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14h-.15c-.03-.09-.04-.16-.08-.25-.34-.79-2.01-1.31-3.12-1.8s-.96-.79-1-1.2c-.01-.06-.01-.12-.01-.18.38-.34.69-.8.89-1.33 0 0 .01-.03.01-.04.04-.12.08-.24.11-.36.25-.05.4-.33.46-.59.06-.1.18-.36.15-.65-.04-.37-.19-.55-.35-.62v-.06c0-.48-.04-1.16-.13-1.61-.02-.12-.05-.25-.08-.37-.16-.55-.51-1.05-.96-1.39C9.26 3.19 8.6 3 8 3c-.59 0-1.26.19-1.73.55-.45.35-.8.84-.96 1.39-.04.13-.06.25-.08.38-.09.45-.13 1.13-.13 1.61v.06c-.18.06-.33.24-.37.62-.03.29.09.54.15.65.06.26.21.54.47.59.03.12.07.25.11.36 0 .01.01.02.01.02v.01c.21.54.53 1.01.92 1.35 0 .05-.01.11-.01.16-.04.41.08.7-1.03 1.2-1.11.49-2.77 1.01-3.12 1.8-.04.09-.05.16-.08.25H2V2h12z"];
})), Q_, $_ = o((() => {
	Q_ = ["M12 3.98H4c-.55 0-1 .45-1 1v1h8v5h1c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1m3-3H7c-.55 0-1 .45-1 1v1h8v5h1c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1m-6 6H1c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1m-1 5H2v-3h6z"];
})), ev, tv = o((() => {
	ev = ["M15 0c-.07 0-.13.03-.19.04V.02l-10 2v.02C4.35 2.13 4 2.52 4 3v9.12c-.31-.07-.65-.12-1-.12-1.66 0-3 .9-3 2s1.34 2 3 2 3-.9 3-2V6.32l8-1.6v5.4c-.31-.07-.65-.12-1-.12-1.66 0-3 .9-3 2s1.34 2 3 2 3-.9 3-2V1c0-.55-.45-1-1-1"];
})), nv, rv = o((() => {
	nv = ["M2 2c.55 0 1 .45 1 1v3c0 1.66 1.34 3 3 3h5.59L10.3 7.71A.97.97 0 0 1 10 7a1.003 1.003 0 0 1 1.71-.71l3 3c.18.18.29.43.29.71s-.11.53-.29.71l-3 3a1.003 1.003 0 0 1-1.42-1.42l1.3-1.29H6c-2.76 0-5-2.24-5-5V3c0-.55.45-1 1-1"];
})), iv, av = o((() => {
	iv = ["M15 2h-1V1a1 1 0 1 0-2 0v1h-1a1 1 0 1 0 0 2h1v1a1 1 0 1 0 2 0V4h1a1 1 0 1 0 0-2M8 3c0-.768.289-1.47.764-2H2c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h2v3a1.003 1.003 0 0 0 1.71.71L9.41 12H15c.55 0 1-.45 1-1V5.83l-.129.041a3.001 3.001 0 0 1-5.742 0A3 3 0 0 1 8 3"];
})), ov, sv = o((() => {
	ov = ["M14.9 11c.6 0 1 .5 1 1 0 .257-.073.44-.22.614l-.08.086-3 3c-.2.2-.4.3-.7.3-.5 0-1-.4-1-1 0-.257.073-.44.22-.614l.08-.086 3-3c.2-.2.4-.3.7-.3M1.3.1l6.734 2.45a3.005 3.005 0 0 0 2.095 3.322 3.005 3.005 0 0 0 3.401 2.081L13.9 9.8v.2c0 .257-.073.44-.22.614l-.08.086-3 3c-.171.171-.343.27-.577.294L9.9 14h-.2l-5-1-.1-.01c-.231-.05-.45-.26-.56-.49L4 12.4l-4-11 .3-.3 5.8 5.8c-.1.2-.2.4-.2.6 0 .8.6 1.5 1.5 1.5s1.5-.7 1.5-1.5S8.2 6 7.4 6c-.16 0-.32.064-.48.14l-.12.06L1 .4zM13 0c.55 0 1 .45 1 1v1h1c.55 0 1 .45 1 1s-.45 1-1 1h-1v1c0 .503-.376.922-.861.99l-.013.002A1 1 0 0 1 13 6l.097-.006-.027.004-.037.001L13 6c-.55 0-1-.45-1-1V4h-1a.99.99 0 0 1-.855-.482A1 1 0 0 1 10 3c0-.55.45-1 1-1h1V1c0-.55.45-1 1-1"];
})), cv, lv = o((() => {
	cv = ["M6 0H1C.45 0 0 .45 0 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m5 14c0-.55-.45-1-1-1s-1 .45-1 1v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1s-.45-1-1-1M6 9H1c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1m9 4c-.55 0-1 .45-1 1-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m-4-4h-1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1s1-.45 1-1c.55 0 1-.45 1-1s-.45-1-1-1m4-9h-5c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m0 9h-1c-.55 0-1 .45-1 1s.45 1 1 1c0 .55.45 1 1 1s1-.45 1-1v-1c0-.55-.45-1-1-1"];
})), uv, dv = o((() => {
	uv = ["m13.982 6.272 1.518.868-.01.01c.3.17.51.48.51.85s-.21.68-.51.85l.01.01-7 4-.01-.01A.94.94 0 0 1 8 13a.94.94 0 0 1-.49-.15l-.01.01-7-4 .01-.01A.98.98 0 0 1 0 8c0-.37.21-.68.51-.86L.5 7.13l7-4 .01.02A.94.94 0 0 1 8 3q.129.001.246.038a2 2 0 1 0 5.735 3.234M14 3c.55 0 1 .45 1 1s-.45 1-1 1h-1v1c0 .55-.45 1-1 1s-1-.45-1-1V5h-1c-.55 0-1-.45-1-1s.45-1 1-1h1V2c0-.55.45-1 1-1s1 .45 1 1v1z"];
})), fv, pv = o((() => {
	fv = ["M13 3h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V5H9a1 1 0 1 1 0-2h2V1a1 1 0 1 1 2 0zm-3-1.983V2H9a2 2 0 1 0 0 4h1v1c0 .279.057.544.16.785l-1.71.855c-.14.07-.29.11-.45.11s-.31-.04-.45-.11l-7-3.5a.992.992 0 0 1 .07-1.81l6.99-3a1 1 0 0 1 .79 0zm.91 7.66a2 2 0 0 0 3.085-1.54l.555-.277c.14-.07.29-.11.45-.11.55 0 1 .45 1 1 0 .39-.23.73-.55.89l-7 3.5c-.14.07-.29.11-.45.11s-.31-.04-.45-.11l-7-3.5C.23 8.48 0 8.14 0 7.75c0-.55.45-1 1-1 .16 0 .31.04.45.11L8 10.13zM15 10.25c.55 0 1 .45 1 1 0 .39-.23.73-.55.89l-7 3.5c-.14.07-.29.11-.45.11s-.31-.04-.45-.11l-7-3.5c-.32-.16-.55-.5-.55-.89 0-.55.45-1 1-1 .16 0 .31.04.45.1L8 13.63l6.55-3.27c.14-.07.29-.11.45-.11"];
})), mv, hv = o((() => {
	mv = ["M15 3h-1V2c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V5h1c.55 0 1-.45 1-1s-.45-1-1-1m-3.5 6a2.5 2.5 0 0 0-2.45 2h-4.1a2.5 2.5 0 1 0 0 1h4.1a2.5 2.5 0 1 0 2.45-3"];
})), gv, _v = o((() => {
	gv = ["M8 4c0 .6.4 1 1 1h2v2c0 .6.4 1 1 1s1-.4 1-1V5h2c.6 0 1-.4 1-1s-.4-1-1-1h-2V1c0-.6-.4-1-1-1s-1 .4-1 1v2H9c-.6 0-1 .5-1 1m6.5 2.5V7c0 1.4-1.1 2.5-2.5 2.5S9.5 8.4 9.5 7v-.5H9C7.6 6.5 6.5 5.4 6.5 4S7.6 1.5 9 1.5h.5V1c0-.3.1-.6.1-.8C9.1.1 8.6 0 8 0 3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8c0-.6-.1-1.3-.2-1.9-.4.3-.8.4-1.3.4"];
})), vv, yv = o((() => {
	vv = ["M9.12 12.69c-1.17-.53-1.01-.85-1.05-1.29-.01-.06-.01-.12-.01-.19.4-.37.73-.87.94-1.44 0 0 .01-.03.01-.04.05-.14.09-.27.12-.4.27-.06.43-.36.49-.63.06-.11.19-.39.16-.7-.04-.41-.2-.6-.38-.68v-.07c0-.51-.05-1.25-.14-1.74-.02-.13-.05-.27-.09-.4-.17-.6-.53-1.14-1.01-1.52C7.66 3.2 6.96 3 6.33 3c-.62 0-1.33.2-1.82.59-.49.38-.85.92-1.02 1.52-.04.13-.07.26-.09.4-.09.49-.13 1.23-.13 1.74v.06c-.19.08-.35.27-.39.68-.03.31.1.59.16.7.06.28.22.59.5.64.03.14.07.27.11.4 0 .01.01.02.01.02v.01c.22.59.55 1.1.96 1.46 0 .06-.01.12-.01.17-.04.44.08.76-1.09 1.29S.59 13.78.23 14.63C-.12 15.5.03 16 .03 16h12.6s.15-.5-.22-1.36c-.36-.85-2.12-1.42-3.29-1.95M14.89 2h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1"];
})), bv, xv = o((() => {
	bv = ["m9.82 11.66 2.48-2.87c.12-.2.13-.37.04-.53-.11-.19-.3-.26-.52-.26h-1.29c-.27 0-.49.13-.63.34L8.44 9.9 6.95 8a.5.5 0 0 0-.08-.1L5.82 6.55c.57-.24 1.04-.57 1.42-1.01.49-.57.74-1.27.74-2.08 0-.51-.1-.99-.32-1.42-.21-.43-.51-.8-.89-1.11A4.1 4.1 0 0 0 5.42.24C4.91.08 4.34 0 3.72 0H.61C.26 0 0 .23 0 .56v9.89c0 .33.26.55.61.55h.8c.36 0 .61-.23.61-.56V6.99H3.3l3.73 4.74-2.71 3.48c-.12.2-.13.37-.04.53.11.19.3.26.52.26h1.27c.27 0 .51-.12.64-.34l1.69-2.15 1.66 2.14c.12.21.34.35.62.35h1.43c.2 0 .39-.08.5-.25.12-.18.09-.38-.02-.55zM4.18 5H1.99V2.02h2.19c.62 0 1.08.13 1.38.37.29.22.44.62.44 1.08 0 .45-.15.94-.44 1.17-.31.23-.76.36-1.38.36M15 2h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1M9.99 3.01c0 .02.01.04.01.06v-.12c0 .02-.01.04-.01.06"];
})), Sv, Cv = o((() => {
	Sv = ["M11 4h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1M8 1Q3.334 4.214 1 4.214 1 11.714 8 16q5.696-3.487 6.757-9.102a4 4 0 0 1-2.055 1.04c-.762 2.394-2.32 4.41-4.702 6.088z"];
})), wv, Tv = o((() => {
	wv = ["M5 6.5c0 .28.22.5.5.5H7v3.5c0 .28.22.5.5.5s.5-.22.5-.5V7h1.5c.28 0 .5-.22.5-.5S9.78 6 9.5 6h-4c-.28 0-.5.22-.5.5M15 2h-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V4h1c.55 0 1-.45 1-1s-.45-1-1-1m-2 5c-.55 0-1 .45-1 1v5H3V4h5c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h11c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1"];
})), Ev, Dv = o((() => {
	Ev = ["M16 5s-2.52 2.11-4.96 1.99C11.03 4.89 10.39.23 5 0c0 0 2.11 2.54 1.96 4.99C4.86 5.01.23 5.65 0 11c0 0 2.56-2.12 5.02-1.95.02 2.11.67 6.72 5.98 6.95 0 0-2.09-2.54-1.94-4.99 2.11-.02 6.71-.68 6.94-6.01M8 9.5c-.83 0-1.5-.67-1.5-1.5S7.17 6.5 8 6.5s1.5.67 1.5 1.5S8.83 9.5 8 9.5"];
})), Ov, kv = o((() => {
	Ov = ["m7.58 5 .44-2.196a1 1 0 0 1 1.96.392L9.62 5H13a1 1 0 0 1 0 2H9.22l-.4 2H13a1 1 0 0 1 0 2H8.42l-.44 2.196a1 1 0 0 1-1.96-.392L6.38 11H3a1 1 0 0 1 0-2h3.78l.4-2H3a1 1 0 1 1 0-2z"];
})), Av, jv = o((() => {
	Av = ["M8 16c1.1 0 2-.9 2-2H6c0 1.1.9 2 2 2m6-5c-.55 0-1-.45-1-1V6c0-2.43-1.73-4.45-4.02-4.9 0-.04.02-.06.02-.1 0-.55-.45-1-1-1S7 .45 7 1c0 .04.02.06.02.1A4.99 4.99 0 0 0 3 6v4c0 .55-.45 1-1 1s-1 .45-1 1 .45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Mv, Nv = o((() => {
	Mv = ["m8.98 1.1.007.001-.008.028a3.001 3.001 0 0 0 0 5.742A3 3 0 0 0 13 8.771V10c0 .55.45 1 1 1s1 .45 1 1-.45 1-1 1H2c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V6c0-2.43 1.73-4.45 4.02-4.9a.2.2 0 0 0-.01-.05Q7.001 1.029 7 1c0-.55.45-1 1-1s1 .45 1 1q-.001.029-.01.05a.2.2 0 0 0-.01.05M8 16c1.1 0 2-.9 2-2H6c0 1.1.9 2 2 2m6-13h-1V2a1 1 0 1 0-2 0v1h-1a1 1 0 0 0 0 2h1v1a1 1 0 1 0 2 0V5h1a1 1 0 1 0 0-2"];
})), Pv, Fv = o((() => {
	Pv = ["M10 14c0 1.1-.9 2-2 2s-2-.9-2-2zM8 0c.404 0 .755.243.912.59L8.9.6c-.7.6-.9 1.36-.9 1.9q0 1.2.8 1.9-.8.9-.784 1.867l.004.358a2.8 2.8 0 0 0 2.8 2.775L13 9.399V10c0 .51.388.935.884.993L14 11c.55 0 1 .45 1 1s-.45 1-1 1H2c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V6c0-2.43 1.73-4.45 4.02-4.9L7 1c0-.55.45-1 1-1m6 6.702a.63.63 0 0 0-.632-.632h-1.743l2.209-2.734A.75.75 0 0 0 14 2.864v-.3A.565.565 0 0 0 13.435 2h-2.874a.561.561 0 1 0 0 1.123h1.814l-2.154 2.672a1 1 0 0 0-.221.628v.279c0 .349.283.631.632.631h2.736A.63.63 0 0 0 14 6.702"];
})), Iv, Lv = o((() => {
	Iv = ["M8 16c1.1 0 2-.9 2-2H6c0 1.1.9 2 2 2m3.399-13.667-.413.412A3 3 0 0 0 9 1.99a3 3 0 0 0-3 2.99c0 .8.32 1.558.876 2.114l2.002 1.992A2.99 2.99 0 0 0 13 9.184V10c0 .55.45 1 1 1s1 .45 1 1-.45 1-1 1H2c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V6c0-2.43 1.73-4.45 4.02-4.9 0-.04-.02-.06-.02-.1 0-.55.45-1 1-1s1 .45 1 1c0 .04-.02.06-.02.1a4.97 4.97 0 0 1 2.419 1.233M10.29 7.67l-2-1.99a1 1 0 0 1-.29-.7 1 1 0 0 1 1-.99c.27 0 .52.11.7.29l1.29 1.29 3.28-3.28c.18-.18.42-.29.7-.29.55 0 1 .44 1 .99 0 .28-.11.52-.3.7l-3.98 3.98a.99.99 0 0 1-1.4 0"];
})), Rv, zv = o((() => {
	Rv = ["M2.76 7h1.26V0h-.94c-.04.21-.12.39-.25.54q-.195.225-.48.36c-.18.09-.39.16-.62.2s-.46.06-.71.06v.9h1.74zm-.59 7.17c.18-.12.37-.25.58-.37a11 11 0 0 0 1.24-.83c.2-.16.37-.33.52-.51.15-.19.28-.39.37-.61s.14-.47.14-.74c0-.22-.04-.45-.12-.7-.08-.26-.21-.49-.4-.69-.18-.21-.43-.39-.72-.52-.3-.14-.68-.21-1.12-.21-.41 0-.77.07-1.08.2-.32.14-.58.32-.8.56-.22.23-.38.51-.49.84-.11.32-.16.67-.16 1.05h1.19c.01-.24.03-.47.08-.67.05-.21.11-.39.21-.54.09-.15.22-.27.38-.36s.35-.13.59-.13q.39 0 .63.12c.16.08.29.18.38.3q.135.18.18.39c.03.14.05.27.05.4-.01.27-.08.5-.22.71s-.32.4-.53.57c-.22.18-.45.34-.71.49s-.51.31-.74.47q-.75.465-1.17 1.11c-.3.41-.44.91-.45 1.48h5v-1H1.43c.05-.15.14-.29.27-.43.14-.13.29-.26.47-.38M15.01 1.99h-7c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-1c0-.55-.44-1-1-1m0 9h-7c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-1c0-.55-.44-1-1-1"];
})), Bv, Vv = o((() => {
	Bv = ["M2.79 4.61c-.13.17-.29.3-.48.41-.18.11-.39.18-.62.23-.23.04-.46.07-.71.07v1.03h1.74V12h1.26V4h-.94c-.04.23-.12.44-.25.61m4.37 5.31c.18-.14.37-.28.58-.42l.63-.45c.21-.16.41-.33.61-.51s.37-.38.52-.59.28-.45.37-.7.13-.54.13-.85c0-.25-.04-.52-.12-.8-.07-.29-.2-.55-.39-.79a2.2 2.2 0 0 0-.73-.6c-.29-.15-.66-.23-1.11-.23-.41 0-.77.08-1.08.23-.31.16-.58.37-.79.64-.22.27-.38.59-.49.96s-.16.77-.16 1.2h1.19c.01-.27.03-.53.08-.77.04-.24.11-.45.21-.62.09-.18.22-.32.38-.42s.35-.15.59-.15c.26 0 .47.05.63.14.15.09.28.21.37.35q.135.21.18.45c.03.16.05.31.05.45-.01.31-.08.58-.22.82-.14.23-.32.45-.53.65-.22.21-.46.39-.71.57q-.39.27-.75.54c-.5.36-.89.78-1.17 1.27S5 11.35 4.99 12h5v-1.15H6.43c.05-.17.14-.33.27-.49.13-.15.29-.29.46-.44m8.5-1.56c-.23-.35-.54-.57-.95-.65v-.02c.34-.13.6-.34.76-.63q.24-.435.24-1.02c0-.34-.06-.64-.19-.9s-.3-.47-.51-.64-.45-.3-.72-.38c-.27-.09-.54-.13-.82-.13-.36 0-.68.07-.96.2s-.53.32-.72.55c-.2.23-.36.51-.47.83s-.18.66-.19 1.04h1.15c-.01-.2.01-.39.06-.58s.12-.36.22-.51.22-.27.37-.36.32-.13.53-.13c.32 0 .59.1.79.3.21.2.31.46.31.79 0 .23-.05.43-.14.59s-.21.29-.35.38c-.15.09-.32.16-.51.19-.19.04-.38.05-.57.04v.93c.23-.01.45 0 .67.02s.42.08.59.17c.18.09.32.23.43.4.11.18.16.41.16.71q0 .66-.39 1.02c-.26.24-.58.36-.97.36-.45 0-.79-.16-1.02-.47s-.33-.7-.32-1.17H11c.01.4.06.77.17 1.1s.26.61.47.85c.21.23.46.42.77.54.31.13.67.19 1.08.19.34 0 .66-.05.96-.16s.57-.27.8-.47.41-.45.55-.74c.13-.27.2-.6.2-.97 0-.5-.11-.92-.34-1.27"];
})), Hv, Uv = o((() => {
	Hv = ["M1 0a1 1 0 0 0-1 1v3h2V2h2V0zM0 15v-3h2v2h2v2H1a1 1 0 0 1-1-1m15 1h-3v-2h2v-2h2v3a1 1 0 0 1-1 1m1-15v3h-2V2h-2V0h3a1 1 0 0 1 1 1M8 7l4.5-2.5-4.108-2.407a.82.82 0 0 0-.76 0L3.57 4.394zm4.955-2q.04.112.04.234v4.834a.71.71 0 0 1-.357.614L8.4 13V7.847zM7.594 7.743 3.04 5a1.2 1.2 0 0 0-.04.308v4.656c0 .254.136.488.356.614L7.594 13z"];
})), Wv, Gv = o((() => {
	Wv = ["M15 5h-3V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h3v-4h4v4h7c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1M5 10H2V7h3zm0-5H2V2h3zm5 5H7V7h3zm0-5H7V2h3zm4 9h-2v-2h2zm0-4h-2V7h2z"];
})), Kv, qv = o((() => {
	Kv = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8M6 14l1-5H4l6-7-1 5h3z"];
})), Jv, Yv = o((() => {
	Jv = ["M15 14h-1.35l-3.34-7.51 2.46-.95 1.45 3.21c.09.2.36.3.6.23q.15-.045.24-.15c.05-.08 1.23-1.56.87-4.2-.11-.79-.52-4.62-3.26-4.62-.93 0-1.68.62-1.67 1.37q0 .21.09.42l.87 1.92L.64 8.07v.01A.98.98 0 0 0 0 9c0 .55.45 1 1 1 .13 0 .25-.03.36-.07v.01l1.04-.4L3.67 14H2c-.55 0-1 .45-1 1s.45 1 1 1h13c.55 0 1-.45 1-1s-.45-1-1-1M4.27 8.81 7.14 7.7 5.2 12.08zM6.54 14 9 8.46 11.46 14z"];
})), Xv, Zv = o((() => {
	Xv = ["M11.99-.01h-3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-14c0-.55-.45-1-1-1m-6 5c-.28 0-.53.11-.71.29l-2 2a1.014 1.014 0 0 0 0 1.42l2 2a1.003 1.003 0 0 0 1.71-.71v-4c0-.55-.45-1-1-1"];
})), Qv, $v = o((() => {
	Qv = ["M14 3a1 1 0 1 0-2 0 1 1 0 0 0 2 0m-3.726 1.254c-.629.232-1.132.634-1.293 1.442C8.765 6.772 8.216 7.506 7.568 8c.648.493 1.197 1.228 1.413 2.304.161.808.664 1.21 1.293 1.442a3 3 0 1 1-.17 2.039 5 5 0 0 1-.51-.158c-1.076-.394-2.237-1.242-2.575-2.93-.161-.809-.664-1.211-1.293-1.443a3 3 0 1 1 0-2.508c.629-.232 1.132-.634 1.293-1.442.338-1.69 1.499-2.537 2.575-2.93q.256-.094.51-.159A3.001 3.001 0 0 1 16 3a3 3 0 0 1-5.726 1.254M13 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2M4 8a1 1 0 1 0-2 0 1 1 0 0 0 2 0"];
})), ey, ty = o((() => {
	ey = ["M2 8a1 1 0 1 0 2 0 1 1 0 0 0-2 0m3.83-1h4.34a3.001 3.001 0 1 1 0 2H5.83a3.001 3.001 0 1 1 0-2M13 7a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), ny, ry = o((() => {
	ny = ["M5 0h10c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1H8v-2h6V3H6v5H4V1c0-.55.45-1 1-1m2.5 5h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-5c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h2c.28 0 .5-.22.5-.5S9.78 6 9.5 6h-2c-.28 0-.5.22-.5.5s.22.5.5.5M11 8.5c0 .28-.165.5-.375.5h-2.25C8.165 9 8 8.78 8 8.5s.165-.5.375-.5h2.25c.21 0 .375.22.375.5M5 14c0 .55.45 1 1 1s1-.45 1-1v-4c0-.55-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1h1.59L.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L5 12.41z"];
})), iy, ay = o((() => {
	iy = ["M8 0c4.42 0 8 3.58 8 8 0 4.06-3.02 7.4-6.94 7.92-.02 0-.04.01-.06.01-.33.04-.66.07-1 .07-4.42 0-8-3.58-8-8 0-.55.45-1 1-1s1 .45 1 1c0 3.31 2.69 6 6 6 .71 0 1.37-.15 2-.38v.01c2.33-.82 4-3.02 4-5.63 0-3.31-2.69-6-6-6-1.78 0-3.36.78-4.46 2H5c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1s1 .45 1 1v1.74A7.95 7.95 0 0 1 8 0m1 12H7v-2h2zm0-3H7V4h2z"];
})), oy, sy = o((() => {
	oy = ["M6.006 3.101A6.98 6.98 0 0 0 4 8c0 1.866.736 3.611 2.002 4.9Q5.515 13 5 13a5 5 0 1 1 1.006-9.899M10 8a5 5 0 0 0-1.999-4l-.083.063A4.99 4.99 0 0 0 6 8c0 1.636.785 3.088 2.001 4A5 5 0 0 0 10 8M7.889 5.485l.11-.13.073.083C8.663 6.145 9 7.044 9 8l-.007.238a4 4 0 0 1-.92 2.324L8 10.643l-.072-.08A3.98 3.98 0 0 1 7 8c0-.935.322-1.815.889-2.515M12 8c0 1.865-.736 3.61-2 4.9q.485.1 1 .1a5 5 0 1 0-1-9.9A7 7 0 0 1 12 8"];
})), cy, ly = o((() => {
	cy = ["M8 16c-4.41 0-8-3.582-8-8.005S3.59 0 8 0c.94 0 1.86.16 2.74.48.52.19.79.76.6 1.281s-.76.79-1.28.6a6.007 6.007 0 0 0-8.05 5.644 6.007 6.007 0 0 0 8.05 5.643.997.997 0 0 1 1.28.6 1 1 0 0 1-.6 1.282c-.88.32-1.8.47-2.74.47m7.71-8.705c.18.18.29.43.29.71s-.11.53-.29.71l-3 3.002a1.003 1.003 0 0 1-1.71-.71c0-.28.11-.53.3-.71l1.29-1.291H5c-.55 0-1-.45-1-1.001s.45-1 1-1h7.59l-1.3-1.291a1.003 1.003 0 0 1 1.42-1.42z"];
})), uy, dy = o((() => {
	uy = ["m9.8.15 5.1 2.6c.7.3 1.1 1 1.1 1.8v6.8c0 .8-.5 1.6-1.3 1.9l-6.9 2.6c-.5.2-1.1.2-1.6 0l-5.1-2.6c-.7-.3-1.1-1-1.1-1.8v-6.8c0-.8.5-1.6 1.3-1.9L8.2.15c.5-.2 1.1-.2 1.6 0M12 6.193V9.9l-2 .8V6.943l-2 .75v6.018l6-2.261V5.443z"];
})), fy, py = o((() => {
	fy = ["M3 7H1a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2m6 0H7a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2m6 0h-2a1 1 0 1 0 0 2h2a1 1 0 1 0 0-2m-1-7h-2v3H4V0H2v4c0 .55.45 1 1 1h10c.55 0 1-.45 1-1zM2 16h2v-3h8v3h2v-4c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1z"];
})), my, hy = o((() => {
	my = ["M15 .95H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-12c0-.55-.45-1-1-1m-9 12H2v-6h4zm8 0H7v-6h7zm0-7H2v-3h12z"];
})), gy, _y = o((() => {
	gy = ["M1 16h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1M2 2h12v12H2zm7 11h4V3H9z"];
})), vy, yy = o((() => {
	vy = ["M15 1c.6 0 1 .4 1 1v11c0 .6-.4 1-1 1H1c-.6 0-1-.4-1-1V2c0-.6.4-1 1-1zM2 3v9h6V3zm7 0v9h5V3zm4 8h-3v-1h3zm0-2h-3V8h3zm0-2h-3V6h3zm0-2h-3V4h3z"];
})), by, xy = o((() => {
	by = ["M15 1H1c-.6 0-1 .4-1 1v11c0 .6.4 1 1 1h14c.6 0 1-.4 1-1V2c0-.6-.4-1-1-1M8 9H6V7h2zm0-3H6V4h2zm-6 6V3h3v9zm4 0v-2h2v2zm8 0H9v-2h5zm0-3H9V7h5zm0-3H9V4h5z"];
})), Sy, Cy = o((() => {
	Sy = ["M14.68 2.31A4.54 4.54 0 0 0 11.46.99c-1.15 0-2.31.44-3.19 1.32L.95 9.63c-.63.63-.95 1.46-.95 2.28a3.21 3.21 0 0 0 3.23 3.22c.83 0 1.66-.31 2.3-.95l7.31-7.32c.76-.77.76-1.98.01-2.73s-1.99-.76-2.75 0l-6.07 6.08c-.24.25-.24.65.01.9s.65.25.91.01l6.07-6.08c.25-.25.67-.25.91-.01.25.25.25.67 0 .92l-7.31 7.32c-.75.75-2.04.74-2.76.01-.75-.75-.73-2.02.01-2.76L9.2 3.21c1.24-1.24 3.35-1.26 4.58-.03 1.24 1.24 1.24 3.36 0 4.6l-7.12 7.13c-.24.25-.24.64.01.88.24.24.63.24.88.01v.01l7.13-7.13A4.4 4.4 0 0 0 16 5.51c0-1.16-.44-2.32-1.32-3.2"];
})), wy, Ty = o((() => {
	wy = ["M13 1H6C3.8 1 2 2.8 2 5s1.8 4 4 4v5c0 .6.4 1 1 1s1-.5 1-1V3h2v11c0 .6.4 1 1 1s1-.5 1-1V3h1c.5 0 1-.4 1-1s-.4-1-1-1"];
})), Ey, Dy = o((() => {
	Ey = ["M10 2v1H5V2c0-.55.45-1 1-1h-.22c.34-.6.98-1 1.72-1s1.38.4 1.72 1H9c.55 0 1 .45 1 1m2 0c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1H3c-.55 0-1-.45-1-1V3c0-.55.45-1 1-1h1v2h7V2zm-1.459 9.455-.225-.129c-.25.352-.434.567-.55.661a.5.5 0 0 1-.276.086c-.125 0-.25-.086-.376-.24-.208-.284-.492-1.048-.842-2.31.317-.557.575-.926.792-1.098a.77.77 0 0 1 .493-.189c.066 0 .183.026.358.069.167.051.326.068.45.068q.276.002.451-.188a.67.67 0 0 0 .184-.49c0-.214-.058-.386-.184-.506-.125-.129-.292-.189-.525-.189q-.3.002-.576.146c-.175.094-.409.309-.684.635-.209.24-.509.67-.918 1.27a5.9 5.9 0 0 0-.81-2.042l-2.16.377-.042.232c.159-.034.3-.051.41-.051.216 0 .391.094.533.283q.326.438.926 2.678c-.308.42-.525.695-.642.824-.192.206-.342.343-.467.403a.65.65 0 0 1-.326.078c-.092 0-.242-.052-.442-.155a1 1 0 0 0-.375-.094.7.7 0 0 0-.518.206.73.73 0 0 0-.2.523c0 .198.067.36.192.49.125.128.292.188.509.188q.31 0 .584-.128c.183-.086.409-.275.684-.558s.65-.739 1.135-1.365c.183.592.35 1.021.484 1.296.133.266.292.464.467.584s.392.18.659.18q.388 0 .776-.283c.334-.25.684-.661 1.051-1.262"];
})), Oy, ky = o((() => {
	Oy = ["M14.5 0h-13C.67 0 0 .67 0 1.5S.67 3 1.5 3H7v3H3.5C2.67 6 2 6.67 2 7.5S2.67 9 3.5 9H7v3H5.5c-.83 0-1.5.67-1.5 1.5S4.67 15 5.5 15h5c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5H9V9h3.5c.83 0 1.5-.67 1.5-1.5S13.33 6 12.5 6H9V3h5.5c.83 0 1.5-.67 1.5-1.5S15.33 0 14.5 0"];
})), Ay, jy = o((() => {
	Ay = ["m15 14.62-4-2.4V9.77c-.32.09-.66.15-1 .18v2.27l-4 2.4V8.71c-.38-.31-.72-.66-1-1.06v6.97l-4-2.4V8c.55 0 1-.45 1-1s-.45-1-1-1V1.38l3.15 1.89c.08-.34.18-.66.32-.97L.76.07v.01A.5.5 0 0 0 .5 0C.22 0 0 .22 0 .5v12c0 .18.1.33.25.42v.01l5 3v-.01c.07.05.16.08.25.08s.18-.03.25-.08v.01l4.74-2.85 4.74 2.85v-.01c.09.05.18.08.27.08.28 0 .5-.22.5-.5v-3.78c-.3.17-.63.28-1 .28zM2 5c0 .55.45 1 1 1s1-.45 1-1-.45-1-1-1-1 .45-1 1m6-1c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m7.75-.92-1.19-.72c.18.43.29.9.36 1.38l.08.04v3.39l1 1V3.5c0-.18-.1-.33-.25-.42M10 2c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m3.3 4.89c.44-.7.7-1.51.7-2.39C14 2.01 11.99 0 9.5 0S5 2.01 5 4.5 7.01 9 9.5 9c.88 0 1.69-.26 2.39-.7l2.41 2.41c.17.18.42.29.7.29a1.003 1.003 0 0 0 .71-1.71zM9.5 8C7.57 8 6 6.43 6 4.5S7.57 1 9.5 1 13 2.57 13 4.5 11.43 8 9.5 8"];
})), My, Ny = o((() => {
	My = ["M6 3H4c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1m6 0h-2c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), Py, Fy = o((() => {
	Py = ["M13.69 13.98c-.05-.24-.14-.5-.25-.76-.36-.86-1.12-1.33-2.69-2-.14-.06-.59-.25-.6-.25-.21-.09-.36-.15-.5-.22.02-.1.02-.2.03-.31 0-.04.01-.08.01-.13-.07-.06-.13-.12-.19-.19q.33-.48.54-1.05c.02-.06.02-.06.03-.1.29-.23.48-.57.59-.96.16-.33.25-.73.21-1.16-.03-.4-.16-.76-.37-1.03-.02-.53-.07-1.13-.15-1.54-.01-.06-.02-.12-.03-.19.23-.06.48-.09.72-.09.49 0 1.05.16 1.44.46.38.29.67.7.8 1.17.03.1.05.21.07.31.07.37.11.94.11 1.33v.05c.14.06.27.21.29.51.02.25-.07.45-.13.54-.05.21-.16.44-.38.48q-.03.15-.09.3c0 .01-.01.03-.01.03-.17.44-.43.83-.75 1.11v.14c.03.35-.09.59.83 1 .93.41 2.32.84 2.6 1.5.29.66.17 1.04.17 1.04h-2.3zm-1.17-.38c.37.86.22 1.36.22 1.36H.06s-.14-.5.22-1.36 2.13-1.43 3.31-1.96c1.17-.54 1.05-.86 1.09-1.3 0-.05.01-.11.01-.17-.41-.35-.75-.86-.97-1.45v-.01s-.01-.01-.01-.02c-.04-.12-.09-.26-.12-.39-.28-.05-.44-.36-.5-.64-.06-.12-.19-.39-.16-.71.04-.41.21-.6.39-.68v-.06c0-.51.05-1.26.14-1.74.02-.13.05-.27.09-.4.17-.6.54-1.13 1.02-1.51.5-.39 1.21-.6 1.84-.6s1.34.21 1.84.6c.48.38.85.91 1.02 1.52.04.13.07.27.09.4.09.48.14 1.22.14 1.73v.07c.18.08.34.27.37.67.03.32-.09.59-.16.71-.06.28-.21.58-.48.63q-.045.195-.12.39c0 .01-.01.04-.01.04-.22.58-.55 1.08-.95 1.45v.18c.04.45-.12.77 1.06 1.3s2.95 1.09 3.31 1.95"];
})), Iy, Ly = o((() => {
	Iy = ["M6 6V4c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v2c0 1.1.9 2 2 2h1c1.1 0 2-.9 2-2M3.5 6c-.28 0-.5-.22-.5-.5v-1c0-.28.22-.5.5-.5s.5.22.5.5v1c0 .28-.22.5-.5.5M13 8h-1c-1.1 0-2 .9-2 2v2c0 1.1.9 2 2 2h1c1.1 0 2-.9 2-2v-2c0-1.1-.9-2-2-2m0 3.5c0 .28-.22.5-.5.5s-.5-.22-.5-.5v-1c0-.28.22-.5.5-.5s.5.22.5.5zM12 3a1.003 1.003 0 0 0-1.87-.5l-5.99 9.98c-.09.15-.14.33-.14.52a1.003 1.003 0 0 0 1.87.5l5.99-9.98c.09-.15.14-.33.14-.52"];
})), Ry, zy = o((() => {
	Ry = ["M15.68 14.32c-.46-1.05-2.68-1.75-4.16-2.4s-1.28-1.05-1.33-1.59c-.01-.07-.01-.15-.01-.23.51-.45.92-1.07 1.19-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.34-.07.54-.44.61-.78.08-.14.23-.48.2-.87-.05-.5-.25-.73-.47-.82v-.09c0-.63-.06-1.55-.17-2.15A3.67 3.67 0 0 0 10.32.72C9.68.25 8.79-.01 8-.01S6.32.24 5.69.72c-.61.47-1.06 1.13-1.28 1.86-.05.17-.09.33-.11.5-.12.6-.17 1.51-.17 2.15v.08c-.24.09-.45.32-.5.83-.03.38.13.72.2.86.08.35.28.72.63.78.04.17.09.33.15.49 0 .01.01.02.01.03l.01.01c.27.72.7 1.35 1.22 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.37 1.59-1.48.65-3.7 1.35-4.16 2.4s-.27 1.67-.27 1.67h15.92c-.01.01.18-.61-.28-1.66"];
})), By, Vy = o((() => {
	By = ["M15.9 12.41c-.06-.06-3.37-2-3.48-2.05a.8.8 0 0 0-.32-.08c-.15 0-.34.11-.57.32-.23.22-.94 1.19-1.15 1.4-.21.22-.38.32-.52.32-.07 0-.15-.02-.25-.06s-1.16-.58-3.36-2.52c-2.2-1.93-2.49-3.2-2.5-3.55 0-.14.11-.31.32-.52.22-.21.45-.41.7-.6s.49-.4.7-.62c.22-.23.32-.42.32-.57 0-.11-.03-.21-.08-.32C5.66 3.46 3.66.15 3.59.08 3.44-.07 2.85 0 2.55.16.16 1.46-.03 3.2 0 3.89c.04.71.49 4.46 4.16 7.95C8.72 16.17 11.89 16 12.1 16c.69 0 2.82-.38 3.72-2.55.13-.32.25-.87.08-1.04"];
})), Hy, Uy = o((() => {
	Hy = ["M15.916 12.41c-.06-.06-3.373-2-3.483-2.05a.8.8 0 0 0-.32-.08c-.15 0-.34.11-.57.32-.23.22-.941 1.19-1.152 1.4-.21.22-.38.32-.52.32a.7.7 0 0 1-.25-.06c-.1-.04-1.161-.58-3.363-2.52-2.202-1.929-2.492-3.199-2.502-3.549 0-.14.11-.31.32-.52.22-.21.45-.41.7-.6s.491-.4.701-.62c.22-.23.32-.42.32-.57a.8.8 0 0 0-.08-.319c-.05-.1-2.051-3.41-2.121-3.48-.15-.15-.741-.08-1.041.08-2.392 1.3-2.582 3.04-2.552 3.73.04.71.49 4.459 4.163 7.948C8.73 16.17 11.903 16 12.113 16c.69 0 2.822-.38 3.723-2.55.13-.32.25-.87.08-1.04M13 7c0 .6-.4 1-1 1s-1-.4-1-1c0-1.1-.9-2-2-2-.6 0-1-.4-1-1s.4-1 1-1c2.2 0 4 1.8 4 4m3 0c0 .6-.4 1-1 1s-1-.4-1-1c0-2.8-2.2-5-5-5-.6 0-1-.4-1-1s.4-1 1-1c3.9 0 7 3.1 7 7"];
})), Wy, Gy = o((() => {
	Wy = ["M15.916 12.41c-.06-.06-3.373-2-3.483-2.05a.8.8 0 0 0-.32-.08c-.15 0-.34.11-.57.32-.23.22-.941 1.19-1.152 1.4-.21.22-.38.32-.52.32a.7.7 0 0 1-.25-.06c-.1-.04-1.161-.58-3.363-2.52-2.202-1.929-2.492-3.199-2.502-3.549 0-.14.11-.31.32-.52.22-.21.45-.41.7-.6s.491-.4.701-.62c.22-.23.32-.42.32-.57a.8.8 0 0 0-.08-.319c-.05-.1-2.051-3.41-2.121-3.48-.15-.15-.741-.08-1.041.08-2.392 1.3-2.582 3.04-2.552 3.73.04.71.49 4.459 4.163 7.948C8.73 16.17 11.903 16 12.113 16c.69 0 2.822-.38 3.723-2.55.13-.32.25-.87.08-1.04M15.71 4.3l-2-2A.97.97 0 0 0 13 2a1.003 1.003 0 0 0-.71 1.71l.29.29H9c-.55 0-1 .45-1 1s.45 1 1 1h3.59l-.29.29a1.003 1.003 0 0 0 1.42 1.42l2-2c.18-.18.29-.43.29-.71s-.12-.52-.3-.7"];
})), Ky, qy = o((() => {
	Ky = ["M3 0h8c.55 0 1 .45 1 1v.598A5.5 5.5 0 0 0 9.5 1a5.49 5.49 0 0 0-4.246 2H4v9h6v-.023a5.4 5.4 0 0 0 1.705-.447l.295.294V15c0 .55-.45 1-1 1H3c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1m3 14c0 .55.45 1 1 1s1-.45 1-1-.45-1-1-1-1 .45-1 1m5.89-3.7a4.5 4.5 0 0 1-2.39.7C7.01 11 5 8.99 5 6.5A4.49 4.49 0 0 1 6.668 3C7.44 2.374 8.425 2 9.5 2A4.49 4.49 0 0 1 14 6.5c0 .88-.26 1.69-.7 2.39l2.41 2.4A1.003 1.003 0 0 1 15 13c-.28 0-.53-.11-.7-.29zM12 6.5a2.5 2.5 0 1 0-5.002 0A2.5 2.5 0 0 0 12 6.5"];
})), Jy, Yy = o((() => {
	Jy = ["M7 1.08c-3.37.5-5.97 3.4-5.97 6.92 0 3.87 3.13 7 6.98 7 3.52 0 6.42-2.61 6.91-6H7zM8 0v8h8c0-4.42-3.58-8-8-8"];
})), Xy, Zy = o((() => {
	Xy = ["M4 4h3.273c.401 0 .727.326.727.727v6.546a.727.727 0 0 1-.727.727H4a4 4 0 0 1 0-8m12 4a4 4 0 0 1-4 4H9.636A.636.636 0 0 1 9 11.364V4.636C9 4.285 9.285 4 9.636 4H12a4 4 0 0 1 4 4m-4-2h-1v4h1a2 2 0 1 0 0-4"];
})), Qy, $y = o((() => {
	Qy = ["M9.41.92c-.51.51-.41 1.5.15 2.56L4.34 7.54C2.8 6.48 1.45 6.05.92 6.58l3.54 3.54-3.54 4.95 4.95-3.54 3.54 3.54c.53-.53.1-1.88-.96-3.42l4.06-5.22c1.06.56 2.04.66 2.55.15z"];
})), eb, tb = o((() => {
	eb = ["M2.477 7.618c.275.55-.263 1.505-.879 2.6-.634 1.126-1.35 2.4-1.35 3.53 0 .18.19.34.349.442.132.085.29.116.446.116h2.875a.79.79 0 0 0 .788-.789c0-.209.083-.41.231-.557l.13-.13a.67.67 0 0 0 .197-.475c0-.178.07-.35.197-.476l.081-.081a.95.95 0 0 0 .279-.673v-.163c0-.308.25-.558.557-.558h2.787c.615 0 1.114-.499 1.114-1.114V8.175c0-.616.5-1.115 1.115-1.115h3.344c.616 0 1.115-.499 1.115-1.114v-.894c0-.066.026-.13.073-.175A.24.24 0 0 0 16 4.702v-.394a.36.36 0 0 0-.074-.217.36.36 0 0 1-.073-.217v-.158a.557.557 0 0 0-.558-.557h-.278a.28.28 0 0 1-.279-.278.28.28 0 0 0-.279-.28h-.115a.4.4 0 0 0-.279.116l-.163.164a.95.95 0 0 1-.673.278H2.708a.56.56 0 0 1-.394-.163.557.557 0 0 0-.788 0 .56.56 0 0 1-.395.163H.805a.557.557 0 0 0-.557.557v1.967c0 .173-.042.342-.106.503-.128.328-.284.874.106.874q.136 0 .319-.012c.628-.033 1.583-.083 1.91.57m3.657 2.229a.244.244 0 0 1-.237-.304l.24-.962c.035-.14.241-.115.241.03 0 .067.055.121.122.121h.351q.084.001.155.047l.442.295c.254.17.556-.133.387-.386l-.295-.443a.3.3 0 0 1-.047-.154v-.195c0-.154.125-.278.279-.278h1.277c.074 0 .145.03.197.081l.15.15c.209.209.326.492.326.788v.537c0 .074-.03.145-.081.197l-.15.15a1.12 1.12 0 0 1-.788.326zM1.81 5h12.9a.25.25 0 0 1 .207.389l-.167.25a.25.25 0 0 1-.208.111H1.644a.25.25 0 0 1-.208-.389l.167-.25A.25.25 0 0 1 1.811 5"];
})), nb, rb = o((() => {
	nb = ["M4.57 7.02.3 11.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4.27-4.27c-.58-.35-1.07-.84-1.41-1.42M15 8c-.55 0-1 .45-1 1v.59l-2.57-2.57c-.34.58-.83 1.07-1.41 1.41L12.59 11H12c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-4-3c0-1.66-1.34-3-3-3S5 3.34 5 5s1.34 3 3 3 3-1.34 3-3M8 6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), ib, ab = o((() => {
	ib = ["M2 4H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m0-4H1C.45 0 0 .45 0 1v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m11.71 4.29C13.53 4.11 13.28 4 13 4s-.53.11-.71.29l-2 2a1.003 1.003 0 0 0 1.42 1.42l.29-.3V9c0 1.66-1.34 3-3 3H7.41l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2c-.18.18-.29.43-.29.71s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H9c2.76 0 5-2.24 5-5V7.41l.29.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM15 0H5c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), ob, sb = o((() => {
	ob = ["M12 8c0-.35-.19-.64-.46-.82l.01-.02-6-4-.01.02A.97.97 0 0 0 5 3c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1 .21 0 .39-.08.54-.18l.01.02 6-4-.01-.02c.27-.18.46-.47.46-.82"];
})), cb, lb = o((() => {
	cb = ["M4.293.293a1 1 0 0 1 1.414 1.414L4.414 3l1.293 1.293a1 1 0 0 1-1.414 1.414L3 4.414 1.707 5.707A1 1 0 0 1 .293 4.293L1.586 3 .293 1.707A1 1 0 0 1 1.707.293L3 1.586zM14.29 4.71 13 3.41V6a3 3 0 0 1-3 3H4a1 1 0 0 0-1 1v5a1 1 0 1 1-2 0v-5a3 3 0 0 1 3-3h6a1 1 0 0 0 1-1V3.41L9.71 4.7c-.18.19-.43.3-.71.3a1.003 1.003 0 0 1-.71-1.71l3-3c.18-.18.43-.29.71-.29s.53.11.71.29l3 3a1.003 1.003 0 0 1-1.42 1.42M16 13a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-2 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"];
})), ub, db = o((() => {
	ub = ["M13 7H9V3c0-.55-.45-1-1-1s-1 .45-1 1v4H3c-.55 0-1 .45-1 1s.45 1 1 1h4v4c0 .55.45 1 1 1s1-.45 1-1V9h4c.55 0 1-.45 1-1s-.45-1-1-1"];
})), fb, pb = o((() => {
	fb = ["M14 5c-.24 0-.47.05-.68.13L9.97 2.34c.01-.11.03-.22.03-.34 0-1.1-.9-2-2-2S6 .9 6 2c0 .04.01.08.01.12L2.88 4.21C2.61 4.08 2.32 4 2 4 .9 4 0 4.9 0 6c0 .74.4 1.38 1 1.72v4.55c-.6.35-1 .99-1 1.73 0 1.1.9 2 2 2 .74 0 1.38-.4 1.72-1h4.55c.35.6.98 1 1.72 1 1.1 0 2-.9 2-2 0-.37-.11-.7-.28-1L14 9c1.11-.01 2-.9 2-2s-.9-2-2-2m-4.01 7c-.73 0-1.37.41-1.71 1H3.73c-.18-.3-.43-.55-.73-.72V7.72c.6-.34 1-.98 1-1.72 0-.04-.01-.08-.01-.12l3.13-2.09c.27.13.56.21.88.21.24 0 .47-.05.68-.13l3.35 2.79c-.01.11-.03.22-.03.34 0 .37.11.7.28 1z"];
})), mb, hb = o((() => {
	mb = ["M5 8c0-1.66 1.34-3 3-3h4.59L11.3 6.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L12.59 3H8C5.24 3 3 5.24 3 8H1a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1zm-3 6v-4h4v4z"];
})), gb, _b = o((() => {
	gb = ["M8 8c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1S7 .45 7 1v6c0 .55.45 1 1 1m3-5.32v2.34c1.21.91 2 2.35 2 3.98 0 2.76-2.24 5-5 5s-5-2.24-5-5c0-1.63.79-3.06 2-3.98V2.68C2.64 3.81 1 6.21 1 9c0 3.87 3.13 7 7 7s7-3.13 7-7c0-2.79-1.64-5.19-4-6.32"];
})), vb, yb = o((() => {
	vb = ["M16 6.41c0-1.01-.49-1.94-1.29-2.49-.43-1.92-2.07-3.28-4-3.28-.46 0-.92.08-1.35.24C8.83.31 8.11 0 7.34 0c-.9 0-1.74.44-2.28 1.16-.12-.01-.24-.02-.36-.02-1.31 0-2.42.89-2.77 2.17C.78 3.72 0 4.84 0 6.13c0 .38.07.76.21 1.12C.07 7.6 0 7.98 0 8.36c0 1.11.58 2.11 1.51 2.63.54.56 1.27.87 2.03.87.49 0 .95-.12 1.37-.36a2.85 2.85 0 0 0 2.18 1.04c.52 0 1.03-.14 1.47-.42.49.39 1.07.65 1.69.73 1.04 1.15 1.84 2.63 1.84 2.64 0 0 .28.49.26.49.77 0 1.41-.16 1.32-1.04 0 .02-.73-2.31-.73-2.31.41-.21.75-.55.97-.98.9-.52 1.47-1.53 1.47-2.61 0-.24-.03-.48-.08-.71.45-.52.7-1.21.7-1.92m-1.23 1.02-.15-.16-.61-.67c-.27-.29-.54-.94-.58-1.39l-.1-1.01c-.05-.59-.94-.58-.91.11 0 .02.1 1.01.1 1.01.03.29.12.62.24.93-.06-.01-.12-.02-.18-.02 0 0-2.06-.1-2.05-.11-.58-.02-.71.97-.04 1l2.05.11c.42.02 1.04.3 1.29.58l.49.54.02.05c.08.21.12.44.12.66 0 .74-.41 1.41-1.07 1.75l-.16.08-.07.18c-.15.38-.48.66-.88.74l-.54.11.7 2.2c-.38-.61-.95-1.43-1.62-2.14l-.12-.13-.17-.01c-.41-.03-.8-.17-1.14-.38l1.36-1.18c.35-.31.83-.44.99-.39 0 0 .63.17.62.18.63.16.83-.74.23-.97l-.62-.18c-.55-.16-1.33.18-1.79.58l-1.53 1.33-.31.26c-.35.29-.75.44-1.2.44-.64 0-1.23-.33-1.58-.86V9.15c0-.4.17-.79.27-.85 0 0 .52-.34.51-.35.71-.53.18-1.23-.49-.89 0-.01-.52.35-.52.35-.26.15-.45.44-.58.77-.11-.11-.22-.2-.34-.28 0 0-1.53-1.01-1.53-1.02-.65-.45-1.2.51-.49.89 0-.01 1.51 1.02 1.51 1.02.37.24.62.78.62 1.09v.67c-.34.19-.63.29-.99.29-.54 0-1.05-.23-1.41-.63l-.05-.06-.07-.04c-.65-.34-1.05-1-1.05-1.73 0-.3.07-.6.2-.87l.12-.25L1.15 7c-.13-.27-.2-.56-.2-.87 0-.9.61-1.68 1.48-1.89l.31-.08.05-.34a1.926 1.926 0 0 1 2.38-1.58l.32.08.18-.31c.35-.6.99-.97 1.67-.97.44 0 .86.15 1.2.42l-.36.36v-.01l-.25.26c-.33.27-.74.42-.89.4 0 0-.67-.1-.67-.11-.67-.13-.87.86-.14 1.02.01 0 .67.11.67.11.02 0 .05 0 .07.01-.11.37-.15.77-.1 1.12 0 0 .17.99.15.99.11.52 1.06.36.93-.18 0-.01-.15-.99-.15-.99-.05-.37.12-.94.36-1.19l.39-.4c.05-.05.1-.09.15-.14l.74-.76c.4-.18.83-.27 1.27-.27 1.55 0 2.86 1.12 3.11 2.67l.04.25.21.12c.61.35.98 1 .98 1.7 0 .36-.1.7-.28 1.01"];
})), bb, xb = o((() => {
	bb = ["M10.91 8.34c.14-.21.36-.34.63-.34h1.29c.22 0 .41.07.52.26.09.16.08.33-.04.53l-2.49 2.87 2.77 3.54c.12.17.14.37.02.55-.11.17-.3.25-.5.25h-1.44a.69.69 0 0 1-.61-.35L9.4 13.51l-1.69 2.15c-.13.21-.36.34-.63.34H5.8c-.22 0-.41-.07-.52-.26-.09-.16-.08-.33.04-.53l2.71-3.48L4.3 6.99H3.03v3.47c0 .33-.26.56-.62.56h-.8c-.35-.01-.61-.23-.61-.56V.56c0-.33.26-.56.62-.56h3.11c.62 0 1.19.08 1.7.24s.96.39 1.34.69a3.2 3.2 0 0 1 1.21 2.53c0 .81-.25 1.5-.74 2.08-.37.44-.84.77-1.42 1.01L7.88 7.9c.04.04.07.08.08.1l1.49 1.9zM5.18 5c.62 0 1.08-.13 1.39-.37.29-.23.44-.71.44-1.16s-.15-.87-.44-1.1C6.26 2.12 5.8 2 5.18 2H2.99v3z"];
})), Sb, Cb = o((() => {
	Sb = ["M15 1H9c0-.55-.45-1-1-1S7 .45 7 1H1c-.55 0-1 .45-1 1s.45 1 1 1v8c0 .55.45 1 1 1h3.59L3.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L7 13.41V15c0 .55.45 1 1 1s1-.45 1-1v-1.59l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L10.41 12H14c.55 0 1-.45 1-1V3c.55 0 1-.45 1-1s-.45-1-1-1m-2 9H3V3h10z"];
})), wb, Tb = o((() => {
	wb = ["M12 2.02c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v1h8zm3 2H1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h1v-3h12v3h1c.55 0 1-.45 1-1v-6c0-.56-.45-1-1-1m-1 3h-2v-1h2zm-3 6H5v-3H3v4c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-4h-2z"];
})), Eb, Db = o((() => {
	Eb = ["M14 3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v1h12zm-2-3H4c-.55 0-1 .45-1 1h10c0-.55-.45-1-1-1m3 5H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-3 6c0 .55-.45 1-1 1H5c-.55 0-1-.45-1-1V9h1v2h6V9h1z"];
})), Ob, kb = o((() => {
	Ob = ["M2 6C.9 6 0 6.9 0 8s.9 2 2 2 2-.9 2-2-.9-2-2-2m4-3h9c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1m-4 9c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m13-5H6c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1m0 6H6c-.55 0-1 .45-1 1s.45 1 1 1h9c.55 0 1-.45 1-1s-.45-1-1-1M2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), Ab, jb = o((() => {
	Ab = ["M3 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m-.5-6.5a2.5 2.5 0 0 0 0 5 2.5 2.5 0 0 0 0-5M7 3h8c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1m8 10H7c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1M3 0C1.9 0 1 .9 1 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m12 6H7c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h8c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1"];
})), Mb, Nb = o((() => {
	Mb = ["M12.16 3.76c.15-.11.3-.16.47-.16.06 0 .17.02.34.06.16.04.31.06.43.06a.58.58 0 0 0 .6-.6c0-.19-.06-.33-.17-.44s-.28-.16-.49-.16c-.19 0-.37.04-.54.13s-.39.27-.65.55c-.2.21-.48.58-.87 1.11a5.2 5.2 0 0 0-.78-1.79l-2.05.32-.04.21c.15-.03.28-.04.39-.04.2 0 .37.08.5.25.21.26.5 1.03.88 2.33-.29.36-.49.6-.6.71q-.27.285-.45.36c-.09.04-.19.07-.3.07-.09 0-.23-.04-.42-.13a.9.9 0 0 0-.36-.09c-.2 0-.36.06-.49.18a.59.59 0 0 0-.19.46c0 .18.06.32.18.43s.28.16.48.16.38-.04.55-.12.39-.24.65-.49.62-.65 1.07-1.19c.18.52.33.89.46 1.13s.28.4.44.51c.17.1.37.16.62.16.24 0 .49-.08.74-.25.33-.21.66-.58 1.01-1.09l-.21-.11c-.23.31-.41.5-.52.57a.44.44 0 0 1-.26.07q-.18 0-.36-.21c-.2-.24-.46-.91-.8-2 .29-.49.54-.81.74-.96M6.37 5.83l.68-2.53h.83l.2-.64h-.84c.24-.91.56-1.59.96-2.01.24-.27.48-.4.71-.4.05 0 .08.01.11.04s.04.06.04.1-.03.11-.1.21c-.06.1-.1.2-.1.29q0 .195.15.33c.1.09.23.14.39.14.17 0 .31-.06.42-.17.12-.12.18-.27.18-.46 0-.21-.08-.39-.25-.52C9.57.07 9.3 0 8.93 0q-.885 0-1.59.48c-.48.32-.93.85-1.36 1.59-.15.26-.29.42-.42.49s-.35.11-.64.1l-.19.65h.81L4.35 7.68c-.2.72-.33 1.16-.4 1.33-.1.24-.26.45-.46.62a.48.48 0 0 1-.31.1c-.03 0-.06-.01-.08-.03l-.03-.03c0-.02.03-.06.09-.11.06-.06.09-.15.09-.26 0-.13-.05-.23-.14-.32-.1-.09-.23-.13-.41-.13-.21 0-.38.05-.51.16A.52.52 0 0 0 2 9.4c0 .16.08.3.23.42.16.12.4.18.74.18.53 0 .99-.13 1.4-.39s.76-.65 1.07-1.19c.3-.53.61-1.39.93-2.59m2.34 3.46A1 1 0 0 0 8 9c-.28 0-.53.11-.71.29l-2 2a1.003 1.003 0 0 0 1.42 1.42l.29-.3V15c0 .55.45 1 1 1s1-.45 1-1v-2.59l.29.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), Pb, Fb = o((() => {
	Pb = ["M15 8h-1.46l-1.7-2.55-.02.01A.98.98 0 0 0 11 5c-.43 0-.79.27-.93.65h-.01l-1.69 4.51-1.38-8.32h-.02A.99.99 0 0 0 6 1c-.41 0-.77.25-.92.61L2.34 8H1c-.55 0-1 .45-1 1s.45 1 1 1h2c.41 0 .77-.25.92-.61l1.65-3.86 1.44 8.63h.02c.08.47.47.84.97.84.43 0 .79-.27.93-.65h.01l2.31-6.17.92 1.38.02-.01c.17.26.46.45.81.45h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Ib, Lb = o((() => {
	Ib = ["M3.5 8a2.5 2.5 0 1 1 .608-4.926 4.002 4.002 0 0 1 7.382-1.03A3 3 0 1 1 12 8zM3 10a1 1 0 0 1 2 0v4a1 1 0 1 1-2 0zm7-1a1 1 0 0 0-1 1v5a1 1 0 1 0 2 0v-5a1 1 0 0 0-1-1m2 1a1 1 0 1 1 2 0v2a1 1 0 1 1-2 0zM7 9a1 1 0 0 0-1 1v2a1 1 0 1 0 2 0v-2a1 1 0 0 0-1-1"];
})), Rb, zb = o((() => {
	Rb = ["M11.48 4h1.11l-.29.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H11c-.32 0-.59.16-.77.38l-.01-.01L8.28 4.8l1.28 1.6zm2.23 6.29a1.003 1.003 0 0 0-1.42 1.42l.3.29h-1.11l-7.7-9.62h-.01A1 1 0 0 0 3 2H1c-.55 0-1 .45-1 1s.45 1 1 1h1.52l7.7 9.62.01-.01c.18.23.45.39.77.39h1.59l-.29.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71zM2.52 12H1c-.55 0-1 .45-1 1s.45 1 1 1h2c.32 0 .59-.16.77-.38l.01.01 1.94-2.42L4.44 9.6z"];
})), Bb, Vb = o((() => {
	Bb = ["M8 0q-.53 0-1.044.068a1 1 0 1 0 .26 1.983 6 6 0 0 1 1.569 0A1 1 0 0 0 9.044.068 8 8 0 0 0 8 0M4.348 3.24a1 1 0 1 0-1.219-1.587A8 8 0 0 0 1.653 3.13 1 1 0 0 0 3.24 4.348c.32-.416.693-.79 1.109-1.109m8.523-1.587a1 1 0 1 0-1.219 1.586c.416.32.79.693 1.109 1.109a1 1 0 1 0 1.586-1.219 8 8 0 0 0-1.476-1.476m3.061 5.303a1 1 0 1 0-1.983.26 6 6 0 0 1 0 1.569 1 1 0 0 0 1.983.259 8 8 0 0 0 0-2.088m-13.881.26a1 1 0 0 0-1.983-.26 8 8 0 0 0 0 2.088 1 1 0 1 0 1.983-.26 6 6 0 0 1 0-1.569M3.24 11.65a1 1 0 1 0-1.586 1.219 8 8 0 0 0 1.476 1.476 1 1 0 0 0 1.219-1.586A6 6 0 0 1 3.24 11.65m11.108 1.219a1 1 0 0 0-1.586-1.219c-.32.416-.693.79-1.109 1.109a1 1 0 1 0 1.219 1.586 8 8 0 0 0 1.476-1.476M9.045 15.93a1 1 0 1 0-.26-1.983 6 6 0 0 1-1.569 0 1 1 0 0 0-.259 1.983 8 8 0 0 0 2.088 0M8 6a2 2 0 1 1 0 4 2 2 0 0 1 0-4m4 2a4 4 0 1 0-8 0 4 4 0 0 0 8 0"];
})), Hb, Ub = o((() => {
	Hb = ["M8 3a5 5 0 1 1 0 10A5 5 0 0 1 8 3"];
})), Wb, Gb = o((() => {
	Wb = ["M3 15h10V1H3zm0 1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1zM8.707 3.293l2 2a1 1 0 0 1-1.414 1.414L8 5.414 6.707 6.707a1 1 0 0 1-1.414-1.414l2-2a1 1 0 0 1 1.414 0m-2 6L8 10.586l1.293-1.293a1 1 0 0 1 1.414 1.414l-2 2a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414"];
})), Kb, qb = o((() => {
	Kb = ["M1 3v10h14V3zM0 3a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm10.707 2.293 2 2a1 1 0 0 1 0 1.414l-2 2a1 1 0 0 1-1.414-1.414L10.586 8 9.293 6.707a1 1 0 0 1 1.414-1.414m-4 1.414L5.414 8l1.293 1.293a1 1 0 0 1-1.414 1.414l-2-2a1 1 0 0 1 0-1.414l2-2a1 1 0 0 1 1.414 1.414"];
})), Jb, Yb = o((() => {
	Jb = ["M1 3h14c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1m1 2v6h12V5z"];
})), Xb, Zb = o((() => {
	Xb = ["M12 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m3.71-6.71-3-3a1.003 1.003 0 0 0-1.42 1.42L12.59 4H5C2.24 4 0 6.24 0 9s2.24 5 5 5h4v-2H5c-1.66 0-3-1.34-3-3s1.34-3 3-3h7.59L11.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), Qb, $b = o((() => {
	Qb = ["M8 3a5 5 0 0 0-5 5 1 1 0 0 1-2 0 7 7 0 0 1 7-7c1.72 0 3.62.416 5 1.567V2a1 1 0 1 1 2 0v3a1 1 0 0 1-1 1h-3a1 1 0 1 1 0-2h.586C10.702 3.334 9.417 3 8 3m0 10a5 5 0 0 0 5-5 1 1 0 1 1 2 0 7 7 0 0 1-7 7c-1.72 0-3.62-.416-5-1.568V14a1 1 0 1 1-2 0v-3a1 1 0 0 1 1-1h3a1 1 0 1 1 0 2h-.586c.884.666 2.169 1 3.586 1"];
})), ex, tx = o((() => {
	ex = ["M5 10a1 1 0 1 1 0 2h-.586c.884.666 2.169 1 3.586 1 .646 0 1.262-.125 1.828-.348l1.505 1.505A7 7 0 0 1 8 15c-1.72 0-3.62-.416-5-1.567V14a1 1 0 1 1-2 0v-3a1 1 0 0 1 1-1zm9-3a1 1 0 0 1 1 1 7 7 0 0 1-.84 3.326l-1.505-1.504A5 5 0 0 0 13 8a1 1 0 0 1 1-1M3.347 6.17A5 5 0 0 0 3 8a1 1 0 0 1-2 0 7 7 0 0 1 .842-3.334zM14 1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-3a1 1 0 1 1 0-2h.586C10.702 3.334 9.417 3 8 3c-.645 0-1.26.123-1.826.345L4.669 1.84A7 7 0 0 1 8 1c1.72 0 3.62.416 5 1.567V2a1 1 0 0 1 1-1M2 1a1.003 1.003 0 0 0-.71 1.71l12 11.99c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L2.71 1.3A.97.97 0 0 0 2 1"];
})), nx, rx = o((() => {
	nx = ["M0 14a2 2 0 1 1 4 0 2 2 0 0 1-4 0M11 0a1 1 0 0 0-1 1v2.768L7.603 2.384a1 1 0 1 0-1 1.732L9 5.5 6.603 6.884a1 1 0 0 0 1 1.732L10 7.232V10a1 1 0 1 0 2 0V7.232l2.397 1.384a1 1 0 1 0 1-1.732L13 5.5l2.397-1.384a1 1 0 1 0-1-1.732L12 3.768V1a1 1 0 0 0-1-1"];
})), ix, ax = o((() => {
	ix = ["M13 6.5c0 .83.67 1.5 1.5 1.5S16 7.33 16 6.5 15.33 5 14.5 5 13 5.67 13 6.5M8.5 5c.83 0 1.5-.67 1.5-1.5S9.33 2 8.5 2 7 2.67 7 3.5 7.67 5 8.5 5M9 9.5c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5S11.33 8 10.5 8 9 8.67 9 9.5M4.5 8C5.33 8 6 7.33 6 6.5S5.33 5 4.5 5 3 5.67 3 6.5 3.67 8 4.5 8M15 12H3.26l12.03-8.59-.58-.81L2 11.67V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), ox, sx = o((() => {
	ox = ["M10.99 6.99h-6c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1m-3-7c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.68 6-6 6"];
})), cx, lx = o((() => {
	cx = ["M14 0H4c-.55 0-1 .45-1 1v3h2V2h3v12H5v-2H3v3c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14h-3V2h3zm-8.71-3.29a1.003 1.003 0 0 0 1.42-1.42L4.41 8 5.7 6.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L3 6.59l-1.29-1.3A1.003 1.003 0 0 0 .29 6.71L1.59 8 .29 9.29a1.003 1.003 0 0 0 1.42 1.42L3 9.41z"];
})), ux, dx = o((() => {
	ux = ["M4 9h4c.55 0 1-.45 1-1s-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1m11-9H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-5 14H2V2h8zm4 0h-3V2h3z"];
})), fx, px = o((() => {
	fx = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M5 14H2V2h3zm9 0H6V2h8zM8 9h4c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1"];
})), mx, hx = o((() => {
	mx = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2V6h12zm0-9H2V2h12zm-8 6h4c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1"];
})), gx, _x = o((() => {
	gx = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2v-3h12zm0-4H2V2h12zM6 7h4c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1s.45 1 1 1"];
})), vx, yx = o((() => {
	vx = ["M10 5c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1s-1 .45-1 1v1.74A7.95 7.95 0 0 0 8 0C3.58 0 0 3.58 0 8c0 4.06 3.02 7.4 6.94 7.92.02 0 .04.01.06.01.33.04.66.07 1 .07 4.42 0 8-3.58 8-8 0-.55-.45-1-1-1s-1 .45-1 1c0 3.31-2.69 6-6 6-.71 0-1.37-.15-2-.38v.01C3.67 12.81 2 10.61 2 8c0-3.31 2.69-6 6-6 1.77 0 3.36.78 4.46 2H11c-.55 0-1 .45-1 1"];
})), bx, xx = o((() => {
	bx = ["M6 5c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1s1 .45 1 1v1.74A7.95 7.95 0 0 1 8 0c4.42 0 8 3.58 8 8 0 4.06-3.02 7.4-6.94 7.92-.02 0-.04.01-.06.01-.33.04-.66.07-1 .07-4.42 0-8-3.58-8-8 0-.55.45-1 1-1s1 .45 1 1c0 3.31 2.69 6 6 6 .71 0 1.37-.15 2-.38v.01c2.33-.82 4-3.02 4-5.63 0-3.31-2.69-6-6-6-1.77 0-3.36.78-4.46 2H5c.55 0 1 .45 1 1"];
})), Sx, Cx = o((() => {
	Sx = ["M6.6 3.3C6.1 3.1 5.6 3 5 3 2.2 3 0 5.2 0 8s2.2 5 5 5c.6 0 1.1-.1 1.6-.3C5.3 11.6 4.5 9.9 4.5 8s.8-3.6 2.1-4.7M8 4c-1.2.9-2 2.4-2 4s.8 3.1 2 4c1.2-.9 2-2.3 2-4s-.8-3.1-2-4m3-1c-.6 0-1.1.1-1.6.3 1.3 1.2 2.1 2.9 2.1 4.7s-.8 3.6-2.1 4.7c.5.2 1 .3 1.6.3 2.8 0 5-2.2 5-5s-2.2-5-5-5"];
})), wx, Tx = o((() => {
	wx = ["M5.71 3c0 1.1.96 2 2.14 2C9.04 5 10 3.96 10 3c0-1.96-1.47-3-2.14-3H5c0 1.96 2.68 1.4.71 3m2.5 3 .01.01s0-.01-.01-.01m6.5 8.29L10 9.59V7c0-.55-.45-1-1-1H7c-.55 0-1 .45-1 1v2.58l-4.71 4.7c-.18.19-.29.44-.29.72a1.003 1.003 0 0 0 1.71.71L6 12.42V15c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-2.58l3.29 3.29a1.003 1.003 0 0 0 1.42-1.42"];
})), Ex, Dx = o((() => {
	Ex = ["M6.6 3.3C5.3 4.4 4.5 6.1 4.5 8s.8 3.6 2.1 4.7c-.5.2-1 .3-1.6.3-2.8 0-5-2.2-5-5s2.2-5 5-5c.6 0 1.1.1 1.6.3m-1.96 8.68C3.92 10.83 3.5 9.46 3.5 8s.42-2.83 1.14-3.98C2.6 4.2 1 5.91 1 8s1.6 3.8 3.64 3.98M8 4c-1.2.9-2 2.4-2 4s.8 3.1 2 4c1.2-.9 2-2.3 2-4s-.8-3.1-2-4m3-1c2.8 0 5 2.2 5 5s-2.2 5-5 5c-.6 0-1.1-.1-1.6-.3 1.3-1.1 2.1-2.9 2.1-4.7s-.8-3.5-2.1-4.7c.5-.2 1-.3 1.6-.3"];
})), Ox, kx = o((() => {
	Ox = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 12c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4"];
})), Ax, jx = o((() => {
	Ax = ["M6 12C4.397 7.46 4.415 4.465 8 0c3.585 4.485 3.602 7.48 2 12zm3-7a1 1 0 1 0-2 0 1 1 0 0 0 2 0m-7 8.022L3 9l1-1c.076 1.317.635 2.954.946 3.864l.054.158zm9-1 .054-.158c.31-.91.87-2.547.946-3.864l1 1 1 4.022zM7 13h2c0 1.5-.5 2.5-1 3-.5-.5-1-1.5-1-3"];
})), Mx, Nx = o((() => {
	Mx = ["M3.992 10c2-5 5-9 11-9 0 6-4 9-9 11zm7.714-4.285a1 1 0 1 0-1.414-1.414 1 1 0 0 0 1.414 1.414m-6.555-.218c-.745 1.142-1.369 2.397-1.91 3.698L-.009 8l3-2zM7.992 16l-1.236-3.232c1.3-.539 2.552-1.158 3.694-1.898L9.992 13zm-4.931-4.94L5 13c-.992.991-2.186 1.154-3.001 1-.154-.815.07-1.948 1.06-2.94"];
})), Px, Fx = o((() => {
	Px = ["M2 1v5H1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-3h3a1 1 0 0 0 1-1V3c0-.55-.45-1-1-1H9.42L7.71.3A.97.97 0 0 0 7 0H3c-.55 0-1 .45-1 1m6.596 3H14v6h-2V7a1 1 0 0 0-1-1H4V2h2.584zM7 8h2l-4 6H3z"];
})), Ix, Lx = o((() => {
	Ix = ["M14.635 7.672a.61.61 0 0 1-.03.828l-3.462 3.46a.609.609 0 0 0 .861.862l3.461-3.461c.677-.677.716-1.76.091-2.485l-2.652-3.072h1.105a.609.609 0 1 0 0-1.217h-2.435a.61.61 0 0 0-.609.609V5.63a.609.609 0 0 0 1.218 0v-.798zm-4.342-.379a1 1 0 0 1 0 1.414L6.05 12.95a1 1 0 0 1-1.414 0L.393 8.707a1 1 0 0 1 0-1.414L4.636 3.05a1 1 0 0 1 1.414 0z"];
})), Rx, zx = o((() => {
	Rx = ["M1.365 7.672a.61.61 0 0 0 .03.828l3.461 3.46a.609.609 0 1 1-.86.862L.535 9.36a1.826 1.826 0 0 1-.091-2.485l2.652-3.072H1.991a.609.609 0 0 1 0-1.217h2.435c.336 0 .609.272.609.609V5.63a.609.609 0 1 1-1.218 0v-.798zm13.928-.379a1 1 0 0 1 0 1.414L11.05 12.95a1 1 0 0 1-1.414 0L5.393 8.707a1 1 0 0 1 0-1.414L9.636 3.05a1 1 0 0 1 1.414 0z"];
})), Bx, Vx = o((() => {
	Bx = ["M12 2h-1.59l.29-.29c.19-.18.3-.43.3-.71A1.003 1.003 0 0 0 9.29.29l-2 2C7.11 2.47 7 2.72 7 3s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H12c.55 0 1 .45 1 1v3c0 .55.45 1 1 1s1-.45 1-1V5c0-1.66-1.34-3-3-3M5.71 5.29A1 1 0 0 0 5 5H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V9c0-.28-.11-.53-.29-.71zM7 14H2V7h2v2c0 .55.45 1 1 1h2z"];
})), Hx, Ux = o((() => {
	Hx = ["M8 6H2c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1m-1 8H3V8h4zm5-12h-1.59l.29-.29c.19-.18.3-.43.3-.71A1.003 1.003 0 0 0 9.29.29l-2 2C7.11 2.47 7 2.72 7 3s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H12c.55 0 1 .45 1 1v3c0 .55.45 1 1 1s1-.45 1-1V5c0-1.66-1.34-3-3-3"];
})), Wx, Gx = o((() => {
	Wx = ["m11.669 5.066.099.189q.17.32.367.661c.226.39.468.78.709 1.151l-.198-.004-.48-.004c-1.745.003-2.369.233-2.369.688 0 .053.226.19 1.038.436l.84.24C13.9 9.064 15 9.83 15 11.63c0 2.123-1.607 3.122-4.027 3.366-.651.065-1.266.075-2.043.05l-.958-.035H5.196l.268-.406a56 56 0 0 0 .998-1.593h1.636l.572.023c.857.036 1.475.034 2.103-.03 1.526-.153 2.227-.59 2.227-1.375 0-.531-.402-.84-1.66-1.22l-.691-.198c-1.04-.293-1.764-.562-2.222-.946C8.8 8.366 9 7.612 9 6.997a5 5 0 0 0-.184-1.334c.645-.395 1.598-.562 2.853-.597M4 3a4.007 4.007 0 0 1 4 3.997C8 9.21 4 15 4 15l-.416-.62C2.56 12.827 0 8.767 0 6.997A4 4 0 0 1 4 3m0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 4 5m10-4c1.103 0 1.996.896 2 1.999C16 4.105 14 7 14 7l-.293-.44C13.15 5.707 12 3.838 12 2.999 12 1.896 12.897 1 14 1"];
})), Kx, qx = o((() => {
	Kx = ["M2 8a6 6 0 0 1 6-6V0a8 8 0 1 0 6 13.292V14a1 1 0 1 0 2 0v-3a1 1 0 0 0-1-1h-3a1 1 0 1 0 0 2h.472A5.98 5.98 0 0 1 8 14a6 6 0 0 1-6-6m14-.07-2 .02a6 6 0 0 0-.218-1.557l1.928-.532a8 8 0 0 1 .29 2.07m-1.105-3.992-1.723 1.016a6 6 0 0 0-.965-1.233l1.4-1.427c.496.486.93 1.038 1.288 1.644m-2.956-2.901-.986 1.74a6 6 0 0 0-1.451-.588l.501-1.936a8 8 0 0 1 1.936.784m-4.384 4.13A1 1 0 0 0 6 6v4a1 1 0 0 0 1.555.832l3-2a1 1 0 0 0 0-1.664z"];
})), Jx, Yx = o((() => {
	Jx = ["M3 9c0-.6.4-1 1-1s1 .4 1 1c0 1.1.9 2 2 2 .6 0 1 .4 1 1s-.4 1-1 1c-2.2 0-4-1.8-4-4M0 9c0-.6.4-1 1-1s1 .4 1 1c0 2.8 2.2 5 5 5 .6 0 1 .4 1 1s-.4 1-1 1c-3.9 0-7-3.1-7-7m7 1c-.6 0-1-.4-1-1s.4-1 1-1 1 .4 1 1-.4 1-1 1m1.3-2.8c-.4-.4-.4-1 0-1.4l4.5-4.5c.4-.4 1-.4 1.4 0l.5.5c.4.4.4 1 0 1.4l-4.5 4.5c-.4.4-1 .4-1.4 0zM5.2.3c.4-.4 1-.4 1.4 0l2.1 2.1c.4.4.4 1 0 1.4l-.9.9c-.4.4-1 .4-1.4 0L4.3 2.6c-.4-.4-.4-1 0-1.4zm7 7c.4-.4 1-.4 1.4 0l2.1 2.1c.4.4.4 1 0 1.4l-.9.9c-.4.4-1 .4-1.4 0l-2.1-2.1c-.4-.4-.4-1 0-1.4z"];
})), Xx, Zx = o((() => {
	Xx = ["M6.71 9.29a1.003 1.003 0 0 0-1.42 1.42l2 2a.997.997 0 0 0 1.6-.27h.01l2-4h-.01c.06-.13.11-.28.11-.44 0-.55-.45-1-1-1-.39 0-.72.23-.89.56H9.1l-1.38 2.76zM9 0H3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V5zm3 14H4V2h4v4h4z"];
})), Qx, $x = o((() => {
	Qx = ["M15 12H2V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m-.5-7c.83 0 1.5-.67 1.5-1.5S15.33 2 14.5 2 13 2.67 13 3.5 13.67 5 14.5 5m-3 4c.83 0 1.5-.67 1.5-1.5S12.33 6 11.5 6 10 6.67 10 7.5 10.67 9 11.5 9m-4-2C8.33 7 9 6.33 9 5.5S8.33 4 7.5 4 6 4.67 6 5.5 6.67 7 7.5 7m-3 4c.83 0 1.5-.67 1.5-1.5S5.33 8 4.5 8 3 8.67 3 9.5 3.67 11 4.5 11"];
})), eS, tS = o((() => {
	eS = ["m15.55 13.43-2.67-2.68a6.94 6.94 0 0 0 1.11-3.76c0-3.87-3.13-7-7-7s-7 3.13-7 7 3.13 7 7 7c1.39 0 2.68-.42 3.76-1.11l2.68 2.67a1.498 1.498 0 1 0 2.12-2.12m-8.56-1.44c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), nS, rS = o((() => {
	nS = ["M13.5 11c-.51 0-.98.15-1.38.42l-2.4-2.41c.17-.3.28-.64.28-1.01s-.11-.71-.28-1.01l2.41-2.41c.39.27.86.42 1.37.42a2.5 2.5 0 0 0 0-5A2.5 2.5 0 0 0 11 2.5c0 .51.15.98.42 1.38l-2.41 2.4C8.71 6.11 8.37 6 8 6s-.71.11-1.01.28l-2.41-2.4c.27-.4.42-.87.42-1.38a2.5 2.5 0 0 0-5 0A2.5 2.5 0 0 0 2.5 5c.51 0 .98-.15 1.38-.42l2.41 2.41C6.11 7.29 6 7.63 6 8s.11.71.28 1.01l-2.41 2.41c-.39-.27-.86-.42-1.37-.42a2.5 2.5 0 0 0 0 5A2.5 2.5 0 0 0 5 13.5c0-.51-.15-.98-.42-1.38l2.41-2.41c.3.18.64.29 1.01.29s.71-.11 1.01-.28l2.41 2.41c-.27.39-.42.86-.42 1.37a2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0-2.5-2.5m0-10c.83 0 1.5.67 1.5 1.5S14.33 4 13.5 4 12 3.33 12 2.5 12.67 1 13.5 1m-11 3C1.67 4 1 3.33 1 2.5S1.67 1 2.5 1 4 1.67 4 2.5 3.33 4 2.5 4m0 11c-.83 0-1.5-.67-1.5-1.5S1.67 12 2.5 12s1.5.67 1.5 1.5S3.33 15 2.5 15m11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5"];
})), iS, aS = o((() => {
	iS = ["m15.55 13.43-2.67-2.67c.7-1.09 1.11-2.38 1.11-3.77 0-3.87-3.13-7-7-7s-7 3.13-7 7 3.13 7 7 7c1.39 0 2.68-.41 3.77-1.11l2.67 2.67a1.498 1.498 0 1 0 2.12-2.12m-8.56-1.44c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5m2.5-6h-5c-.28 0-.5.22-.5.5s.22.5.5.5h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5m0-2h-5c-.28 0-.5.22-.5.5s.22.5.5.5h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5m0 4h-5c-.28 0-.5.22-.5.5s.22.5.5.5h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5"];
})), oS, sS = o((() => {
	oS = ["M9 4H5c-.55 0-1 .45-1 1s.45 1 1 1h1v3c0 .55.45 1 1 1s1-.45 1-1V6h1c.55 0 1-.45 1-1s-.45-1-1-1m6.56 9.44-2.67-2.67C13.59 9.68 14 8.39 14 7c0-3.87-3.13-7-7-7S0 3.13 0 7s3.13 7 7 7c1.39 0 2.68-.41 3.77-1.11l2.67 2.67a1.498 1.498 0 1 0 2.12-2.12M7 12c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), cS, lS = o((() => {
	cS = ["M15 4H1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m-1 6H8V6h6z"];
})), uS, dS = o((() => {
	uS = ["M16 15c0-.28-.12-.52-.31-.69l.02-.02-3.12-3.12 3.41-.84-8.05-2.86c.03-.09.05-.17.05-.27V2c0-.55-.45-1-1-1H3c0-.55-.45-1-1-1S1 .45 1 1c-.55 0-1 .45-1 1s.45 1 1 1v4c0 .55.45 1 1 1h5.2c.1 0 .18-.02.27-.05L10.33 16l.85-3.41 3.12 3.12.02-.02c.16.19.4.31.68.31.04 0 .07-.02.1-.02s.06.02.1.02c.44 0 .8-.36.8-.8 0-.04-.02-.07-.02-.1s.02-.06.02-.1M6 6H3V3h3z"];
})), fS, pS = o((() => {
	fS = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6m0-9C6.34 5 5 6.34 5 8s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3"];
})), mS, hS = o((() => {
	mS = ["M10 2H6V0h4zM0 6v4h2V6zm6 10h4v-2H6zm8-6V6h2v4zM2 0H1a1 1 0 0 0-1 1v3h2V2h2V0zM0 15v-3h2v2h2v2H1a1 1 0 0 1-1-1m14 1h1a1 1 0 0 0 1-1v-3h-2v2h-2v2zm2-15v3h-2V2h-2V0h3a1 1 0 0 1 1 1"];
})), gS, _S = o((() => {
	gS = ["M6 2h4V0H6zm-6 8V6h2v4zM1 0h3v2H2v2H0V1a1 1 0 0 1 1-1M0 14v1a1 1 0 0 0 1 1h3v-2H2v-2H0zm10 0v2H6v-2zm6-8h-2v4h2zm-1 10h-3v-2h2v-2h2v3a1 1 0 0 1-1 1m1-14V1a1 1 0 0 0-1-1h-3v2h2v2h2zM7 5a1 1 0 0 1 2 0v2h2a1 1 0 1 1 0 2H9v2a1 1 0 1 1-2 0V9H5a1 1 0 0 1 0-2h2z"];
})), vS, yS = o((() => {
	vS = ["M10 2H6V0h4zM0 6v4h2V6zm6 10h4v-2H6zm8-10h2v4h-2zM2 0H1a1 1 0 0 0-1 1v3h2V2h2V0zM0 15v-3h2v2h2v2H1a1 1 0 0 1-1-1m14 1h1a1 1 0 0 0 1-1v-3h-2v2h-2v2zM8.72 9.224l-1.943-1.94 5.268-5.265 1.934 1.949zm-.685.684L5 11l1.1-3.01zM13.657.4c.252-.244.597-.401.975-.401.763 0 1.376.62 1.368 1.367 0 .385-.15.723-.401.974l-1.132 1.132-1.942-1.94z"];
})), bS, xS = o((() => {
	bS = ["M10 2H6V0h4zM0 6v4h2V6zm6 10h4v-2H6zm8-6V6h2v4zM1 0a1 1 0 0 0-1 1v3h2V2h2V0zM0 15v-3h2v2h2v2H1a1 1 0 0 1-1-1m15 1a1 1 0 0 0 1-1v-3h-2v2h-2v2zm1-15v3h-2V2h-2V0h3a1 1 0 0 1 1 1M5 9a1 1 0 0 1 0-2h6a1 1 0 1 1 0 2z"];
})), SS, CS = o((() => {
	SS = ["M7.303 15.71c.18.18.43.29.7.29s.53-.11.71-.29l2.997-2.99a1.003 1.003 0 0 0-1.42-1.42l-1.288 1.29L9 9h6a1 1 0 1 0 0-2H9V5h6a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6v2H1a1 1 0 1 0 0 2h6v3.586h.003v.004l-1.29-1.29a1 1 0 0 0-.699-.29 1.003 1.003 0 0 0-.71 1.71z"];
})), wS, TS = o((() => {
	wS = ["M15.399 9.01 1.527 15.875c-.535.267-1.175.081-1.421-.427A.95.95 0 0 1 0 15v-5l8-2-8-2V1c0-.528.407-1 1.004-1 .169 0 .416.04.567.116L15.403 7.07a1.084 1.084 0 0 1-.005 1.939"];
})), ES, DS = o((() => {
	ES = ["M15 7.5c-.8 0-1.5-.4-2-1l-1.2 1.2c-.4.5-1.1.7-1.8.7-1.4.1-2.5-1-2.5-2.4 0-.7.3-1.3.7-1.8L9.5 3c-.6-.5-1-1.2-1-2 0-.3.1-.7.2-1H8C3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8v-.7c-.3.1-.6.2-1 .2M15 0h-4c-.6 0-1 .5-1 1s.4 1 1 1h1.6L9.3 5.3c-.2.2-.3.4-.3.7 0 .5.4 1 1 1 .3 0 .5-.1.7-.3L14 3.4V5c0 .6.4 1 1 1 .5 0 1-.4 1-1V1c0-.5-.4-1-1-1"];
})), OS, kS = o((() => {
	OS = ["M6 9H2c-.55 0-1 .45-1 1s.45 1 1 1h1.59L.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L5 12.41V14c0 .55.45 1 1 1s1-.45 1-1v-4c0-.55-.45-1-1-1m8 .5c-.56 0-1.06.23-1.42.59l-2.13-1.24L8.99 8l3.59-2.09A2.002 2.002 0 0 0 16 4.5c0-1.1-.9-2-2-2s-2 .9-2 2c0 .19.03.37.08.54L8.5 7.13v-3.2c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S6 .9 6 2c0 .93.64 1.71 1.5 1.93v3.2l-.88-.52-2.7-1.57c.05-.17.08-.35.08-.54 0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.56 0 1.06-.23 1.42-.59l2.13 1.24 3.84 2.24 2.7 1.57q-.09.255-.09.54c0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2"];
})), AS, jS = o((() => {
	AS = ["M6 9H2c-.55 0-1 .45-1 1s.45 1 1 1h1.59L.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L5 12.41V14c0 .55.45 1 1 1s1-.45 1-1v-4c0-.55-.45-1-1-1m9.55-5.83-4.49-3A.98.98 0 0 0 9.99.15L5.53 2.82 1.56.17A1.003 1.003 0 0 0 0 1v6h2V2.87l2.94 1.96.06.03V7h1V4.86s.01 0 .01-.01L10 2.47v8.67s-.01 0-.01.01l-.99.58v2.33l1.47-.88 3.97 2.65A1.003 1.003 0 0 0 16 15V4c0-.35-.18-.65-.45-.83M14 13.13l-2.94-1.96c-.02-.01-.04-.02-.05-.03v-8.6l3 2v8.59z"];
})), MS, NS = o((() => {
	MS = ["M10.586 11a1 1 0 0 1 .707.293L13 13h2v2H1v-2h2l1.707-1.707A1 1 0 0 1 5.414 11zM8 8a1 1 0 1 1 0 2 1 1 0 0 1 0-2M5.2 6.153c1.07-1.428 4.238-1.628 5.568-.04.35.43.29 1.06-.13 1.41-.43.35-1.06.29-1.41-.13-.47-.57-2.11-.47-2.43-.04-.33.44-.96.53-1.4.2s-.529-.96-.199-1.4M2.302 4.278c3.12-3.039 8.278-3.039 11.387.01.4.38.4 1.01.02 1.41s-1.02.409-1.41.019c-2.339-2.289-6.258-2.289-8.598 0-.4.38-1.04.36-1.42-.03a.996.996 0 0 1 .02-1.41"];
})), PS, FS = o((() => {
	PS = ["M10.68 7.9c.44.54 1.07.92 1.79 1.05l-2.76 2.76c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L5 8.41l-3 3V13h13c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1s1 .45 1 1v4.59l2.29-2.3C4.47 6.11 4.72 6 5 6s.53.11.71.29L9 9.59zM15 3c.55 0 1 .45 1 1s-.45 1-1 1h-1v1c0 .55-.45 1-1 1s-1-.45-1-1V5h-1c-.55 0-1-.45-1-1s.45-1 1-1h1V2c0-.55.45-1 1-1s1 .45 1 1v1z"];
})), IS, LS = o((() => {
	IS = ["M9.94 9.64c.65.23 1.34.36 2.06.36.14 0 .29-.01.43-.01L9.7 12.71c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L5 9.41l-3 3V14h12.99c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V5c0-.55.45-1 1-1s1 .45 1 1v4.59l2.29-2.3C4.47 7.11 4.72 7 5 7s.53.11.71.29L9 10.59zm4.73-6.44h.92c.22 0 .4.18.4.4v.8c0 .22-.18.4-.4.4h-.93c-.06.2-.14.38-.24.55l.66.65c.15.15.15.4 0 .55l-.54.55c-.15.15-.4.15-.55 0l-.65-.65c-.17.1-.36.18-.55.24v.91c0 .22-.18.4-.4.4h-.8c-.22 0-.4-.18-.4-.4v-.93c-.18-.06-.36-.13-.52-.22l-.68.68c-.15.16-.41.16-.57 0l-.56-.56a.417.417 0 0 1 0-.57l.68-.68c-.08-.16-.16-.33-.22-.52h-.93c-.22 0-.4-.18-.4-.4v-.8c0-.22.18-.4.4-.4h.93c.06-.2.14-.38.24-.55l-.65-.64a.39.39 0 0 1 0-.55l.54-.55a.38.38 0 0 1 .54 0l.65.65c.18-.1.36-.18.55-.24V.4c0-.22.18-.4.4-.4h.8c.22 0 .4.18.4.4v.93c.18.06.35.14.52.22l.68-.68c.15-.16.41-.16.57 0l.57.57c.15.16.15.41 0 .57l-.68.68c.09.16.16.33.22.51m-4.18.8c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5-.67-1.5-1.5-1.5c-.82 0-1.5.67-1.5 1.5"];
})), RS, zS = o((() => {
	RS = ["M10.66 7.92c.44.54 1.07.91 1.8 1.03L9.71 11.7c-.18.19-.43.3-.71.3s-.53-.11-.71-.3L5 8.41l-3 3V13h13c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1s1 .45 1 1v4.59l2.29-2.3C4.47 6.11 4.72 6 5 6s.53.11.71.29L9 9.59zM12.3 5.3l.3-.3H8c-.6 0-1-.4-1-1s.4-1 1-1h4.6l-.3-.3c-.2-.2-.3-.4-.3-.7 0-.6.5-1 1-1 .3 0 .5.1.7.3l2 2c.2.2.3.4.3.7s-.1.5-.3.7l-2 2c-.2.2-.4.3-.7.3-.6 0-1-.4-1-1 0-.3.1-.5.3-.7"];
})), BS, VS = o((() => {
	BS = ["M9.29 9.3c.3.62.8 1.12 1.42 1.41l-1 1c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L5 8.41l-3 3V13h13c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1s1 .45 1 1v4.59l2.29-2.3C4.47 6.11 4.72 6 5 6s.53.11.71.29L9 9.59zM15.48 1c.31 0 .52.26.52.57 0 .16-.06.3-.17.41l-2.86 2.73v2.63c0 .16-.06.3-.17.41l-.82 1.1c-.1.1-.25.17-.41.17-.31 0-.57-.26-.57-.57V4.71L8.17 1.98A.57.57 0 0 1 8 1.57c0-.31.26-.57.57-.57z"];
})), HS, US = o((() => {
	HS = ["M9.6 8.94a4.9 4.9 0 0 0 1.82.01c.1-.01.22-.04.39-.08l.23-.07c.04-.01.08-.02.11-.04l.22.22-2.7 2.72c-.18.19-.43.3-.71.3s-.53-.11-.71-.3L4.98 8.41l-2.99 3V13h12.94c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V3.99c0-.55.45-1 1-1s1 .45 1 1v4.59l2.28-2.3c.17-.18.42-.29.7-.29s.53.11.7.29l3.28 3.3zm6.22-.41c.1.12.17.27.18.44 0 .34-.27.61-.61.61a.57.57 0 0 1-.43-.18l-2.24-2.25c-.13.08-.26.16-.4.23-.02.01-.05.02-.07.03-.14.06-.27.12-.42.17h-.01c-.14.05-.29.08-.44.11-.04.01-.08.02-.11.02-.15.02-.3.04-.46.04-1.85 0-3.35-1.51-3.35-3.37S8.96 1.01 10.81 1c1.85 0 3.35 1.51 3.35 3.37 0 .16-.02.31-.04.47-.01.04-.01.07-.02.11-.02.15-.05.29-.1.44v.01c-.05.15-.11.28-.17.42-.01.02-.02.05-.03.07-.07.14-.14.27-.23.4zm-5.01-1.94c1.22 0 2.21-.99 2.21-2.22s-.99-2.22-2.21-2.22-2.21.99-2.21 2.22c0 1.22.99 2.22 2.21 2.22"];
})), WS, GS = o((() => {
	WS = ["M11 0a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zm-1 2.667C10 2.3 9.7 2 9.333 2h-.666C8.3 2 8 2.3 8 2.667v.666C8 3.7 8.3 4 8.667 4h.666C9.7 4 10 3.7 10 3.333zm0 3.666v-.666C10 5.3 9.7 5 9.333 5h-.666C8.3 5 8 5.3 8 5.667v.666C8 6.7 8.3 7 8.667 7h.666C9.7 7 10 6.7 10 6.333m0 2.334C10 8.3 9.7 8 9.333 8h-.666C8.3 8 8 8.3 8 8.667v.666c0 .367.3.667.667.667h.666C9.7 10 10 9.7 10 9.333zM.446 10.359 3 8.659V11a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V8.66l2.554 1.698a1 1 0 0 1 .189 1.502l-3.436 3.809c-.19.21-.46.331-.745.331H4.438c-.284 0-.555-.12-.745-.331l-3.436-3.81a1 1 0 0 1 .19-1.5"];
})), KS, qS = o((() => {
	KS = ["M14.29 4.296a1.002 1.002 0 0 1 1.42 1.419l-3 2.996a1.015 1.015 0 0 1-1.42 0l-3-2.997a1.002 1.002 0 0 1 1.42-1.419L11 5.586V1a1 1 0 0 1 2 0v4.584zM7.583 6.422l3.01 3.006.01.01c.359.34.85.563 1.397.563V11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h5.268A2 2 0 0 0 10 1v2.27a2.002 2.002 0 0 0-2.417 3.152M13 9.736q.23-.13.417-.317l.29-.29 1.847 1.23a1 1 0 0 1 .189 1.5l-3.436 3.81c-.19.21-.46.331-.745.331H4.438c-.284 0-.555-.12-.745-.331l-3.436-3.81a1 1 0 0 1 .19-1.5L3 8.659V11a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2z"];
})), JS, YS = o((() => {
	JS = ["M3 1c0-.55-.45-1-1-1S1 .45 1 1v3h2zm0 4H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m12-4c0-.55-.45-1-1-1s-1 .45-1 1v2h2zM9 1c0-.55-.45-1-1-1S7 .45 7 1v6h2zM1 15c0 .55.45 1 1 1s1-.45 1-1v-5H1zM15 4h-2c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m-2 11c0 .55.45 1 1 1s1-.45 1-1V9h-2zM9 8H7c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-2 7c0 .55.45 1 1 1s1-.45 1-1v-2H7z"];
})), XS, ZS = o((() => {
	XS = ["M5.92 8.139c.44-.282 1.006-.121 1.264.358l2.689 4.988c.083.155.127.33.127.51C10 14.55 9.587 15 9.077 15H3.924a.86.86 0 0 1-.438-.12c-.449-.263-.617-.873-.376-1.362l2.465-4.989a.97.97 0 0 1 .346-.39M12 4a3 3 0 1 1 0 6 3 3 0 0 1 0-6M6 1a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"];
})), QS, $S = o((() => {
	QS = ["M10.99 13.99h-9v-9h4.76l2-2H.99c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h11c.55 0 1-.45 1-1V7.24l-2 2zm4-14h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L7.29 7.28a1 1 0 0 0-.3.71 1.003 1.003 0 0 0 1.71.71l5.29-5.29V6c0 .55.45 1 1 1s1-.45 1-1V1c0-.56-.45-1.01-1-1.01"];
})), eC, tC = o((() => {
	eC = ["M13.843 15.163c.232.53.138.837.138.837H6.017s-.088-.308.138-.837c.226-.53 1.338-.88 2.079-1.206.735-.332.66-.53.685-.8 0-.03.006-.068.006-.105a2.2 2.2 0 0 1-.61-.892v-.006s-.006-.006-.006-.012c-.025-.074-.056-.16-.075-.24-.176-.031-.276-.222-.314-.394a.8.8 0 0 1-.1-.437c.025-.253.131-.37.244-.419v-.037c0-.313.032-.775.088-1.07A1.84 1.84 0 0 1 8.85 8.37c.315-.24.76-.37 1.156-.37s.842.13 1.156.37c.301.233.534.56.64.935.026.08.045.166.057.246.057.295.088.75.088 1.064v.043c.113.05.214.167.232.413a.75.75 0 0 1-.1.437c-.038.172-.132.357-.301.387a2 2 0 0 1-.076.24l-.006.025a2.35 2.35 0 0 1-.597.892v.111c.025.277-.075.474.666.8s1.853.67 2.079 1.2M14.853 15h1.13s.083-.27-.12-.732c-.16-.373-.82-.641-1.411-.88a15 15 0 0 1-.409-.17c-.565-.25-.57-.412-.577-.61q-.001-.045-.005-.09v-.097c.22-.2.401-.469.522-.781 0 0 .005-.016.005-.022q.042-.105.066-.21c.149-.026.231-.188.264-.339a.66.66 0 0 0 .088-.382c-.016-.215-.104-.318-.203-.36v-.039a6 6 0 0 0-.077-.931 1.6 1.6 0 0 0-.61-1.034 1.74 1.74 0 0 0-1.285-.3c.236.285.42.622.529.996.038.124.065.248.083.36.048.257.079.578.093.867a1.74 1.74 0 0 1 .08 1.624 1.7 1.7 0 0 1-.217.453 1.4 1.4 0 0 1-.176.209q-.12.307-.292.585l.202.083c.285.117.64.261.9.387.226.11.475.245.698.414.213.161.476.408.63.764q.052.12.091.235m-2.712-.88.09.037ZM11 1c.55 0 1 .45 1 1 0 .28-.11.53-.29.7L8 6.41v1.374a2.8 2.8 0 0 0-.833 1.589 7 7 0 0 0-.092.86 1.64 1.64 0 0 0-.25.739l-.001.004c-.02.217.006.413.046.573L5.71 12.71A1.003 1.003 0 0 1 4 12V6.41L.29 2.71A1.003 1.003 0 0 1 1 1z"];
})), nC, rC = o((() => {
	nC = ["M8 16q7-4.572 7-12.571-2.334 0-7-3.429-4.666 3.429-7 3.429 0 8 7 12.571M8 2.121c2.005 1.388 3.715 2.304 5.186 2.735-.342 3.702-2.05 6.683-5.186 9.038z"];
})), iC, aC = o((() => {
	iC = ["M5.44.804A1 1 0 0 1 6.42 0h3.16a1 1 0 0 1 .98.804L10.8 2H13a1 1 0 0 1 1 1v3.714l1.005.287a1 1 0 0 1 .677 1.27l-1.208 3.74a1 1 0 0 1-.308.457q.392.031.834.032a.5.5 0 0 1 0 1c-1.46 0-2.568-.261-3.318-.53a6 6 0 0 1-.856-.373l-.004-.002c-.552.372-1.502.905-2.822.905-1.334 0-2.289-.544-2.839-.917-.747.374-2.094.917-4.161.917a.5.5 0 0 1 0-1q.283 0 .544-.014l-.005-.012C1.127 11.54.596 9.647.23 8.215a.99.99 0 0 1 .69-1.192L2 6.714V3a1 1 0 0 1 1-1h2.2zM4 6.143l3-.857V4H4zm5-.857 3 .857V4H9zm-4.036 8.273a.5.5 0 0 1 .527.034c.455.325 1.277.907 2.509.907s2.054-.582 2.51-.907a.5.5 0 0 1 .579-.001l.006.004.036.023q.051.034.168.097c.154.082.394.197.72.313.649.232 1.642.471 2.981.471a.5.5 0 0 1 0 1c-1.46 0-2.568-.261-3.318-.53a6 6 0 0 1-.856-.373l-.004-.002c-.552.372-1.502.905-2.822.905-1.334 0-2.289-.544-2.839-.917-.747.374-2.094.917-4.161.917a.5.5 0 0 1 0-1c2.129 0 3.384-.63 3.964-.94"];
})), oC, sC = o((() => {
	oC = ["M3 2h10c.55 0 1-.45 1-1s-.45-1-1-1H3c-.55 0-1 .45-1 1s.45 1 1 1m9 11H4v-3H2v5c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-5h-2zm4-6-1.01-3.17C14.9 3.36 14.49 3 14 3H2c-.49 0-.9.36-.98.83L.01 7H0c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2"];
})), cC, lC = o((() => {
	cC = ["M14 10H7.72l-.33-1H13c.39 0 .72-.23.89-.56h.01l2-4h-.01c.06-.13.11-.28.11-.44 0-.55-.45-1-1-1H5.39l-.44-1.32h-.01C4.8 1.29 4.44 1 4 1H1c-.55 0-1 .45-1 1s.45 1 1 1h2.28l2.33 7H4c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2h6c0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2M6.05 5h7.33l-1 2H6.72z"];
})), uC, dC = o((() => {
	uC = ["M1 6h14c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m4 3H1c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1m7 3c0-.28-.11-.53-.29-.71l-.3-.29H15c.55 0 1-.45 1-1s-.45-1-1-1h-3.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2c-.18.18-.29.43-.29.71s.11.53.29.71l2 2A1.003 1.003 0 0 0 12 12"];
})), fC, pC = o((() => {
	fC = ["M5.474 7.971A5.3 5.3 0 0 0 6.66 8.9l.007.019.018.056c.015.038.038.06.045.098l1.5 5.999a.75.75 0 0 1-1.455.36l-.42-1.68h-.704l-.42 1.68a.746.746 0 0 1-.907.547.746.746 0 0 1-.547-.907l1.5-6c.007-.037.03-.06.044-.097.015-.037.015-.075.038-.112a.7.7 0 0 1-.105-.36c0-.207.084-.394.22-.53M2.795 5.277a.763.763 0 0 0-.015-1.065.756.756 0 0 0-1.065.015c-2.286 2.34-2.286 6.21 0 8.549a.747.747 0 1 0 1.072-1.042c-1.709-1.763-1.709-4.702.008-6.457m5.013 4.111a5.3 5.3 0 0 0 1.58.211 2.24 2.24 0 0 1-.656.98.756.756 0 0 1-1.057-.098.756.756 0 0 1 .097-1.057zm3.736-.283.378.378a6.02 6.02 0 0 1-1.638 3.285c-.285.3-.757.3-1.057.015a.74.74 0 0 1-.015-1.057 4.5 4.5 0 0 0 1.185-2.24q.602-.126 1.147-.381m-7.49.319c-.427-.352-.352-1.582-.03-1.822a.75.75 0 0 0 .15-1.05.75.75 0 0 0-1.05-.15c-1.079.802-1.221 3.18-.03 4.177a.75.75 0 1 0 .96-1.155M9.318 0a4.32 4.32 0 0 1 4.317 4.318c0 .206-.02.402-.049.598-.01.05-.01.088-.02.138a5 5 0 0 1-.137.569v.01a5 5 0 0 1-.216.54l-.039.087a5 5 0 0 1-.294.51l2.884 2.886a.88.88 0 0 1 .236.559.787.787 0 0 1-.785.785.8.8 0 0 1-.56-.226L11.772 7.89a5 5 0 0 1-.51.295l-.089.039a5 5 0 0 1-.54.216h-.01a4 4 0 0 1-.568.137c-.05.01-.099.02-.138.02-.196.03-.392.049-.598.049A4.32 4.32 0 0 1 5 4.327 4.33 4.33 0 0 1 9.318 0m-.02 1.1A3.195 3.195 0 0 0 6.1 4.298a3.195 3.195 0 0 0 3.198 3.198 3.195 3.195 0 0 0 3.198-3.198A3.195 3.195 0 0 0 9.298 1.1"];
})), mC, hC = o((() => {
	mC = ["m13.71 4.29-4-4A1 1 0 0 0 9 0H3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V5c0-.28-.11-.53-.29-.71M7 6h2v2H7zM4 6h2v2H4zm2 8H4v-2h2zm3 0H7v-2h2zm3 0h-2v-2h2zm0-3H4V9h8zm0-3h-2V6h2z"];
})), gC, _C = o((() => {
	gC = ["M10 2a.99.99 0 0 0-.96.73l-2.99 9.96A1.003 1.003 0 0 0 7 14c.46 0 .85-.31.96-.73l2.99-9.96A1.003 1.003 0 0 0 10 2"];
})), vC, yC = o((() => {
	vC = ["m9.41 8 2.29-2.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L8 6.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42L6.59 8 4.3 10.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L8 9.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), bC, xC = o((() => {
	bC = ["M14 8A6 6 0 1 1 2 8a6 6 0 0 1 12 0M9 4H7v2h2zm0 3H6v1h1v3H6v1h4v-1H9z"];
})), SC, CC = o((() => {
	SC = ["M11 7H5c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1"];
})), wC, TC = o((() => {
	wC = ["M11 7H9V5c0-.55-.45-1-1-1s-1 .45-1 1v2H5c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V9h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), EC, DC = o((() => {
	EC = ["M5 5v6h6V5zM4 3h8a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1"];
})), OC, kC = o((() => {
	OC = ["M12 5c-.28 0-.53.11-.71.29L7 9.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l5-5A1.003 1.003 0 0 0 12 5"];
})), AC, jC = o((() => {
	AC = ["m13.364 9 .879.879a1 1 0 1 1-1.415 1.414l-2.12-2.121a1 1 0 0 1-.14-.172H9v1.604q.063.045.121.103l2.122 2.121a1 1 0 0 1-1.415 1.415L9 13.414V15a1 1 0 0 1-2 0v-1.636l-.879.879a1 1 0 1 1-1.414-1.415l2.121-2.12q.08-.08.172-.139V9H5.38q-.057.09-.137.172l-2.122 2.12A1 1 0 1 1 1.707 9.88L2.586 9H1a1 1 0 1 1 0-2h1.536l-.829-.828a1 1 0 0 1 1.414-1.415L5.243 6.88q.057.058.103.121H7V5.38a1 1 0 0 1-.172-.137L4.708 3.12A1 1 0 0 1 6.12 1.707l.88.879V1a1 1 0 1 1 2 0v1.536l.828-.829a1 1 0 0 1 1.415 1.414L9.12 5.243a1 1 0 0 1-.12.103V7h1.604q.045-.063.103-.121l2.121-2.122a1 1 0 0 1 1.415 1.415L13.414 7H15a1 1 0 0 1 0 2z"];
})), MC, NC = o((() => {
	MC = ["M15 7.5a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0M7.5 13c.694 0 1.357-.128 1.969-.363l.342-1.053-1.132-1.557H6.34L5.202 11.59l.341 1.052A5.5 5.5 0 0 0 7.5 13m5.499-5.39-1.179-.856-1.67.542-.686 2.113.002-.001 1.154 1.588h1.126a5.48 5.48 0 0 0 1.253-3.386m-9.74 3.392h1.135L5.54 9.424 4.854 7.31l-1.711-.556-1.142.83a5.48 5.48 0 0 0 1.258 3.418M8 4.963l1.883 1.369 1.628-.53.48-1.477a5.5 5.5 0 0 0-2.89-2.088L8 3.037zM5.899 2.237A5.5 5.5 0 0 0 2.983 4.36l.47 1.442 1.652.537L7 4.963V3.037z"];
})), PC, FC = o((() => {
	PC = ["M9.5 4c.4 0 .8-.1 1.1-.3C12 4.5 12.9 6 13 7.6c0 .5.5.9 1 .9.6 0 1-.4 1-1v-.2c-.2-2.4-1.5-4.4-3.5-5.5-.1-1-.9-1.8-2-1.8s-2 .9-2 2 .9 2 2 2M4 8.5c0-.7-.4-1.3-.9-1.7.3-1.4 1.2-2.6 2.5-3.3.3-.1.6-.4.6-.9s-.4-1-1-1c-.2 0-.3 0-.5.1-1.9 1-3.2 2.8-3.6 5C.4 7.1 0 7.8 0 8.5c0 1.1.9 2 2 2s2-.9 2-2m8.8 1.2c-1.1 0-2 .9-2 2v.3c-.8.6-1.8.9-2.8.9-1.2 0-2.3-.4-3.2-1.1-.2-.2-.4-.3-.7-.3-.6 0-1 .4-1 1 0 .3.1.6.3.8C4.6 14.4 6.2 15 8 15c1.5 0 3-.5 4.1-1.3.2.1.5.1.7.1 1.1 0 2-.9 2-2s-.9-2.1-2-2.1"];
})), IC, LC = o((() => {
	IC = ["M5 12c-.28 0-.53.11-.71.29l-.29.3V9c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29A.97.97 0 0 0 1 12a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 5 12m3-9h7c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1m7 2H8c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1m0 8H8c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1m0-4H8c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1"];
})), RC, zC = o((() => {
	RC = ["M6 12c-.28 0-.53.11-.71.29l-.29.3V9c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29A.97.97 0 0 0 2 12a1.003 1.003 0 0 0-.71 1.71l2 2c.19.18.44.29.71.29.28 0 .53-.11.71-.29l2-2c.18-.18.29-.43.29-.71a.99.99 0 0 0-1-1m7.93-.95v-1.04H9.25v1.11h2.94L9 14.96V16h5.02v-1.11h-3.27zm-1.42-4.84.62 1.78H15L11.94.01H10.1L7 7.99h1.81l.64-1.78zm-1.52-4.24h.02l1.03 2.93H9.92z"];
})), BC, VC = o((() => {
	BC = ["M5.99 11.99c-.28 0-.53.11-.71.29l-.29.29V8.99c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29a1.003 1.003 0 0 0-1.42 1.42l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2c.18-.18.29-.43.29-.71 0-.56-.45-1.01-1-1.01M12.7 10h-1.38L9 15.99h1.36l.48-1.33h2.3l.46 1.33H15zm-1.51 3.67.8-2.2h.02l.77 2.2zm3.8-7.17h-4.57l4.45-5.12V0H8.34v1.48h4.1L7.99 6.59v1.39h7z"];
})), HC, UC = o((() => {
	HC = ["M8 7h3c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1m0-4h1c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1m0 8h5c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1m-3 1c-.28 0-.53.11-.71.29l-.29.3V9c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29A.97.97 0 0 0 1 12a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 5 12m10 1H8c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1"];
})), WC, GC = o((() => {
	WC = ["M5 12c-.28 0-.53.11-.71.29l-.29.3V9c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29A.97.97 0 0 0 1 12a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 5 12m4 1H8c-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1-.45 1-1s-.45-1-1-1m4-8H8c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m-2 4H8c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1m4-8H8c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1"];
})), KC, qC = o((() => {
	KC = ["M6 11.99c-.28 0-.53.11-.71.29l-.29.3V8.99c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29c-.18-.18-.43-.3-.71-.3a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 6 11.99m7.91-.08q-.09-.54-.33-.96c-.16-.28-.37-.51-.64-.69-.27-.17-.61-.26-1.03-.26-.28 0-.54.06-.78.17q-.345.165-.6.45c-.17.19-.3.41-.39.67a2.5 2.5 0 0 0-.04 1.52 1.62 1.62 0 0 0 .89 1.03c.22.11.45.16.68.16.26 0 .5-.05.7-.15s.38-.26.53-.5l.02.02c-.01.16-.03.34-.07.54-.03.2-.09.4-.17.57-.08.18-.18.33-.31.45s-.29.19-.5.19a.63.63 0 0 1-.48-.21c-.13-.14-.21-.31-.25-.5H10.1c.03.25.1.48.19.68.1.2.22.37.38.5.16.14.33.24.54.31s.42.1.65.1q.585 0 .99-.27c.27-.18.49-.41.66-.7s.29-.61.37-.97.12-.72.12-1.07q0-.54-.09-1.08m-1.14.54c-.04.13-.09.24-.16.34a.8.8 0 0 1-.27.24q-.165.09-.39.09a.75.75 0 0 1-.37-.09.8.8 0 0 1-.26-.25c-.07-.1-.12-.22-.15-.35s-.05-.26-.05-.4c0-.13.02-.26.05-.39.04-.13.09-.24.16-.34s.16-.18.26-.24.22-.09.35-.09c.14 0 .26.03.37.09s.2.14.28.24a1.3 1.3 0 0 1 .23.74c0 .15-.02.28-.05.41m-1.56-4.47H13V0h-1.42c-.05.3-.16.56-.31.76-.16.21-.35.37-.58.5s-.49.21-.78.26c-.3.05-.6.07-.91.06V2.8h2.21z"];
})), JC, YC = o((() => {
	JC = ["M6 11.99c-.28 0-.53.11-.71.29l-.29.3V8.99c0-.55-.45-1-1-1s-1 .45-1 1v3.59l-.29-.29a.98.98 0 0 0-.71-.3 1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 6 11.99m7.86-9.45c-.09-.48-.26-.9-.5-1.28S12.8.58 12.4.35 11.49 0 10.86 0c-.43 0-.82.07-1.17.22q-.525.225-.9.6c-.25.25-.44.55-.58.89s-.2.71-.2 1.11c0 .31.05.61.15.91s.26.57.48.8c.23.24.52.43.85.58.33.14.68.21 1.03.21.4 0 .75-.07 1.05-.2s.57-.35.79-.66l.02.02c-.02.21-.05.45-.1.73-.05.27-.13.53-.25.76-.12.24-.27.44-.47.6-.19.16-.44.25-.75.25a.98.98 0 0 1-.72-.29c-.19-.18-.31-.4-.37-.66H8.15c.05.34.14.64.29.9s.34.49.57.67.5.32.8.41c.31.1.63.15.98.15.58 0 1.08-.12 1.48-.36q.6-.36.99-.93c.26-.39.44-.82.56-1.29Q14 4.7 14 3.98c0-.48-.05-.96-.14-1.44m-1.71.72c-.05.17-.14.32-.24.46-.11.13-.24.24-.41.31-.16.08-.36.12-.58.12-.21 0-.39-.04-.55-.13q-.24-.12-.39-.33c-.12-.14-.19-.29-.24-.46s-.08-.35-.08-.54c0-.18.03-.35.08-.52.06-.16.14-.31.25-.44s.24-.24.4-.32.33-.12.52-.12c.21 0 .4.04.56.12s.3.19.41.32c.11.14.2.29.26.46s.09.35.09.52c0 .2-.03.38-.08.55m-.46 7.31c-.12.15-.26.28-.44.37-.17.09-.37.16-.58.2-.22.04-.44.05-.67.05v.92h1.65v3.88h1.33V10h-1.06c-.03.23-.11.42-.23.57"];
})), XC, ZC = o((() => {
	XC = ["m6.89.56 4 8c.06.13.11.28.11.44 0 .55-.45 1-1 1-.39 0-.72-.23-.89-.55H9.1L8.38 8H3.62L2.9 9.44h-.01c-.17.33-.5.56-.89.56-.55 0-1-.45-1-1 0-.16.05-.31.12-.44L3.1 4.58 4 2.76 5.11.56C5.28.23 5.61 0 6 0s.72.23.89.56M14 9c-.28 0-.53.11-.71.29L9 13.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l5-5A1.003 1.003 0 0 0 14 9M6 3.24 4.62 6h2.76z"];
})), QC, $C = o((() => {
	QC = ["M5.287 6.281a.98.98 0 0 1 1.373 0l2.059 2.04.066.073A.955.955 0 0 1 8.72 9.68l-2.06 2.039a.98.98 0 0 1-1.373 0 .955.955 0 0 1 0-1.36l.171-.17c-.66.104-1.262.246-1.773.422-.78.27-1.318.607-1.551.974a.73.73 0 0 0-.116.556q.058.277.347.544c.385.352 1.06.66 1.946.891s1.948.374 3.066.413a17 17 0 0 0 3.257-.191c1.01-.164 1.862-.42 2.458-.738a2.4 2.4 0 0 0 .681-.512.9.9 0 0 0 .216-.407l.014-.141a1 1 0 0 1 2 0c0 1.569-1.26 2.446-1.97 2.824-.862.46-1.95.764-3.078.947-1.15.188-2.41.26-3.647.217-1.234-.043-2.446-.202-3.501-.476-.997-.26-2.048-.67-2.791-1.35-.392-.359-.804-.89-.955-1.608a2.73 2.73 0 0 1 .385-2.042c.614-.965 1.71-1.488 2.585-1.79.815-.282 1.759-.478 2.747-.594l-.49-.487a.955.955 0 0 1 0-1.36m3.059-6a.98.98 0 0 1 1.373 0 .955.955 0 0 1 0 1.36l-.408.402c1.118.074 2.201.245 3.145.515.994.283 2.125.757 2.843 1.601.402.473.742 1.15.7 1.977-.041.81-.433 1.437-.84 1.86-.747.778-1.87 1.225-2.893 1.498a1 1 0 1 1-.516-1.932c.922-.246 1.606-.577 1.967-.952.18-.188.275-.383.285-.576q.016-.291-.227-.579c-.322-.379-.973-.718-1.869-.974a13 13 0 0 0-2.493-.424l.306.302a.955.955 0 0 1 0 1.36.98.98 0 0 1-1.373 0l-2.059-2.04a.955.955 0 0 1 0-1.359zm-5.4 2.47a1 1 0 0 1 .672 1.884c-.595.212-1.045.465-1.317.742-.278.283-.357.577-.256.86a1 1 0 0 1-1.884.67c-.435-1.22.081-2.288.714-2.931.576-.587 1.35-.967 2.071-1.225"];
})), ew, tw = o((() => {
	ew = ["M12 10a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H9V2h3v1.71c.31-.13.64-.21 1-.21s.69.08 1 .21V1c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v2.71c.31-.13.64-.21 1-.21s.69.08 1 .21V2h3v5H3.41l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C.11 7.47 0 7.72 0 8s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L3.41 9H7v5H4v-1.71c-.31.13-.64.21-1 .21s-.69-.08-1-.21V15c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-2.71c-.31.13-.64.21-1 .21s-.69-.08-1-.21V14H9V9h3.59l-.29.29c-.19.18-.3.43-.3.71"];
})), nw, rw = o((() => {
	nw = ["M6 .5a.5.5 0 0 1 .816-.387C7.154-.111 7.652.04 8.182.2 8.811.39 9.486.596 10 .21v2.62c-.51.315-1.085.128-1.618-.046-.538-.176-1.035-.338-1.382.046v1.193Q7.492 4 8 4c1.06 0 2.074.077 3 .218V.5a.5.5 0 0 1 .816-.387c.338-.224.836-.073 1.366.088.629.19 1.304.395 1.818.01V2.83c-.51.315-1.085.128-1.618-.046-.538-.176-1.035-.338-1.382.046V4.4c2.391.52 4 1.489 4 2.599 0 .552-.398 1.07-1.091 1.514C14.366 7.088 11.479 6 8 6 4.52 6 1.634 7.088 1.092 8.514.397 8.069 0 7.552 0 7c0-.528.364-1.024 1.002-1.455L1 5.5v-5a.5.5 0 0 1 .816-.387C2.154-.111 2.652.04 3.182.2 3.811.39 4.486.596 5 .21v2.62c-.51.315-1.085.128-1.618-.046-.538-.176-1.035-.338-1.382.046v2.186c1.042-.443 2.428-.77 4-.921zm8 8.485c-.005-.081-.046-.232-.262-.45-.234-.238-.623-.497-1.182-.737C11.44 7.32 9.83 7 8 7s-3.44.32-4.556.798c-.56.24-.948.5-1.182.737-.216.218-.257.369-.262.45C3.466 9.607 5.61 10 8 10s4.534-.393 6-1.015m.008 1.073C12.422 10.653 10.298 11 8 11s-4.422-.348-6.008-.942C1.22 9.768.525 9.439 0 8.985V13c0 1.398 2.55 2.667 6 3v-1a2 2 0 1 1 4 0v1c3.45-.333 6-1.602 6-3V8.985c-.525.454-1.22.783-1.992 1.073"];
})), iw, aw = o((() => {
	iw = ["M15 0H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H2V2h12z"];
})), ow, sw = o((() => {
	ow = ["M10 2c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v3h3zm3 10h1c.55 0 1-.45 1-1V8h-3v3c0 .55.45 1 1 1m2-7c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v2h3zm-5 1H7v3h3zM5 7c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v1h3zm3 5h1c.55 0 1-.45 1-1v-1H7v1c0 .55.45 1 1 1m7 1H2c-.55 0-1 .45-1 1s.45 1 1 1h13c.55 0 1-.45 1-1s-.45-1-1-1M3 12h1c.55 0 1-.45 1-1V9H2v2c0 .55.45 1 1 1"];
})), cw, lw = o((() => {
	cw = ["M12 6H4a2 2 0 1 0 0 4h8a2 2 0 1 0 0-4M4 4h8a4 4 0 0 1 0 8H4a4 4 0 0 1 0-8"];
})), uw, dw = o((() => {
	uw = ["m8 0 2.5 5.3 5.5.8-4 4.1.9 5.8L8 13.3 3.1 16l.9-5.8-4-4.1 5.5-.8z"];
})), fw, pw = o((() => {
	fw = ["m16 6.11-5.53-.84L8 0 5.53 5.27 0 6.11l4 4.1L3.06 16 8 13.27 12.94 16 12 10.21zM4.91 13.2l.59-3.62L3 7.02l3.45-.53L8 3.2l1.55 3.29 3.45.53-2.5 2.56.59 3.62L8 11.49z"];
})), mw, hw = o((() => {
	mw = ["M12 3c-.24 0-.44.09-.62.23l-.01-.01L7 6.72V4c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V9.28l4.38 3.5.01-.01c.17.14.37.23.61.23.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), gw, _w = o((() => {
	gw = ["M15 12H2v-2h3c.55 0 1-.45 1-1V7h2v1c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V5h1c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1v3h-2V6c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v2H2V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), vw, yw = o((() => {
	vw = ["M12 3h-1c-.55 0-1 .45-1 1v2.72l-4.38-3.5v.01A1 1 0 0 0 5 3c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1 .24 0 .44-.09.62-.23l.01.01L10 9.28V12c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), bw, xw = o((() => {
	bw = ["M12 3H4c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h8c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), Sw, Cw = o((() => {
	Sw = ["M9 2v1.083A6.002 6.002 0 0 1 8 15 6 6 0 0 1 7 3.083V2H6a1 1 0 1 1 0-2h4a1 1 0 0 1 0 2zM8 5a4 4 0 1 0 4 4H8z"];
})), ww, Tw = o((() => {
	ww = ["M14 7H8.65c-.38-.09-.73-.18-1.04-.26s-.49-.13-.54-.14c-.43-.11-.79-.29-1.05-.52-.27-.23-.4-.55-.4-.95q0-.435.21-.72c.21-.285.32-.34.54-.46q.33-.165.72-.24c.26-.05.52-.07.77-.07.74 0 1.36.15 1.84.46.32.2.55.5.68.9h2.22c-.06-.33-.17-.64-.32-.92-.25-.45-.59-.84-1.02-1.15s-.93-.54-1.49-.7S8.59 2 7.95 2c-.55 0-1.1.07-1.63.2-.54.13-1.02.34-1.45.62q-.63.42-1.02 1.05t-.39 1.5c0 .3.04.59.13.88q.12.39.39.75H2c-.55 0-1 .45-1 1s.45 1 1 1h7.13c.25.07.49.14.71.22.25.09.48.23.7.44.21.21.32.53.32.97 0 .21-.05.43-.14.63-.09.21-.24.39-.45.55q-.315.24-.81.39t-1.2.15c-.44 0-.84-.05-1.21-.14s-.7-.24-.99-.43c-.29-.2-.51-.45-.67-.76-.01 0-.01-.01-.02-.02H3.14a3.68 3.68 0 0 0 1.39 2.03c.46.34 1 .58 1.62.74.61.15 1.27.23 1.97.23.61 0 1.2-.07 1.79-.2.58-.13 1.11-.34 1.56-.63q.69-.435 1.11-1.11c.28-.45.42-1 .42-1.64q0-.45-.15-.9c-.05-.19-.13-.36-.22-.52H14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), Ew, Dw = o((() => {
	Ew = ["M14 14H2V2h8.76l2-2H1C.45 0 0 .45 0 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V6.24l-2 2zm1.4-14L9.7 5.7l2.1 2.1L16 3.6V0zM4 11.92c2.33.15 4.42.15 6.15-1.5.82-.83.82-2.25 0-3.08-.45-.38-.98-.6-1.5-.6-.53 0-1.05.22-1.43.6-.82.91-1.27 3.38-3.22 4.58"];
})), Ow, kw = o((() => {
	Ow = ["M6.2 4.4a1 1 0 0 1 1.6 1.2L5.25 9l2.55 3.4a1 1 0 0 1-1.6 1.2L4 10.667 1.8 13.6a1 1 0 0 1-1.6-1.2L2.75 9 .2 5.6a1 1 0 0 1 1.6-1.2L4 7.333zm6.954 9.544.016-.014c.18-.14.36-.28.57-.42l.63-.45c.21-.16.41-.33.61-.51s.37-.38.52-.59.28-.45.37-.7.13-.54.13-.85c0-.25-.04-.51-.12-.79-.07-.29-.2-.55-.39-.79a2.2 2.2 0 0 0-.73-.6c-.29-.15-.66-.23-1.11-.23-.4 0-.76.08-1.07.23-.31.16-.58.37-.79.62-.22.27-.38.59-.49.96s-.16.77-.16 1.2h1.19c.01-.27.03-.53.08-.77.04-.24.11-.45.21-.62.09-.18.22-.32.38-.42s.35-.15.59-.15c.26 0 .47.05.63.14.15.09.28.21.37.35q.135.21.18.45c.03.16.05.31.05.45-.01.31-.08.58-.22.82-.14.23-.32.45-.53.65-.22.21-.46.39-.71.57q-.39.27-.75.54c-.5.36-.89.78-1.17 1.27S11.01 15.35 11 16h4.99v-1.14h-3.55c.05-.17.14-.33.27-.49.126-.145.28-.281.444-.426"];
})), Aw, jw = o((() => {
	Aw = ["M6.006 3.101A6.98 6.98 0 0 0 4 8c0 1.866.736 3.611 2.002 4.9Q5.515 13 5 13a5 5 0 1 1 1.006-9.899M16 8a5 5 0 0 0-6-4.9A7 7 0 0 1 12 8c0 1.865-.736 3.61-2 4.9q.486.1 1 .1a5 5 0 0 0 5-5m-3 0c0-1.37-.348-2.695-.999-3.873l.154.042A4 4 0 0 1 15 8l-.005.2a4 4 0 0 1-2.84 3.63l-.155.043.162-.305A8 8 0 0 0 13 8M8.001 4A5 5 0 0 1 10 8a5 5 0 0 1-1.999 3.999 4.99 4.99 0 0 1-2.001-4 4.99 4.99 0 0 1 1.918-3.937zM8 5.354l-.11.13A3.98 3.98 0 0 0 7 8c0 .957.337 1.856.928 2.563l.072.08.072-.08c.542-.648.87-1.458.921-2.325L9 8c0-.956-.337-1.855-.928-2.562z"];
})), Mw, Nw = o((() => {
	Mw = ["m13.154 5.944.016-.014c.18-.14.36-.28.57-.42l.63-.45c.21-.16.41-.33.61-.51s.37-.38.52-.59.28-.45.37-.7.13-.54.13-.85c0-.25-.04-.51-.12-.79-.07-.29-.2-.55-.39-.79a2.2 2.2 0 0 0-.73-.6C14.47.08 14.1 0 13.65 0c-.4 0-.76.08-1.07.23-.31.16-.58.37-.79.62-.22.27-.38.59-.49.96s-.16.77-.16 1.2h1.19c.01-.27.03-.53.08-.77.04-.24.11-.45.21-.62.09-.18.22-.32.38-.42s.35-.15.59-.15c.26 0 .47.05.63.14.15.09.28.21.37.35q.135.21.18.45c.03.16.05.31.05.45-.01.31-.08.58-.22.82-.14.23-.32.45-.53.65-.22.21-.46.39-.71.57q-.39.27-.75.54c-.5.36-.89.78-1.17 1.27S11.01 7.35 11 8h4.99V6.86h-3.55c.05-.17.14-.33.27-.49.126-.145.28-.281.444-.426M6.2 4.4a1 1 0 0 1 1.6 1.2L5.25 9l2.55 3.4a1 1 0 0 1-1.6 1.2L4 10.667 1.8 13.6a1 1 0 0 1-1.6-1.2L2.75 9 .2 5.6a1 1 0 0 1 1.6-1.2L4 7.333z"];
})), Pw, Fw = o((() => {
	Pw = ["M0 7.02.05 7H0zm2-2.03h9.57l-1.29 1.29A1.003 1.003 0 0 0 11.7 7.7l2.99-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2.99-3a1.07 1.07 0 0 0-.71-.28 1.003 1.003 0 0 0-.71 1.71L11.57 3H2c-.55 0-1 .45-1 1a1 1 0 0 0 1 .99M15.96 9H16v-.02zM14 11.01H4.43l1.29-1.29A1.003 1.003 0 0 0 4.3 8.3l-2.99 3a1 1 0 0 0-.29.7c0 .28.11.53.29.71l2.99 3a1.003 1.003 0 0 0 1.42-1.42L4.43 13H14c.55 0 1-.45 1-1s-.45-.99-1-.99"];
})), Iw, Lw = o((() => {
	Iw = ["M9 0h-.02L9 .04zM7 16h.02L7 15.95zM4.7 1.31c-.18-.18-.43-.29-.7-.29s-.53.11-.71.29l-3 2.99a1.003 1.003 0 0 0 1.42 1.42L3 4.43V14c0 .55.45 1 1 1s1-.45 1-1V4.43l1.29 1.29c.18.18.43.29.7.29A1.003 1.003 0 0 0 7.7 4.3zM15 9.99c-.28 0-.53.11-.71.29L13 11.57V2c0-.55-.45-1-1-1s-1 .45-1 1v9.57l-1.29-1.29a1 1 0 0 0-.7-.29 1.003 1.003 0 0 0-.71 1.71l3 2.99c.18.18.43.29.71.29s.53-.11.71-.29l3-2.99c.18-.18.29-.43.29-.71-.01-.55-.46-1-1.01-1"];
})), Rw, zw = o((() => {
	Rw = ["M10 0a1 1 0 0 0-1 1v8H6a1 1 0 0 0-1 1v1h10v-1a1 1 0 0 0-1-1h-3V1a1 1 0 0 0-1-1M3.5 3a.5.5 0 0 1 0-1h3a.5.5 0 0 1 0 1zm-2 2a.5.5 0 0 1 0-1h5a.5.5 0 0 1 0 1zm2 2a.5.5 0 0 1 0-1h3a.5.5 0 0 1 0 1zM3 15c.44 0 1.653-.773 1.939-3h10.037c-.08 1.516-.432 4-1.976 4h-1v-1l-2 1H8v-1l-2 1H3z"];
})), Bw, Vw = o((() => {
	Bw = ["m9.293 2.293 1.414 1.414-4.999 5a3 3 0 1 1-1.415-1.415zM13 7a3 3 0 1 1 0 6 3 3 0 0 1 0-6M3 9a1 1 0 1 0 0 2 1 1 0 0 0 0-2m10 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), Hw, Uw = o((() => {
	Hw = ["M8 3a5 5 0 1 1 0 10A5 5 0 0 1 8 3"];
})), Ww, Gw = o((() => {
	Ww = ["M12 6.01h-2v-2c0-.55-.45-1-1-1H7c-.55 0-1 .45-1 1v2H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h2v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-2h2c.55 0 1-.45 1-1v-2c0-.56-.45-1-1-1"];
})), Kw, qw = o((() => {
	Kw = ["M12 8.01c0-.19-.07-.36-.16-.51l.01-.01-3-5-.01.01c-.17-.29-.48-.49-.84-.49s-.67.2-.84.49l-.02-.01-3 5 .02.01c-.09.15-.16.32-.16.51s.07.36.16.51h-.02l3 5 .01-.01c.18.29.49.5.85.5s.67-.2.84-.49l.01.01 3-5-.01-.01c.09-.16.16-.32.16-.51"];
})), Jw, Yw = o((() => {
	Jw = ["M13 4H3c-.5 0-1 .5-1 1v6c0 .5.5 1 1 1h10c.5 0 1-.5 1-1V5c0-.5-.5-1-1-1"];
})), Xw, Zw = o((() => {
	Xw = ["M12 3.01H4c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-8c0-.56-.45-1-1-1"];
})), Qw, $w = o((() => {
	Qw = ["M13 4.01c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 .16.05.31.11.44H3.1l4 8h.01c.16.33.49.56.89.56s.72-.23.89-.56h.01l4-8h-.01c.06-.14.11-.28.11-.44"];
})), eT, tT = o((() => {
	eT = ["m12.89 11.56-3.99-8h-.01c-.17-.32-.5-.55-.89-.55s-.72.23-.89.55H7.1l-4 8h.01c-.06.14-.11.29-.11.45 0 .55.45 1 1 1h8c.55 0 1-.45 1-1 0-.16-.05-.31-.11-.45"];
})), nT, rT = o((() => {
	nT = ["M11.146.146a.5.5 0 0 1 .708 0l4 4a.5.5 0 0 1-.708.708l-.646-.647L13.207 5.5l1.647 1.646a.5.5 0 0 1-.708.708l-.646-.647-1.147 1.147-5.5 5.5a.5.5 0 0 1-.707 0l-.646-.647-1.646 1.647a.5.5 0 0 1-.708 0l-.646-.647-1.646 1.647a.5.5 0 0 1-.708-.708L1.793 13.5l-.647-.646a.5.5 0 0 1 0-.708L2.793 10.5l-.647-.646a.5.5 0 0 1 0-.708l5.5-5.5L8.794 2.5l-.647-.646a.5.5 0 1 1 .708-.708L10.5 2.793 11.793 1.5l-.647-.646a.5.5 0 0 1 0-.708M11.293 8 8 4.707 3.207 9.5 6.5 12.793 7.793 11.5 6.146 9.854a.5.5 0 1 1 .708-.708L8.5 10.793 9.793 9.5 8.146 7.854a.5.5 0 1 1 .708-.708L10.5 8.793zM8.707 4 12 7.293l.793-.793L9.5 3.207zm-6.5 8.5L3.5 13.793 4.793 12.5 3.5 11.207zm11.586-9L12.5 2.207 11.207 3.5 12.5 4.793z"];
})), iT, aT = o((() => {
	iT = ["M15 0H1C.4 0 0 .5 0 1v12c0 .6.4 1 1 1h4.126A4 4 0 0 1 5 13a2 2 0 0 1-1.731-1H2v-2h1.264q.132-.23.319-.417L4.166 9H2V7h12v1.352c.623.705 1 1.632 1 2.648.364 0 .706.098 1 .269V1c0-.5-.4-1-1-1M6 6H2V4h4zm4 0H7V4h3zm4 0h-3V4h3zm-4.29 4.29-2-2A1 1 0 0 0 7 8c-.28 0-.53.11-.71.29l-2 2a1.003 1.003 0 0 0 1.42 1.42l.29-.3V13c0 1.66 1.34 3 3 3 .55 0 1-.45 1-1s-.45-1-1-1-1-.45-1-1v-1.59l.29.3a1.003 1.003 0 0 0 1.42-1.42m.58 3.42 2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2a1.003 1.003 0 0 0-1.42-1.42l-.29.3V11c0-1.66-1.34-3-3-3-.55 0-1 .45-1 1s.45 1 1 1 1 .45 1 1v1.59l-.29-.3a1.003 1.003 0 0 0-1.42 1.42"];
})), oT, sT = o((() => {
	oT = ["M1 3a2 2 0 0 1 2-2h4.584a2 2 0 0 1 1.414.586l5.413 5.412a2 2 0 0 1 0 2.829L9.827 14.41a2 2 0 0 1-2.829 0L1.586 8.998A2 2 0 0 1 1 7.584zm3.487-.007a1.494 1.494 0 1 0 0 2.988 1.494 1.494 0 0 0 0-2.988"];
})), cT, lT = o((() => {
	cT = ["M12 0a1 1 0 0 1 1 1v2h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V5H9a1 1 0 0 1 0-2h2V1a1 1 0 0 1 1-1M7.792 2.406A2 2 0 0 0 9 6h1v1a2 2 0 0 0 3.594 1.208 2 2 0 0 1-.183 2.619L8.827 15.41a2 2 0 0 1-2.829 0L.586 9.998A2 2 0 0 1 0 8.584V4a2 2 0 0 1 2-2h4.584a2 2 0 0 1 1.208.406m-5.8 3.081a1.494 1.494 0 1 0 2.99 0 1.494 1.494 0 0 0-2.99 0"];
})), uT, dT = o((() => {
	uT = ["M11.29.29c.39-.39 1.03-.39 1.42 0l2.98 2.96c.41.41.41 1.07 0 1.48l-2.98 2.961c-.39.39-1.03.39-1.42 0a.996.996 0 0 1 0-1.41l2.3-2.29-2.3-2.29a.996.996 0 0 1 0-1.411m2.32 7.941c.57.78.51 1.89-.2 2.6l-4.58 4.581c-.78.78-2.05.78-2.83 0l-5.41-5.41c-.38-.38-.59-.89-.59-1.42V4c0-1.1.9-2 2-2h4.28c.08.15.18.29.31.42L8.18 4 6.59 5.58a2.007 2.007 0 0 0 0 2.84c.38.37.87.58 1.41.58s1.04-.21 1.42-.58l.71-.71A2 2 0 0 0 12 9.001c.54 0 1.04-.21 1.42-.58zM3.49 6.991c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5-1.5.67-1.5 1.5.67 1.5 1.5 1.5M8.71.29l2.98 2.96c.41.41.41 1.07 0 1.48L8.71 7.692c-.39.39-1.03.39-1.42 0a.996.996 0 0 1 0-1.41l2.3-2.29-2.3-2.29a.996.996 0 0 1 0-1.411c.39-.39 1.03-.39 1.42 0"];
})), fT, pT = o((() => {
	fT = ["M10.29 6.29a1.003 1.003 0 0 1 1.42 1.42l-.3.29H13c.55 0 1-.45 1-1s.45-1 1-1 1 .45 1 1c0 1.66-1.34 3-3 3h-1.59l.3.29a1.003 1.003 0 0 1-1.42 1.42l-2-2A1 1 0 0 1 8 9c0-.28.11-.53.29-.71zm3.42-.58a1.003 1.003 0 0 1-1.42-1.42l.3-.29H11c-.55 0-1 .45-1 1s-.45 1-1 1-1-.45-1-1c0-1.66 1.34-3 3-3h1.59l-.3-.29A1.003 1.003 0 0 1 13.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71zM7.888 2.484A4 4 0 0 0 7 5c0 .854.539 1.585 1.294 1.871l-.711.712A2 2 0 0 0 7 9c0 .548.218 1.052.583 1.417l2 2a2 2 0 0 0 1.671.567L8.827 15.41a2 2 0 0 1-2.829 0L.586 9.998A2 2 0 0 1 0 8.584V4a2 2 0 0 1 2-2h4.584a2 2 0 0 1 1.304.484M1.993 5.487a1.494 1.494 0 1 0 2.988 0 1.494 1.494 0 0 0-2.988 0"];
})), mT, hT = o((() => {
	mT = ["M12 1a1 1 0 0 1 1-1c1.66 0 3 1.34 3 3s-1.34 3-3 3h-1.59l.3.29a1.003 1.003 0 0 1-1.42 1.42l-2-2A1 1 0 0 1 8 5c0-.28.11-.53.29-.71l2-2a1.003 1.003 0 0 1 1.42 1.42l-.3.29H13c.55 0 1-.45 1-1s-.45-1-1-1a1 1 0 0 1-1-1m.932 6.519.48.48a2 2 0 0 1 0 2.828L8.826 15.41a2 2 0 0 1-2.829 0L.586 9.998A2 2 0 0 1 0 8.584V4a2 2 0 0 1 2-2h4.584a2 2 0 0 1 1.414.586l.291.29-.706.707A2 2 0 0 0 7 5c0 .548.218 1.052.583 1.417l2 2a2.004 2.004 0 0 0 3.349-.898M1.992 5.487a1.494 1.494 0 1 0 2.99 0 1.494 1.494 0 0 0-2.99 0"];
})), gT, _T = o((() => {
	gT = ["M4 0h4.584a2 2 0 0 1 1.414.586l5.413 5.412a2 2 0 0 1 0 2.829l-4.584 4.584a2 2 0 0 1-2.829 0L2.586 7.998A2 2 0 0 1 2 6.584V2a2 2 0 0 1 2-2m-.007 3.493a1.5 1.5 0 1 0 3 0 1.5 1.5 0 0 0-3 0M.263 5.176 1 3.819v2.765a3 3 0 0 0 .879 2.122l5.412 5.412c.312.312.676.541 1.064.687L4.41 15.93c-1.045.297-2.12-.362-2.4-1.473l-1.942-7.7a2.2 2.2 0 0 1 .196-1.58"];
})), vT, yT = o((() => {
	vT = ["M9 11a1.003 1.003 0 0 0 1.71.71l4-4a1.003 1.003 0 0 0-1.42-1.42l-4 4c-.18.18-.29.43-.29.71M4 6c.28 0 .53-.11.71-.29l4-4A1.003 1.003 0 0 0 7.29.29l-4 4A1.003 1.003 0 0 0 4 6m4 4 5-5-.79-.79.5-.5a1.003 1.003 0 0 0-1.42-1.42l-.5.5L10 2 5 7l.79.79-5.5 5.5a1.003 1.003 0 0 0 1.42 1.42l5.5-5.5zm7 4H7c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1"];
})), bT, xT = o((() => {
	bT = ["M3.7 3.4a1 1 0 0 1 .8-.4h5.086a1 1 0 0 1 .707.293L11 4h3a1 1 0 1 1 0 2h-3v1h2.5a2.5 2.5 0 0 1 0 5h-11a2.5 2.5 0 0 1 0-5H3V4.667a1 1 0 0 1 .2-.6zM2.5 9a.5.5 0 0 0 0 1h11a.5.5 0 0 0 0-1z"];
})), ST, CT = o((() => {
	ST = ["M7 4a1 1 0 0 1 2 0v2a1 1 0 0 1-2 0zm3 3h2a1 1 0 0 1 0 2h-2a1 1 0 0 1 0-2M4 7h2a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2m4 2a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1m8-1A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-2 0A6 6 0 1 0 2 8a6 6 0 0 0 12 0"];
})), wT, TT = o((() => {
	wT = ["M15.12 6.63h-.38L15 7c-.01.3-.01.64 0 .98V8c0 .07-.03.13-.04.19h.02L14 13.1v.9c0 .55-.45 1-1 1s-1-.45-1-1v-1H4v1c0 .55-.45 1-1 1s-1-.45-1-1v-.9l-.98-4.9h.02C1.03 8.13 1 8.07 1 8H.99c0-.33 0-.67.01-1l.26-.37H.88C.4 6.63 0 6.21 0 5.69s.4-.94.88-.94h1.05l.77-2.11c.19-.53.76-1.08 1.26-1.24 0 0 .68-.2 2.05-.32C6.01 1.05 6 1.03 6 1c0-.55.45-1 1-1h2c.55 0 1 .45 1 1 0 .03-.01.05-.02.08 1.37.12 2.05.32 2.05.32.51.15 1.08.71 1.27 1.24l.76 2.12h1.05c.49 0 .89.42.89.93 0 .52-.4.94-.88.94M11 10h2V8h-2zm-8 0h2V8H3zm10-5-.73-1.63C12.21 3.19 12.18 3 12 3H4c-.18 0-.21.19-.27.37L3 5c-.06.18-.18 1 0 1h10c.18 0 .06-.82 0-1"];
})), ET, DT = o((() => {
	ET = ["M11.328 10.238c1.015.413 2.16.878 2.439 1.516.303.69.248 2.67.235 3.143L14 15H2s-.113-2.465.232-3.253c.28-.638 1.424-1.104 2.44-1.517.238-.097.47-.191.682-.284.985-.436 1-.722 1.02-1.067l.008-.127q0-.039.004-.079l.004-.078a3.35 3.35 0 0 1-.916-1.351l-.008-.008q0-.005-.003-.01l-.004-.012a3 3 0 0 1-.113-.368c-.262-.045-.412-.323-.472-.585-.053-.105-.173-.36-.15-.646.037-.382.195-.555.375-.623v-.06c0-.48.037-1.163.127-1.613.015-.128.045-.248.083-.375a2.8 2.8 0 0 1 .96-1.396C6.742 1.188 7.41 1 8.003 1s1.261.195 1.741.548a2.76 2.76 0 0 1 1.043 1.77c.083.451.128 1.142.128 1.614V5c.165.068.315.24.353.615a1.2 1.2 0 0 1-.15.653c-.053.255-.203.533-.458.586a3 3 0 0 1-.113.36c-.007.007-.015.037-.015.037-.202.533-.51.998-.893 1.336 0 .06 0 .12.008.173q.006.078.008.15c.011.335.021.618.99 1.043.212.093.444.187.683.285M4.5 7.521a1.6 1.6 0 0 1-.282-.308 2 2 0 0 1-.279-.593c-.304-.652-.29-1.486.153-2.074.023-.628.065-1.278.244-1.884a4 4 0 0 1 .177-.473A2.9 2.9 0 0 0 3.497 2c-.543 0-1.156.179-1.596.502a2.53 2.53 0 0 0-.956 1.624 9.5 9.5 0 0 0-.117 1.479v.062c-.152.062-.29.22-.323.564a1.1 1.1 0 0 0 .137.598c.048.234.186.489.42.537.027.11.062.227.103.33a3.1 3.1 0 0 0 .832 1.259q.002.084-.007.158-.006.072-.007.139c-.01.306-.02.565-.908.955C.281 10.556 0 11.046 0 12v3h1s-.16-2.356 0-3 .572-1.184 1.108-1.59c.61-.46 1.333-.753 2.04-1.039l.213-.087c.857-.35.7-.644.421-1.164a5 5 0 0 1-.282-.6m7 .001a1.6 1.6 0 0 0 .282-.308c.136-.193.224-.401.278-.593.305-.652.292-1.486-.152-2.074-.024-.628-.065-1.278-.244-1.884a4 4 0 0 0-.177-.473A2.9 2.9 0 0 1 12.503 2c.543 0 1.156.179 1.596.502a2.53 2.53 0 0 1 .956 1.624c.076.412.117 1.045.117 1.479v.062c.151.062.289.22.323.564a1.1 1.1 0 0 1-.137.598c-.048.234-.186.489-.42.537-.027.11-.062.227-.103.33a3.1 3.1 0 0 1-.832 1.259q-.002.084.006.158.006.072.008.139c.01.306.02.565.907.955C15.72 10.556 16 11.046 16 12v3h-1s.16-2.356 0-3-.572-1.184-1.108-1.59c-.61-.46-1.333-.753-2.04-1.039l-.213-.087c-.857-.35-.7-.644-.421-1.164a5 5 0 0 0 .283-.599"];
})), OT, kT = o((() => {
	OT = ["M8.5 0A1.5 1.5 0 0 0 7 1.5v7.837a3.5 3.5 0 1 0 3 0V1.5A1.5 1.5 0 0 0 8.5 0M2 5.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M2.5 1a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zM4 3.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 0 1h-1a.5.5 0 0 1-.5-.5M4.5 7a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"];
})), AT, jT = o((() => {
	AT = ["M9 10H2V6h7V4H1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h8zm4 3h-1V3h1c.55 0 1-.45 1-1s-.45-1-1-1h-1c-.37 0-.7.11-1 .28-.3-.17-.63-.28-1-.28H9c-.55 0-1 .45-1 1s.45 1 1 1h1v10H9c-.55 0-1 .45-1 1s.45 1 1 1h1c.37 0 .7-.11 1-.28.3.17.63.28 1 .28h1c.55 0 1-.45 1-1s-.45-1-1-1m2-9h-2v2h1v4h-1v2h2c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1"];
})), MT, NT = o((() => {
	MT = ["M15 1H1c-.6 0-1 .5-1 1v12c0 .6.4 1 1 1h14c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1M6 13H2v-2h4zm0-3H2V8h4zm0-3H2V5h4zm8 6H7v-2h7zm0-3H7V8h7zm0-3H7V5h7z"];
})), PT, FT = o((() => {
	PT = ["M13 0a1 1 0 0 0-1 1v1h-1a1 1 0 1 0 0 2h1v1a1 1 0 1 0 2 0V4h1a1 1 0 1 0 0-2h-1V1a1 1 0 0 0-1-1M8.764 5H7v2h3.764a3.001 3.001 0 0 0 5.108-1.129L16 5.83V14c0 .6-.4 1-1 1H1c-.6 0-1-.4-1-1V2c0-.5.4-1 1-1h7.764A3 3 0 0 0 8 3c0 .768.289 1.47.764 2M6 5H2v2h4zm0 3H2v2h4zm1 2h7V8H7zm-1 1H2v2h4zm1 2h7v-2H7z"];
})), IT, LT = o((() => {
	IT = ["m5.6 10-.3.3c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3l2-2c.2-.2.3-.4.3-.7s-.1-.5-.3-.7l-2-2C6.5 6.1 6.3 6 6 6c-.5 0-1 .4-1 1 0 .3.1.5.3.7l.3.3H1c-.6 0-1 .4-1 1s.4 1 1 1zM15 1H2c-.5 0-1 .5-1 1v5h2V5h11v2H8.8l.6.6c.1.1.2.3.3.4H14v2H9.7c-.1.1-.2.3-.3.4l-.6.6H14v2H3v-2H1v3c0 .5.5 1 1 1h13c.6 0 1-.5 1-1V2c0-.5-.4-1-1-1"];
})), RT, zT = o((() => {
	RT = ["M12 1h3c.6 0 1 .5 1 1v12c0 .6-.4 1-1 1h-4.97l.286-2H14v-2h-3.398l.143-1H14V8h-2.97l.143-1H14V5h-2.541l.51-3.576Q12 1.211 12 1M5.97 1l-.572 4H2v2h3.112L4.97 8H2v2h2.684l-.143 1H2v2h2.255l-.225 1.576Q4 14.789 4 15H1c-.6 0-1-.4-1-1V2c0-.5.4-1 1-1zM8.01.859a1 1 0 1 1 1.98.282l-2 14a1 1 0 1 1-1.98-.282z"];
})), BT, VT = o((() => {
	BT = ["M10 10h3l1.78-2.226a1 1 0 0 0 .22-.625V4.3l1-.9V14c0 .6-.4 1-1 1H1c-.6 0-1-.4-1-1V2c0-.5.4-1 1-1h4.333L9 4.3V5H7v2h2v1H7v2zm-4 3v-2H2v2zm0-3V8H2v2zm0-3V5H2v2zm8 6v-2H7v2zm1.48-13c.31 0 .52.26.52.57 0 .16-.06.3-.17.41l-2.86 2.73v2.63c0 .16-.06.3-.17.41l-.82 1.1c-.1.1-.25.17-.41.17-.31 0-.57-.26-.57-.57V3.71L8.17.98A.57.57 0 0 1 8 .57c0-.31.26-.57.57-.57z"];
})), HT, UT = o((() => {
	HT = ["M15 1H1c-.6 0-1 .5-1 1v12c0 .6.4 1 1 1h14c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1m-1 12H2v-2h12zm0-3H2V8h12zm0-3H2V5h12z"];
})), WT, GT = o((() => {
	WT = ["M12 1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0V4h-1a1 1 0 1 1 0-2h1zM8 3c0 .768.289 1.47.764 2H2v2h8.764c.55.614 1.348 1 2.236 1H2v2h12V8h-1a3 3 0 0 0 2.872-2.129L16 5.83V14c0 .6-.4 1-1 1H1c-.6 0-1-.4-1-1V2c0-.5.4-1 1-1h7.764A3 3 0 0 0 8 3M7 13h7v-2H2v2z"];
})), KT, qT = o((() => {
	KT = ["M7 8a1 1 0 0 0 0-2H4a1 1 0 0 0-1 1v3a1 1 0 0 0 2 0v-.637l2.36 2.358a.962.962 0 0 0 1.36-1.358L6.355 8zM1 1c-.6 0-1 .5-1 1v12a1 1 0 0 0 1 1h14c.6 0 1-.4 1-1V2a1 1 0 0 0-1-1zm13 12H2V5h12z"];
})), JT, YT = o((() => {
	JT = ["M12 1a.999.999 0 1 1 2 0v1h1a1 1 0 0 1 .83.44 1 1 0 0 1-.02 1.148A1 1 0 0 1 15 4h-1v1a1 1 0 0 1-.49.86 1 1 0 0 1-.9.061A1 1 0 0 1 12 5V4h-1a1 1 0 0 1-.83-.44 1 1 0 0 1 .033-1.164A1 1 0 0 1 11 2h1zm2 6.83a3 3 0 0 0 1.872-1.959q.065-.02.128-.042V14c0 .6-.4 1-1 1H1a1 1 0 0 1-1-1V2c0-.5.4-1 1-1h7.764A3 3 0 0 0 8 3c0 .768.289 1.47.764 2H2v8h12zm-6.64 3.89L5 9.363V10a1 1 0 0 1-2 0V7a1 1 0 0 1 1-1h3a1 1 0 0 1 0 2h-.645l2.365 2.362a.962.962 0 0 1-1.36 1.359"];
})), XT, ZT = o((() => {
	XT = ["M4.448 9q.146.436.325.795l.012.025a2 2 0 0 0 .185.92c.055.197.143.383.26.55q.107.141.24.26a4 4 0 0 0 .202.441 6 6 0 1 1 6.254-6.933 3 3 0 0 0-.336-.018 3 3 0 0 0-.5 0l-.177.028A5 5 0 0 0 10.584 4H8.829q.09.5.133 1.037A4 4 0 0 0 8.46 5a3.4 3.4 0 0 0-.502.042A10 10 0 0 0 7.812 4H4.188C4.068 4.609 4 5.283 4 6s.068 1.391.188 2h.995a9 9 0 0 0-.083.87 2 2 0 0 0-.079.13zM3.171 8C3.06 7.374 3 6.701 3 6s.06-1.374.17-2H1.417A5 5 0 0 0 1 6c0 .711.148 1.388.416 2zM2 9a5 5 0 0 0 2.086 1.62A6.8 6.8 0 0 1 3.401 9zm2.448-6h3.104a6 6 0 0 0-.325-.795C6.737 1.225 6.246 1 6 1s-.737.225-1.227 1.205q-.179.358-.325.795m4.15 0H10a5 5 0 0 0-2.086-1.62c.273.453.506 1.002.685 1.62M4.087 1.38A5 5 0 0 0 2 3h1.4a6.8 6.8 0 0 1 .685-1.62M13.476 16s.118-.385-.172-1.046c-.228-.533-1.172-.915-2.015-1.257a22 22 0 0 1-.584-.243c-.808-.356-.816-.588-.825-.872q-.002-.062-.007-.128v-.139c.314-.284.573-.669.745-1.115 0 0 .008-.023.008-.03q.06-.15.095-.3c.212-.04.33-.27.377-.485a.94.94 0 0 0 .125-.547c-.024-.307-.15-.453-.29-.515v-.054c0-.392-.04-.961-.11-1.33a2 2 0 0 0-.071-.308 2.3 2.3 0 0 0-.8-1.17C9.558 6.162 9.001 6 8.506 6s-1.052.162-1.445.462A2.3 2.3 0 0 0 6.19 7.93c-.07.369-.11.946-.11 1.338v.046c-.14.062-.274.208-.306.523a1 1 0 0 0 .126.547c.047.215.173.453.393.492.02.083.05.172.078.253l.016.047c0 .008.008.015.008.015v.008c.172.454.44.846.761 1.115l-.004.072-.004.06-.007.105c-.016.287-.028.523-.848.894-.176.078-.37.156-.568.237-.847.345-1.802.735-2.031 1.27C3.41 15.616 3.52 16 3.52 16zm2.503-1.25h-1.413a4 4 0 0 0-.116-.294c-.192-.445-.52-.753-.787-.955a5.3 5.3 0 0 0-.873-.517 21 21 0 0 0-1.122-.483l-.02-.008-.235-.097q.216-.347.366-.731c.089-.087.162-.177.22-.26a2 2 0 0 0 .271-.568c.117-.251.24-.64.199-1.105a2 2 0 0 0-.299-.925 9 9 0 0 0-.116-1.083 3.4 3.4 0 0 0-.104-.45 3.5 3.5 0 0 0-.661-1.246A2 2 0 0 1 11.63 6c.432 0 .92.141 1.264.404.33.256.584.612.7 1.023.028.087.049.182.062.27.062.322.097.82.097 1.164v.047c.123.053.233.181.254.45a.8.8 0 0 1-.11.478c-.041.189-.144.391-.33.425a2 2 0 0 1-.082.262c0 .007-.007.027-.007.027-.151.39-.378.727-.653.976v.121q.005.057.006.111v.002c.008.247.015.451.722.762.158.07.332.14.51.213.739.299 1.565.634 1.764 1.1.254.579.151.915.151.915"];
})), QT, $T = o((() => {
	QT = ["M2 2H0v7h2c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m13.99 4.38c.08-.58-.44-1.02-1.15-1.05-.25-.01-.52-.03-.81-.05.02 0 .05-.01.07-.01.7-.1 1.34-.49 1.41-1.07.06-.58-.46-.97-1.17-1.04-.25-.02-.52-.04-.79-.06.47-.15.84-.42.87-.93.04-.58-.79-1.03-1.5-1.09-.27-.02-.51-.04-.73-.05h-.09c-.23-.02-.43-.02-.62-.03C8.35.95 5.66 1.47 4 2.51v6c2.14 1.29 4.76 3.59 4.21 5.51-.18.59.31 1.05.98.98.81-.09 1.37-.91 1.4-1.78.04-1-.15-2.01-.5-2.91-.04-.25.01-.5.37-.53.49-.03 1.11-.06 1.59-.08.26 0 .51-.01.75-.02h.01c.41-.02.8-.05 1.13-.09.7-.09 1.35-.47 1.43-1.05s-.44-.97-1.15-1.05c-.05-.01-.11-.01-.16-.02.17-.01.33-.03.49-.05.72-.08 1.37-.46 1.44-1.04"];
})), eE, tE = o((() => {
	eE = ["M15.99 9.62c-.08-.58-.73-.96-1.43-1.05-.15-.02-.32-.04-.49-.05.06-.01.11-.01.16-.02.71-.08 1.23-.47 1.15-1.05s-.73-.96-1.43-1.05c-.34-.04-.72-.07-1.13-.09h-.01c-.24-.01-.49-.02-.75-.02-.48-.02-1.11-.04-1.59-.08-.36-.03-.41-.28-.37-.53.35-.9.54-1.91.5-2.91-.04-.85-.6-1.68-1.41-1.77-.67-.07-1.16.39-.99.98C8.76 3.91 6.13 6.2 4 7.49v6c1.66 1.03 4.35 1.56 7.48 1.5.19 0 .39-.01.62-.02h.09c.22-.01.46-.03.73-.05.71-.06 1.54-.51 1.5-1.09-.03-.51-.4-.79-.87-.93.27-.02.54-.04.79-.06.71-.06 1.24-.45 1.17-1.04-.06-.58-.7-.97-1.41-1.07-.02 0-.05-.01-.07-.01.29-.02.57-.03.81-.05.71-.03 1.23-.47 1.15-1.05M2 7H0v7h2c.55 0 1-.45 1-1V8c0-.56-.45-1-1-1"];
})), nE, rE = o((() => {
	nE = ["M14 3c-.28 0-.53.11-.71.29L6 10.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l8-8A1.003 1.003 0 0 0 14 3"];
})), iE, aE = o((() => {
	iE = ["M8 16c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m4-11c-.28 0-.53.11-.71.29L7 9.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l5-5A1.003 1.003 0 0 0 12 5"];
})), oE, sE = o((() => {
	oE = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6m1-6.41V4c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .28.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42z"];
})), cE, lE = o((() => {
	cE = ["M15 2.59 9.91 7.68 6.6 5.2l-.01.01C6.42 5.09 6.23 5 6 5c-.24 0-.44.09-.62.23v-.01L3 7.12V11h12zM15 12H2V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), uE, dE = o((() => {
	uE = ["M8 12h1c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1m5 0h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1m2 1H2c-.55 0-1 .45-1 1s.45 1 1 1h13c.55 0 1-.45 1-1s-.45-1-1-1M3 12h1c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1"];
})), fE, pE = o((() => {
	fE = ["M8 11H7v1h1zm-4 0H3v1h1zm7-8c.6 0 1-.5 1-1V1c0-.5-.4-1-1-1s-1 .5-1 1v1c0 .5.5 1 1 1M4 3c.5 0 1-.5 1-1V1c0-.5-.5-1-1-1S3 .5 3 1v1c0 .5.5 1 1 1m10-2h-1v1c0 1.1-.9 2-2 2s-2-.9-2-2V1H6v1c0 1.1-.9 2-2 2s-2-.9-2-2V1H1c-.5 0-1 .5-1 1v12c0 .5.5 1 1 1h13c.6 0 1-.5 1-1V2c0-.5-.4-1-1-1M5 13H2v-3h3zm0-4H2V6h3zm4 4H6v-3h3zm0-4H6V6h3zm4 4h-3v-3h3zm0-4h-3V6h3zm-1-2h-1v1h1z"];
})), mE, hE = o((() => {
	mE = ["M15 12H2V9.41l3-3L8.29 9.7c.18.19.43.3.71.3s.53-.11.71-.29l6-6a1.003 1.003 0 0 0-1.42-1.42L9 7.59l-3.29-3.3C5.53 4.11 5.28 4 5 4s-.53.11-.71.29L2 6.59V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), gE, _E = o((() => {
	gE = ["M7.88 1s-4.9 6.28-4.9 8.9c.01 2.82 2.34 5.1 4.99 5.1 2.65-.01 5.03-2.3 5.03-5.13C12.99 7.17 7.88 1 7.88 1"];
})), vE, yE = o((() => {
	vE = ["M5 15c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H5zm7-15H4c-.55 0-1 .45-1 1v1h10V1c0-.55-.45-1-1-1M5 7v6h6V7l2-4H3zm2 0c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1s-1-.45-1-1z"];
})), bE, xE = o((() => {
	bE = ["M3.5 9a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7m9.5 1a3 3 0 1 1 0 6 3 3 0 0 1 0-6m-9.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m9.5 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2M5 0c1.46 0 2.527.668 3 2l.815 3.255a79 79 0 0 1 2.186.195L11 2h2l.001 3.688q1.048.142 2.013.312c.623.11.986.479.986 1v3.354a4.001 4.001 0 0 0-6.873 1.645H7.999l-.026-.002A4.5 4.5 0 0 0 .659 9.01l-.654.001v-.829C.003 7.386.002 6.423 0 6.022 0 5.5.376 4.99 1 4.99V1a1 1 0 0 1 1-1zm1 2H3v2.99c1.29.024 2.554.069 3.781.135z"];
})), SE, CE = o((() => {
	SE = ["M13 14h-1l1 2H3l1-2H3c-1.1 0-2-.9-2-2V2C1 .9 4.13 0 8 0s7 .9 7 2v10c0 1.1-.9 2-2 2m-2-2h2v-2h-2zM9 7h4V3H9zm-6 5h2v-2H3zm0-5h4V3H3z"];
})), wE, TE = o((() => {
	wE = ["m15.89 14.56-3.99-8h-.01c-.17-.33-.5-.56-.89-.56s-.72.23-.89.56h-.01L9 8.76 7.17 7.38l.23-.18C8.37 6.47 9 5.31 9 4V3h1c.55 0 1-.45 1-1s-.45-1-1-1H7c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1H1c-.55 0-1 .45-1 1s.45 1 1 1h6v1c0 .66-.32 1.25-.82 1.61l-.68.51-.68-.5C4.32 5.25 4 4.66 4 4H2c0 1.31.63 2.47 1.6 3.2l.23.17L1.4 9.2l.01.01C1.17 9.4 1 9.67 1 10c0 .55.45 1 1 1 .23 0 .42-.09.59-.21l.01.01 2.9-2.17 2.6 1.95-1.99 3.98h.01c-.07.13-.12.28-.12.44 0 .55.45 1 1 1 .39 0 .72-.23.89-.56h.01L8.62 14h4.76l.72 1.45h.01c.17.32.5.55.89.55.55 0 1-.45 1-1 0-.16-.05-.31-.11-.44M9.62 12 11 9.24 12.38 12z"];
})), EE, DE = o((() => {
	EE = ["M14.49 3.99h-13c-.28 0-.5.22-.5.5s.22.5.5.5h.5v10c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-10h.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5m-8.5 9c0 .55-.45 1-1 1s-1-.45-1-1v-6c0-.55.45-1 1-1s1 .45 1 1zm3 0c0 .55-.45 1-1 1s-1-.45-1-1v-6c0-.55.45-1 1-1s1 .45 1 1zm3 0c0 .55-.45 1-1 1s-1-.45-1-1v-6c0-.55.45-1 1-1s1 .45 1 1zm2-12h-4c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1h-4c-.55 0-1 .45-1 1v1h14v-1c0-.55-.45-1-1-1"];
})), OE, kE = o((() => {
	OE = ["M9 11.857V16H7v-4.143L1 13l3.885-4.44L3 9l3.07-4.297L5 5l3-5 3 5-1.07-.297L13 9l-1.885-.44L15 13z"];
})), AE, jE = o((() => {
	AE = ["M15 7c-.55 0-1 .45-1 1v.59l-4.29-4.3A1 1 0 0 0 9 4c-.16 0-.31.05-.44.11V4.1L5 5.88 1.45 4.11v.01C1.31 4.05 1.16 4 1 4c-.55 0-1 .45-1 1 0 .39.23.72.56.89v.01l4 2v-.01c.13.06.28.11.44.11s.31-.05.44-.11v.01L8.8 6.22 12.59 10H12c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1"];
})), ME, NE = o((() => {
	ME = ["M15 4h-3c-.55 0-1 .45-1 1s.45 1 1 1h.59L8.8 9.78 5.45 8.11v.01C5.31 8.05 5.16 8 5 8s-.31.05-.44.11V8.1l-4 2v.01c-.33.17-.56.5-.56.89 0 .55.45 1 1 1 .16 0 .31-.05.44-.11v.01L5 10.12l3.55 1.78v-.01c.14.06.29.11.45.11.28 0 .53-.11.71-.29L14 7.41V8c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1"];
})), PE, FE = o((() => {
	PE = ["M4 .917C4 .41 4.41 0 4.917 0h6.166c.507 0 .917.41.917.917V2h3a1 1 0 0 1 1 1v1a5 5 0 0 1-4.522 4.977A4 4 0 0 1 9 10.874V14h2a1 1 0 1 1 0 2H5a1 1 0 1 1 0-2h2v-3.126a4 4 0 0 1-2.478-1.897A5 5 0 0 1 0 4V3a1 1 0 0 1 1-1h3zM4 4H2c0 1.306.835 2.417 2 2.83zm8 2.83A3 3 0 0 0 14 4h-2z"];
})), IE, LE = o((() => {
	IE = ["M12.5 0a.5.5 0 0 1 .5.5V9a1 1 0 0 1 1 1v2h.5a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H13v1a1 1 0 0 1-2 0v-1H5v1a1 1 0 0 1-2 0v-1H1.5a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5H2v-2a1 1 0 0 1 1-1V.5a.5.5 0 0 1 1 0V3a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2V.5a.5.5 0 0 1 .5-.5M9 8H7a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1m3.5 3h-1a.5.5 0 1 0 0 1h1a.5.5 0 1 0 0-1m-8 0h-1a.5.5 0 1 0 0 1h1a.5.5 0 1 0 0-1M9 9a.5.5 0 0 1 .5.5v1l-.008.09A.5.5 0 0 1 9 11H7l-.09-.008a.5.5 0 0 1-.41-.492v-1l.008-.09A.5.5 0 0 1 7 9Zm2-5H5v2h6z"];
})), RE, zE = o((() => {
	RE = ["M3.99-.01h-3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-14c0-.55-.45-1-1-1m11.71 7.3-2-2a1.003 1.003 0 0 0-1.71.71v4a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M9.99-.01h-3c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-14c0-.55-.45-1-1-1"];
})), BE, VE = o((() => {
	BE = ["M13.382 0a1 1 0 0 1 .894.553L16 4v11a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V4L1.724.553A1 1 0 0 1 2.618 0zM8 6c-.28 0-.53.11-.71.29l-2 2-.084.096A1.003 1.003 0 0 0 6.71 9.71l.29-.3V12l.007.116c.058.496.482.884.993.884.55 0 1-.45 1-1V9.41l.29.29.081.076A.97.97 0 0 0 10 10a1.003 1.003 0 0 0 .71-1.71l-2-2-.096-.084A1 1 0 0 0 8 6m5-4H3L2 4h12z"];
})), HE, UE = o((() => {
	HE = ["M8 14c2.8 0 5-2.2 5-5V3c0-.6-.4-1-1-1s-1 .4-1 1v6c0 1.7-1.3 3-3 3s-3-1.3-3-3V3c0-.6-.4-1-1-1s-1 .4-1 1v6c0 2.8 2.2 5 5 5m5.5 1h-11c-.3 0-.5.2-.5.5s.2.5.5.5h11c.3 0 .5-.2.5-.5s-.2-.5-.5-.5"];
})), WE, GE = o((() => {
	WE = ["M4 11c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m7-7H3.41L4.7 2.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 4.47 0 4.72 0 5s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L3.41 6H11c1.66 0 3 1.34 3 3s-1.34 3-3 3H7v2h4c2.76 0 5-2.24 5-5s-2.24-5-5-5"];
})), KE, qE = o((() => {
	KE = ["M3.5 5C1.57 5 0 6.57 0 8.5S1.57 12 3.5 12 7 10.43 7 8.5 5.43 5 3.5 5m9 0C10.57 5 9 6.57 9 8.5s1.57 3.5 3.5 3.5S16 10.43 16 8.5 14.43 5 12.5 5"];
})), JE, YE = o((() => {
	JE = ["M10.507 9.75v-3.5c0-.089.023-.171.051-.25h-7.55c-.176 0-.061-.824 0-1l.729-1.63c.06-.177.095-.37.27-.37h4.5V1.01c-.166-.003-.32-.01-.5-.01-2.72 0-4.036.402-4.036.402-.508.155-1.079.711-1.268 1.237L1.94 4.756H.887c-.483 0-.88.423-.88.939s.397.939.88.939h.376L1.008 7c-.034.685 0 1.436 0 2v5c0 .657.384 1 1 1s1-.343 1-1v-1h10v1c0 .657.383 1 1 1s1-.343 1-1v-3.5h-3.75a.75.75 0 0 1-.75-.75m-5.5.25h-2V8h2zM15.34.826a2.8 2.8 0 0 0-.932-.598q-.58-.24-1.445-.241-.67 0-1.213.228-.542.229-.926.636c-.384.407-.456.592-.598.963a3.5 3.5 0 0 0-.218 1.144V3h1.789c.003-.208.023-.405.069-.588q.074-.29.225-.506.153-.216.39-.345.239-.13.567-.13.488 0 .762.272.275.27.275.839.012.333-.116.555a1.7 1.7 0 0 1-.335.408 7 7 0 0 1-.452.37q-.243.185-.463.438a2.6 2.6 0 0 0-.384.611q-.165.358-.2.889V6h1.645v-.1q.048-.371.237-.618.189-.246.433-.438t.518-.383a2.4 2.4 0 0 0 .878-1.117q.153-.383.152-.975A2.24 2.24 0 0 0 15.34.826M12.007 7v2h2V7z"];
})), XE, ZE = o((() => {
	XE = ["M11.998.005a3.996 3.996 0 0 1 3.997 3.998c0 1.109-.46 2.088-1.19 2.808l.02.02-.999 1-.02-.02a3.97 3.97 0 0 1-2.052 1.114l-.93-.929 1.583-1.595 1-1-.01-.01c.36-.36.6-.849.6-1.398 0-1.1-.9-2-2-2-.55 0-1.039.24-1.399.6l-.01-.01L8 5.172l-.924-.925A4.04 4.04 0 0 1 8.19 2.194l-.02-.02 1-1 .02.02A3.93 3.93 0 0 1 11.997.005M2.293 2.293a1 1 0 0 1 1.414 0l10 10a1 1 0 0 1-1.414 1.414L8.936 10.35q.061.318.063.648c0 1.1-.46 2.089-1.189 2.808l.02.02-1 1-.02-.02a3.93 3.93 0 0 1-2.808 1.189 3.996 3.996 0 0 1-3.997-3.997c0-1.1.46-2.09 1.19-2.809l-.02-.02.999-1 .02.02a3.93 3.93 0 0 1 2.808-1.188q.334.001.649.064L2.293 3.707a1 1 0 0 1 0-1.414m5.71 7.124-2.292 2.29a1.002 1.002 0 0 1-1.42-1.42l2.292-2.29-.694-.694-3.296 3.295.01.01c-.36.36-.6.85-.6 1.4 0 1.099.9 1.998 2 1.998.55 0 1.039-.24 1.399-.6l.01.01 3.295-3.295zm.702-3.54 1.584-1.585a1.002 1.002 0 0 1 1.42 1.42l-1.585 1.583z"];
})), QE, $E = o((() => {
	QE = ["M11.99-.01c-2.21 0-4 1.79-4 4v3h-7c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-7c0-.55-.45-1-1-1h-3v-3c0-1.1.9-2 2-2s2 .9 2 2v1c0 .55.45 1 1 1s1-.45 1-1v-1c0-2.21-1.79-4-4-4"];
})), eD, tD = o((() => {
	eD = ["M9.39 1c-.5.5-.4 1.48.15 2.53L4.38 7.54C2.85 6.5 1.52 6.07 1 6.59l3.5 3.5c-.02.02-1.4 2.8-1.4 2.8l2.8-1.4 3.5 3.5c.53-.53.1-1.86-.95-3.38l4.02-5.16c1.04.55 2.01.65 2.51.14z"];
})), nD, rD = o((() => {
	nD = ["M11 3c-.55 0-1.07.09-1.57.26a6.46 6.46 0 0 1 0 9.48c.5.17 1.02.26 1.57.26 2.76 0 5-2.24 5-5s-2.24-5-5-5M9.78 9.38l.09-.27c.08-.36.13-.73.13-1.11s-.05-.75-.13-1.11l-.09-.27a5.3 5.3 0 0 0-.29-.79l-.12-.21c-.14-.27-.31-.52-.51-.76a1 1 0 0 0-.08-.1c-.24-.27-.49-.52-.78-.74-.43-.32-.92-.58-1.45-.75l.01-.01c-.1-.03-.2-.05-.3-.08-.12-.03-.23-.07-.36-.09A5.3 5.3 0 0 0 5 3C2.24 3 0 5.24 0 8s2.24 5 5 5c.31 0 .61-.04.9-.09.12-.02.24-.06.36-.09.1-.03.21-.04.3-.08l-.01-.01c.88-.29 1.64-.8 2.22-1.49.03-.03.06-.07.09-.1.19-.24.36-.49.51-.76.04-.07.08-.14.11-.21.13-.25.23-.52.3-.79"];
})), iD, aD = o((() => {
	iD = ["M8 0a7.95 7.95 0 0 0-6 2.74V1c0-.55-.45-1-1-1S0 .45 0 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.54C4.64 2.78 6.22 2 8 2c3.31 0 6 2.69 6 6 0 2.61-1.67 4.81-4 5.63-.63.22-1.29.37-2 .37-3.31 0-6-2.69-6-6 0-.55-.45-1-1-1s-1 .45-1 1c0 4.42 3.58 8 8 8 .34 0 .67-.03 1-.07.02 0 .04-.01.06-.01C12.98 15.4 16 12.06 16 8c0-4.42-3.58-8-8-8m3 5c-.28 0-.53.11-.71.29L7 8.58 5.71 7.29a1.003 1.003 0 0 0-1.42 1.42l2 2c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 11 5"];
})), oD, sD = o((() => {
	oD = ["M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m3 8c-.28 0-.53-.11-.71-.29L9 6.41V12c0 .55-.45 1-1 1s-1-.45-1-1V6.41l-1.29 1.3a1.003 1.003 0 0 1-1.42-1.42l3-3C7.47 3.11 7.72 3 8 3s.53.11.71.29l3 3A1.003 1.003 0 0 1 11 8"];
})), cD, lD = o((() => {
	cD = ["M7.99-.01A8 8 0 0 0 .03 8.77c.01.09.03.18.04.28.02.15.04.31.07.47.02.11.05.22.08.34.03.13.06.26.1.38s.08.25.12.37c.04.11.08.21.12.32a7 7 0 0 0 .3.65c.07.14.14.27.22.4.04.07.08.13.12.2l.27.42.1.13a7.97 7.97 0 0 0 3.83 2.82c.03.01.05.02.07.03.37.12.75.22 1.14.29l.2.03c.39.06.79.1 1.2.1s.81-.04 1.2-.1l.2-.03c.39-.07.77-.16 1.14-.29.03-.01.05-.02.07-.03a8.04 8.04 0 0 0 3.83-2.82c.03-.04.06-.08.09-.13.1-.14.19-.28.28-.42.04-.07.08-.13.12-.2.08-.13.15-.27.22-.41.04-.08.08-.17.12-.26.06-.13.11-.26.17-.39.04-.1.08-.21.12-.32.04-.12.08-.24.12-.37s.07-.25.1-.38c.03-.11.06-.22.08-.34.03-.16.05-.31.07-.47.01-.09.03-.18.04-.28.02-.26.04-.51.04-.78-.03-4.41-3.61-7.99-8.03-7.99m0 14.4c-1.98 0-3.75-.9-4.92-2.31.67-.36 1.49-.66 2.14-.95 1.16-.52 1.04-.84 1.08-1.27.01-.06.01-.11.01-.17-.41-.36-.74-.86-.96-1.44v-.01c0-.01-.01-.02-.01-.02q-.075-.195-.12-.39c-.28-.05-.44-.35-.5-.63-.06-.11-.18-.38-.15-.69.04-.41.2-.59.38-.67v-.06c0-.51.05-1.24.14-1.72q.03-.195.09-.39c.17-.59.53-1.12 1.01-1.49.49-.38 1.19-.59 1.82-.59.62 0 1.32.2 1.82.59.48.37.84.9 1.01 1.49.04.13.07.26.09.4.09.48.14 1.21.14 1.72v.07c.18.08.33.26.37.66.03.31-.1.58-.16.69-.06.27-.21.57-.48.62-.03.13-.07.26-.12.38 0 .01-.01.04-.01.04-.21.57-.54 1.06-.94 1.42 0 .06.01.13.01.19.04.43-.12.75 1.05 1.27.65.29 1.47.6 2.14.95a6.42 6.42 0 0 1-4.93 2.31"];
})), uD, dD = o((() => {
	uD = ["M3.94 3.15c.47-.66 1.05-1.24 1.76-1.73l.13-.4c-1.11.45-2.05 1.01-2.84 1.7-1.02.88-1.8 1.9-2.32 3.05C.22 6.76 0 7.75 0 8.75c0 1.75.66 3.5 1.99 5.25l.13-.42c-.39-.94-.59-1.82-.59-2.63 0-1.28.22-2.64.67-4.1.45-1.45 1.03-2.69 1.74-3.7m7.51 6.41-.27-.15c-.3.41-.52.66-.66.77-.09.06-.21.1-.33.1-.15 0-.3-.1-.45-.28-.25-.33-.59-1.22-1.01-2.69.38-.65.69-1.08.95-1.28.19-.15.39-.22.59-.22.08 0 .22.03.43.08.2.06.39.08.54.08.22 0 .4-.07.54-.22.15-.15.22-.34.22-.57 0-.25-.07-.45-.22-.59-.15-.15-.35-.22-.63-.22-.24 0-.47.06-.69.17-.21.11-.49.36-.82.74-.25.28-.61.78-1.1 1.48a6.7 6.7 0 0 0-.97-2.38l-2.59.44-.05.27c.19-.04.36-.06.49-.06.26 0 .47.11.64.33q.39.51 1.11 3.12c-.37.49-.63.81-.77.96-.23.24-.41.4-.56.47q-.165.09-.39.09c-.11 0-.29-.06-.53-.18-.17-.07-.32-.11-.45-.11-.25 0-.46.08-.62.24s-.24.37-.24.61c0 .23.08.42.23.57s.35.22.61.22c.25 0 .48-.05.7-.15s.49-.32.82-.65.78-.86 1.36-1.59c.22.69.42 1.19.58 1.51.16.31.35.54.56.68s.47.21.79.21q.465 0 .93-.33c.4-.29.82-.77 1.26-1.47m2.56-8.54-.12.42c.39.95.59 1.82.59 2.64 0 1.09-.17 2.26-.5 3.51-.26.96-.6 1.87-1.02 2.71-.42.85-.82 1.51-1.21 1.98q-.585.72-1.44 1.32l-.14.4c1.11-.45 2.05-1.02 2.84-1.7 1.03-.89 1.81-1.91 2.33-3.05q.66-1.485.66-3c0-1.73-.66-3.48-1.99-5.23"];
})), fD, pD = o((() => {
	fD = ["M5.7 1.4c-.71.49-1.29 1.07-1.76 1.73-.71 1.01-1.29 2.25-1.74 3.7-.45 1.46-.67 2.82-.67 4.1 0 .81.2 1.69.59 2.63l-.13.42C.66 12.23 0 10.48 0 8.73c0-1 .22-1.99.67-2.98.52-1.15 1.3-2.17 2.32-3.05.79-.69 1.73-1.25 2.84-1.7zM10.54 4c.28 0 .48.07.63.22.15.14.22.34.22.59 0 .23-.07.42-.22.57-.14.15-.32.22-.54.22-.15 0-.34-.02-.54-.08a2.4 2.4 0 0 0-.43-.08c-.2 0-.4.07-.59.22-.26.2-.57.63-.95 1.28.298 1.044.558 1.795.772 2.261l-.976.42a1.5 1.5 0 0 0-.615.48L7.3 10.1c-.16-.32-.36-.82-.58-1.51-.58.73-1.03 1.26-1.36 1.59s-.6.55-.82.65-.45.15-.7.15c-.26 0-.46-.07-.61-.22a.78.78 0 0 1-.23-.57c0-.24.08-.45.24-.61s.37-.24.62-.24c.13 0 .28.04.45.11.24.12.42.18.53.18q.225 0 .39-.09c.15-.07.33-.23.56-.47.14-.15.4-.47.77-.96Q5.84 5.5 5.45 4.99c-.17-.22-.38-.33-.64-.33-.13 0-.3.02-.49.06l.05-.27 2.59-.44c.47.72.8 1.52.97 2.38.49-.7.85-1.2 1.1-1.48.33-.38.61-.63.82-.74.22-.11.45-.17.69-.17m2.3-3c1.33 1.75 1.99 3.5 1.99 5.23q0 1.328-.508 2.632l-1.68-.721q.088-.283.168-.57c.33-1.25.5-2.421.5-3.511 0-.82-.2-1.69-.59-2.64zM8.275 11.445l3.5 1.5a.5.5 0 0 0 .45 0l3.5-1.5a.5.5 0 0 0-.03-.905L12.2 9.04a.5.5 0 0 0-.395 0l-3.495 1.5a.496.496 0 0 0-.035.905M15.5 12.5q-.12.001-.225.055L12 14l-3.275-1.445a.498.498 0 1 0-.45.89l3.5 1.5a.5.5 0 0 0 .45 0l3.5-1.5A.5.5 0 0 0 16 13c0-.275-.225-.5-.5-.5"];
})), mD, hD = o((() => {
	mD = ["m9.703.29 1.997 2h.01c.18.18.29.43.29.71s-.11.53-.29.71l-1.997 2a1.002 1.002 0 0 1-1.418-1.42l.29-.29H4.998C4.449 4 4 3.55 4 3s.45-1 .999-1h3.565l-.29-.29A1.004 1.004 0 0 1 8.995 0c.28 0 .53.11.709.29M9.57 8.64c.2-.51.78-.77 1.29-.57s.77.78.57 1.29l-2.25 5.8c-.2.51-.66.84-1.18.84s-.98-.33-1.18-.84l-2.25-5.8c-.2-.51.05-1.09.57-1.29.51-.2 1.09.05 1.29.57L8 12.68z"];
})), gD, _D = o((() => {
	gD = ["M6 7c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1s1-.45 1-1V8c0-.55-.45-1-1-1M2 9c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1m8-5c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1m4-4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), vD, yD = o((() => {
	vD = ["M6 4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1M2 0c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m8 7c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1s1-.45 1-1V8c0-.55-.45-1-1-1m4 2c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1"];
})), bD, xD = o((() => {
	bD = ["M1 2h14c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1s.45 1 1 1m14 11H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M3 5c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1z"];
})), SD, CD = o((() => {
	SD = ["M16 0H0v1a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1zM0 15v1h16v-1a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1M8.707 3.293a1 1 0 0 0-1.414 0l-2 2a1 1 0 0 0 1.414 1.414L8 5.414l1.293 1.293a1 1 0 0 0 1.414-1.414zm-2 6a1 1 0 0 0-1.414 1.414l2 2a1 1 0 0 0 1.414 0l2-2a1 1 0 0 0-1.414-1.414L8 10.586z"];
})), wD, TD = o((() => {
	wD = ["M15 2H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1M5 11V5l6 3z"];
})), ED, DD = o((() => {
	ED = ["m11.918 11.107.737.737.052-.051A1 1 0 0 1 14.2 13.12l-.078.087-1.414 1.414a1 1 0 0 1-1.492-1.327l.029-.033-.863-.863c-.426.231-.89.402-1.38.502L9 14l.117.007A1 1 0 0 1 9 16H7l-.117-.007A1 1 0 0 1 7 14v-1.1a5 5 0 0 1-1.447-.539l-.846.846.078.087a1 1 0 0 1-1.492 1.327l-1.414-1.414-.078-.087a1 1 0 0 1 1.492-1.327l.744-.744A5 5 0 0 1 3.23 9.5H2a1 1 0 0 1-1.993.117L0 9.5v-2a1 1 0 0 1 1.993-.117L2 7.5h1.025a5 5 0 0 1 .905-2.405l-.512-.513-.125.125A1 1 0 0 1 1.8 3.38l.078-.087 1.414-1.414a1 1 0 0 1 1.529 1.277l.573.575a5 5 0 0 1 1.604-.63V2l-.116-.007a1 1 0 0 1 0-1.986L7 0h2a1 1 0 0 1 .117 1.993L9 2l.001 1.1c.639.13 1.233.381 1.757.73l.535-.537-.078-.087a1 1 0 0 1 1.492-1.327l1.414 1.414.078.087a1 1 0 0 1-1.492 1.327l-.535.536a5 5 0 0 1 .803 2.257H14l.007-.117A1 1 0 0 1 16 7.5v2l-.007.117A1 1 0 0 1 14 9.5h-1.229a5 5 0 0 1-.853 1.607M10 9a1 1 0 1 0 0 2 1 1 0 0 0 0-2M6.5 5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"];
})), OD, kD = o((() => {
	OD = ["M9 2c-.28 0-.53.11-.71.29L5.59 5H3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h2.59l2.71 2.71c.17.18.42.29.7.29.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m3.57 1.44-1.59 1.22C11.62 5.61 12 6.76 12 8s-.38 2.39-1.02 3.34l1.59 1.22C13.47 11.27 14 9.7 14 8s-.53-3.27-1.43-4.56"];
})), AD, jD = o((() => {
	AD = ["M11 2c-.28 0-.53.11-.71.29L7.59 5H5c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h2.59l2.71 2.71c.17.18.42.29.7.29.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), MD, ND = o((() => {
	MD = ["M7 1.86c-.28 0-.53.11-.71.29l-2.7 2.71H1c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h2.59l2.71 2.71a1.003 1.003 0 0 0 1.71-.71v-10c-.01-.55-.46-1-1.01-1m6.74-.99-1.58 1.22A10 10 0 0 1 14 7.86c0 2.16-.69 4.15-1.85 5.78l1.58 1.22c1.42-1.97 2.26-4.38 2.26-7 .01-2.61-.84-5.02-2.25-6.99M8.98 4.52C9.62 5.48 10 6.63 10 7.86s-.38 2.39-1.02 3.34l1.59 1.22c.9-1.29 1.43-2.86 1.43-4.56s-.53-3.27-1.43-4.56z"];
})), PD, FD = o((() => {
	PD = ["M13 8h-2c-.16 0-.31-.05-.44-.11v.01l-1.02-.51-.37 1.86 1.38.92-.01.02c.27.17.46.46.46.81v4c0 .55-.45 1-1 1s-1-.45-1-1v-3.46l-1.27-.85-1.8 4.67h-.01A.98.98 0 0 1 5 16c-.55 0-1-.45-1-1 0-.13.03-.25.07-.36h-.01L7.39 6H5.62l-.73 1.45h-.01C4.72 7.77 4.39 8 4 8c-.55 0-1-.45-1-1 0-.16.05-.31.11-.44H3.1l1-2h.01c.17-.33.5-.56.89-.56h3.16l.29-.75C8.17 2.9 8 2.47 8 2c0-1.1.9-2 2-2s2 .9 2 2c0 1-.73 1.82-1.69 1.97l-.5 1.32 1.43.71H13c.55 0 1 .45 1 1s-.45 1-1 1"];
})), ID, LD = o((() => {
	ID = ["m15.84 13.5.01-.01-7-12-.01.01c-.17-.3-.48-.5-.85-.5s-.67.2-.85.5l-.01-.01-7 12 .01.01c-.09.15-.15.31-.15.5 0 .55.45 1 1 1h14c.55 0 1-.45 1-1 0-.19-.06-.35-.15-.5m-6.85-.51h-2v-2h2zm0-3h-2v-5h2z"];
})), RD, zD = o((() => {
	RD = ["M8 7c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1m-4 4h1c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1m7-6c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1s-1 .45-1 1v1c0 .55.45 1 1 1m4-3h-1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m0 10H2V3c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), BD, VD = o((() => {
	BD = ["M3 1a1 1 0 0 1 .894.553c.102.202.393.607.779.957.419.381.72.49.827.49.108 0 .408-.109.827-.49.386-.35.677-.755.779-.957a1 1 0 0 1 1.788 0c.102.202.393.607.779.957.419.381.72.49.827.49.108 0 .408-.109.827-.49.386-.35.677-.755.779-.957a1 1 0 0 1 1.788 0c.173.344.38.75.637 1.072.277.347.437.375.469.375a1 1 0 1 1 0 2c-.968 0-1.642-.64-2.03-1.125l-.076-.097a6 6 0 0 1-.221.212C12.175 4.442 11.393 5 10.5 5c-.892 0-1.675-.558-2.173-1.01A6 6 0 0 1 8 3.67q-.158.165-.327.32C7.175 4.442 6.393 5 5.5 5c-.892 0-1.675-.558-2.173-1.01a6 6 0 0 1-.221-.212l-.075.097C2.64 4.36 1.968 5 1 5a1 1 0 0 1 0-2c.032 0 .191-.028.47-.375.256-.321.463-.728.636-1.072A1 1 0 0 1 3 1m0 5a1 1 0 0 1 .894.553c.102.202.393.607.779.957.419.381.72.49.827.49.108 0 .408-.109.827-.49.386-.35.677-.755.779-.957a1 1 0 0 1 1.788 0c.102.202.393.607.779.957.419.381.72.49.827.49.108 0 .408-.109.827-.49.386-.35.677-.755.779-.957a1 1 0 0 1 1.788 0c.173.344.38.75.637 1.072.277.347.437.375.469.375a1 1 0 1 1 0 2c-.968 0-1.642-.639-2.03-1.125l-.076-.097a6 6 0 0 1-.221.212c-.498.452-1.28 1.01-2.173 1.01-.892 0-1.675-.558-2.173-1.01A6 6 0 0 1 8 8.67q-.158.165-.327.32C7.175 9.442 6.393 10 5.5 10c-.892 0-1.675-.558-2.173-1.01a6 6 0 0 1-.221-.212l-.075.097C2.64 9.36 1.968 10 1 10a1 1 0 0 1 0-2c.032 0 .191-.028.47-.375.256-.321.463-.728.636-1.072A1 1 0 0 1 3 6m.894 5.553a1 1 0 0 0-1.788 0c-.173.344-.38.75-.637 1.072-.278.347-.437.375-.469.375a1 1 0 1 0 0 2c.968 0 1.642-.639 2.03-1.125l.076-.097q.108.109.221.212C3.825 14.442 4.607 15 5.5 15c.892 0 1.675-.558 2.173-1.01q.17-.155.327-.32.158.165.327.32c.498.452 1.28 1.01 2.173 1.01.892 0 1.675-.558 2.173-1.01q.113-.104.221-.212l.075.097C13.36 14.36 14.032 15 15 15a1 1 0 1 0 0-2c-.032 0-.191-.028-.47-.375-.256-.321-.463-.728-.636-1.072a1 1 0 0 0-1.788 0c-.102.202-.393.607-.779.957-.419.381-.72.49-.827.49-.108 0-.408-.109-.827-.49-.386-.35-.677-.755-.779-.957a1 1 0 0 0-1.788 0c-.102.202-.393.607-.779.957-.419.381-.72.49-.827.49-.108 0-.408-.109-.827-.49-.386-.35-.677-.755-.779-.957"];
})), HD, UD = o((() => {
	HD = ["M13 11h2V5h-2zM3 5H1v6h2zm11-1c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2M2 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M5 3h6V1H5zM2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m3 15h6v-2H5z"];
})), WD, GD = o((() => {
	WD = ["M1 3h14c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1m1 2v6h12V5zm3 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m3 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m3 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), KD, qD = o((() => {
	KD = ["M14 0H2c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H3v-3h10zm0-4H3V2h10z"];
})), JD, YD = o((() => {
	JD = ["M14 0H2c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 14H3V6h10zm0-9H3V2h10z"];
})), XD, ZD = o((() => {
	XD = ["M10 4a2 2 0 1 1 2 2H4a1 1 0 0 0 0 2h8a4 4 0 1 0-4-4 1 1 0 0 0 2 0M1 9a1 1 0 1 0 0 2h7.5a1.5 1.5 0 0 1 0 3c-.749 0-1.386-.538-1.52-1.199a1 1 0 1 0-1.96.398C5.35 14.82 6.83 16 8.5 16a3.5 3.5 0 1 0 0-7z"];
})), QD, $D = o((() => {
	QD = ["M2.75 5h3.5L7 2h2l.75 3h3.5L14 2h2l-.758 3.03A1 1 0 0 1 15 7h-.25l-.25 1h.5a1 1 0 1 1 0 2h-1l-1 4h-3l-1-4H7l-1 4H3l-1-4H1a1 1 0 0 1 0-2h.5l-.25-1H1a1 1 0 0 1-.243-1.97L0 2h2zm1.75 7 .5-2H4zm6.5-2 .5 2 .5-2zm-.75-3 .25 1h2l.25-1zM3.5 8h2l.25-1h-2.5zm4 0h1l-.25-1h-.5z"];
})), eO, tO = o((() => {
	eO = ["M12.5 7a3.5 3.5 0 1 1 0 7h-2.09l.29.29c.19.18.3.43.3.71a1.003 1.003 0 0 1-1.71.71l-2-2A1 1 0 0 1 7 13c0-.28.11-.53.29-.71l2-2a1.003 1.003 0 0 1 1.42 1.42l-.3.29h2.09a1.5 1.5 0 0 0 0-3H1a1 1 0 0 1 0-2zM4 12c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1zM15 2c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1z"];
})), nO, rO = o((() => {
	nO = ["m15.83 3.7-3.06 3.05-2.84-.7-.7-2.83L12.29.17a5 5 0 0 0-4.83 1.29 4.97 4.97 0 0 0-1.12 5.36L.58 12.58c-.36.36-.58.86-.58 1.41 0 1.1.9 2 2 2 .55 0 1.05-.22 1.41-.59l5.77-5.77c1.79.69 3.91.33 5.35-1.12 1.32-1.3 1.74-3.15 1.3-4.81"];
})), iO, aO = o((() => {
	iO = ["m7.71 3.71-2 2a1.003 1.003 0 0 1-1.42-1.42l.3-.29H3c-.55 0-1 .45-1 1s.45 1 1 1a1 1 0 1 1 0 2C1.34 8 0 6.66 0 5s1.34-3 3-3h1.59l-.3-.29A1.003 1.003 0 0 1 5.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71m1.875 8.863-2.98 2.98a1.526 1.526 0 0 1-2.158-2.158l2.98-2.98a4.502 4.502 0 0 1 6.013-5.977l-3 3.001a1.5 1.5 0 0 0 2.12 2.122l3.002-3.001a4.502 4.502 0 0 1-5.977 6.013"];
})), oO, sO = o((() => {
	oO = ["M1 0h4a1 1 0 0 1 .775 1.632L3.08 5H5a1 1 0 0 1 0 2H1a1 1 0 0 1-.771-1.636L2.919 2H1a1 1 0 1 1 0-2m8.585 12.573-2.98 2.98a1.526 1.526 0 0 1-2.158-2.158l2.98-2.98a4.502 4.502 0 0 1 6.013-5.977l-3 3.001a1.5 1.5 0 0 0 2.12 2.122l3.002-3.001a4.502 4.502 0 0 1-5.977 6.013"];
})), cO, lO = o((() => {
	cO = ["M0 3.5C0 1.57 1.57 0 3.5 0S7 1.57 7 3.5 5.43 7 3.5 7 0 5.43 0 3.5m3-2v2.21l1.56 1.56c.1.09.23.14.36.14.12 0 .25-.05.35-.14.19-.2.19-.51 0-.71L4 3.29V1.5c0-.28-.22-.5-.5-.5s-.5.22-.5.5m6.585 11.073-2.98 2.98a1.526 1.526 0 0 1-2.158-2.158l2.98-2.98a4.502 4.502 0 0 1 6.013-5.977l-3 3.001a1.5 1.5 0 0 0 2.12 2.122l3.002-3.001a4.502 4.502 0 0 1-5.977 6.013"];
})), uO, dO = o((() => {
	uO = ["M8 7.417 11 2h2L9.571 8H11a1 1 0 1 1 0 2H9v1h2a1 1 0 1 1 0 2H9v2H7v-2H5a1 1 0 1 1 0-2h2v-1H5a1 1 0 0 1 0-2h1.429L3 2h2z"];
})), fO, pO = o((() => {
	fO = ["M7.99 5.99v-2c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1zm7.56 7.44-2.67-2.68a6.94 6.94 0 0 0 1.11-3.76c0-3.87-3.13-7-7-7s-7 3.13-7 7 3.13 7 7 7c1.39 0 2.68-.42 3.76-1.11l2.68 2.67a1.498 1.498 0 1 0 2.12-2.12m-8.56-1.44c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), mO, hO = o((() => {
	mO = ["M3.99 5.99c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1zm11.56 7.44-2.67-2.68a6.94 6.94 0 0 0 1.11-3.76c0-3.87-3.13-7-7-7s-7 3.13-7 7 3.13 7 7 7c1.39 0 2.68-.42 3.76-1.11l2.68 2.67a1.498 1.498 0 1 0 2.12-2.12m-8.56-1.44c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), gO, _O = o((() => {
	gO = ["M11 10a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42L12.59 8 11.3 9.29c-.19.18-.3.43-.3.71M1 5c.55 0 1-.45 1-1V2h2c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v3c0 .55.45 1 1 1m4 1a1.003 1.003 0 0 0-1.71-.71l-2 2C1.11 7.47 1 7.72 1 8s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L3.41 8 4.7 6.71c.19-.18.3-.43.3-.71m1-1c.28 0 .53-.11.71-.29L8 3.41 9.29 4.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-2-2C8.53 1.11 8.28 1 8 1s-.53.11-.71.29l-2 2A1.003 1.003 0 0 0 6 5m9 6c-.55 0-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1m0-11h-3c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1M4 14H2v-2c0-.55-.45-1-1-1s-1 .45-1 1v3c0 .55.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1m6-3c-.28 0-.53.11-.71.29L8 12.59 6.71 11.3A.97.97 0 0 0 6 11a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 10 11"];
})), vO = /* @__PURE__ */ c({
	Add: () => On,
	AddApplication: () => An,
	AddChild: () => Mn,
	AddClip: () => Pn,
	AddColumnLeft: () => In,
	AddColumnRight: () => Rn,
	AddDerivedColumn: () => Bn,
	AddLocation: () => Hn,
	AddParent: () => Wn,
	AddRowBottom: () => Kn,
	AddRowTop: () => Jn,
	AddTile: () => Xn,
	AddToArtifact: () => Qn,
	AddToFolder: () => er,
	AimpointsTarget: () => nr,
	Airplane: () => ir,
	AlignCenter: () => or,
	AlignJustify: () => cr,
	AlignLeft: () => ur,
	AlignRight: () => fr,
	AlignmentBottom: () => mr,
	AlignmentHorizontalCenter: () => gr,
	AlignmentLeft: () => vr,
	AlignmentRight: () => br,
	AlignmentTop: () => Sr,
	AlignmentVerticalCenter: () => wr,
	Ammunition: () => Er,
	Anchor: () => Or,
	Annotation: () => Ar,
	Announcement: () => Mr,
	Antenna: () => Pr,
	AppHeader: () => Ir,
	Application: () => Rr,
	Applications: () => Br,
	Archive: () => Hr,
	AreaOfInterest: () => Wr,
	Array: () => Kr,
	ArrayBoolean: () => Jr,
	ArrayDate: () => Xr,
	ArrayFloatingPoint: () => Qr,
	ArrayNumeric: () => ei,
	ArrayObject: () => ni,
	ArrayString: () => ii,
	ArrayTimestamp: () => oi,
	ArrowBottomLeft: () => ci,
	ArrowBottomRight: () => ui,
	ArrowDown: () => fi,
	ArrowLeft: () => mi,
	ArrowRight: () => gi,
	ArrowTopLeft: () => A,
	ArrowTopRight: () => yi,
	ArrowUp: () => xi,
	ArrowsArc: () => Ci,
	ArrowsHorizontal: () => Ti,
	ArrowsVertical: () => Di,
	Asterisk: () => ki,
	At: () => ji,
	AutomaticUpdates: () => Ni,
	Axle: () => Fi,
	Backlink: () => Li,
	BackwardTen: () => zi,
	Badge: () => Vi,
	BanCircle: () => Ui,
	BankAccount: () => Gi,
	Barcode: () => qi,
	BinaryNumber: () => Yi,
	Blank: () => Zi,
	BlockPromote: () => $i,
	BlockedPerson: () => ta,
	Bold: () => j,
	Book: () => ra,
	Bookmark: () => ia,
	Box: () => oa,
	BranchLocked: () => ca,
	BranchUnlocked: () => ua,
	Briefcase: () => fa,
	BringData: () => ma,
	BringForward: () => ga,
	BritishPound: () => va,
	Bug: () => ba,
	Buggy: () => Sa,
	Build: () => wa,
	Bullseye: () => Ea,
	Calculator: () => Oa,
	Calendar: () => Aa,
	Camera: () => Ma,
	CaretDown: () => P,
	CaretLeft: () => Fa,
	CaretRight: () => La,
	CaretUp: () => za,
	CargoShip: () => Va,
	CellTower: () => Ua,
	Changes: () => Ga,
	Chart: () => qa,
	Chat: () => Ya,
	ChevronBackward: () => Za,
	ChevronDown: () => $a,
	ChevronForward: () => to,
	ChevronLeft: () => ro,
	ChevronRight: () => ao,
	ChevronUp: () => so,
	Circle: () => lo,
	CircleArrowDown: () => fo,
	CircleArrowLeft: () => mo,
	CircleArrowRight: () => go,
	CircleArrowUp: () => vo,
	CircleDashed: () => bo,
	Citation: () => So,
	Clean: () => wo,
	Clip: () => Eo,
	Clipboard: () => Oo,
	ClipboardFile: () => ko,
	Cloud: () => jo,
	CloudDownload: () => No,
	CloudServer: () => I,
	CloudTick: () => R,
	CloudUpload: () => Io,
	Code: () => Ro,
	CodeBlock: () => zo,
	Cog: () => Vo,
	CollapseAll: () => Uo,
	ColorFill: () => Go,
	ColumnLayout: () => qo,
	Comment: () => Yo,
	Comparison: () => Zo,
	Compass: () => $o,
	Compressed: () => ts,
	Confirm: () => rs,
	Console: () => as,
	ConsoleAlert: () => ss,
	Construction: () => ls,
	Contrast: () => ds,
	Control: () => ps,
	CreditCard: () => hs,
	Crop: () => _s,
	Cross: () => ys,
	CrossCircle: () => xs,
	Crown: () => Cs,
	CrystalBall: () => Ts,
	CssStyle: () => Ds,
	Cube: () => ks,
	CubeAdd: () => js,
	CubeCutout: () => Ns,
	CubeCutouts: () => Fs,
	CubeEdit: () => Ls,
	CubeRemove: () => zs,
	Cubes: () => Vs,
	CurlyBraces: () => Us,
	CurvedRangeChart: () => Gs,
	Cut: () => qs,
	Cycle: () => Ys,
	Dashboard: () => Zs,
	DataCloud: () => $s,
	DataConnection: () => tc,
	DataLineage: () => rc,
	DataSearch: () => ac,
	DataSync: () => sc,
	Database: () => lc,
	Delete: () => dc,
	DeleteClip: () => pc,
	Delta: () => hc,
	DeriveColumn: () => B,
	Descendant: () => vc,
	Desktop: () => V,
	Detection: () => H,
	Diagnosis: () => Sc,
	DiagramTree: () => wc,
	DirectionLeft: () => Ec,
	DirectionRight: () => Oc,
	Disable: () => Ac,
	Divide: () => Mc,
	Document: () => Nc,
	DocumentCode: () => Fc,
	DocumentLocked: () => Lc,
	DocumentOpen: () => zc,
	DocumentShare: () => Vc,
	Dollar: () => Uc,
	Dot: () => Gc,
	DoubleCaretHorizontal: () => qc,
	DoubleCaretVertical: () => W,
	DoubleChevronDown: () => K,
	DoubleChevronLeft: () => Yc,
	DoubleChevronRight: () => J,
	DoubleChevronUp: () => Qc,
	DoughnutChart: () => el,
	Download: () => nl,
	DragHandleHorizontal: () => il,
	DragHandleVertical: () => ol,
	Draw: () => cl,
	DrawerLeft: () => ul,
	DrawerLeftFilled: () => fl,
	DrawerRight: () => ml,
	DrawerRightFilled: () => gl,
	DriveTime: () => vl,
	Drone: () => bl,
	DroneUav: () => Sl,
	Duplicate: () => wl,
	Edit: () => El,
	Eject: () => Ol,
	Emoji: () => Al,
	Endnote: () => Ml,
	Endorsed: () => Pl,
	Engagement: () => Il,
	Envelope: () => Rl,
	Equals: () => Bl,
	Eraser: () => Y,
	Error: () => Ul,
	Euro: () => Gl,
	Excavator: () => ql,
	Exchange: () => Yl,
	ExcludeRow: () => Zl,
	ExpandAll: () => $l,
	Explain: () => tu,
	Export: () => ru,
	EyeOff: () => au,
	EyeOn: () => su,
	EyeOpen: () => lu,
	FastBackward: () => du,
	FastForward: () => pu,
	Feed: () => hu,
	FeedSubscribed: () => _u,
	FighterJet: () => yu,
	Film: () => xu,
	Filter: () => Cu,
	FilterKeep: () => Tu,
	FilterList: () => Du,
	FilterOpen: () => ku,
	FilterRemove: () => ju,
	FilterSortAsc: () => Nu,
	FilterSortDesc: () => Fu,
	Flag: () => Lu,
	Flame: () => zu,
	Flash: () => Vu,
	FloatingPoint: () => Uu,
	FloppyDisk: () => Gu,
	FlowBranch: () => qu,
	FlowEnd: () => Yu,
	FlowLinear: () => Zu,
	FlowReview: () => $u,
	FlowReviewBranch: () => td,
	Flows: () => rd,
	FolderClose: () => ad,
	FolderNew: () => sd,
	FolderOpen: () => ld,
	FolderShared: () => dd,
	FolderSharedOpen: () => pd,
	Follower: () => hd,
	Following: () => _d,
	Font: () => yd,
	Fork: () => xd,
	ForkEnd: () => Cd,
	Form: () => Td,
	ForwardTen: () => Dd,
	FrameToFrame: () => kd,
	Fuel: () => jd,
	FullCircle: () => Nd,
	FullStackedChart: () => Fd,
	Fullscreen: () => Ld,
	Function: () => zd,
	FunctionMinimal: () => Vd,
	GanttChart: () => Ud,
	Generate: () => Gd,
	Geofence: () => qd,
	Geolocation: () => Yd,
	Geosearch: () => Zd,
	Geotime: () => $d,
	GiftBox: () => tf,
	GitBranch: () => rf,
	GitCommit: () => of,
	GitMerge: () => cf,
	GitNewBranch: () => uf,
	GitPull: () => ff,
	GitPush: () => mf,
	GitRebase: () => gf,
	GitRepo: () => vf,
	Glass: () => bf,
	Globe: () => Sf,
	GlobeNetwork: () => wf,
	GlobeNetworkAdd: () => Ef,
	Graph: () => Of,
	GraphRemove: () => Af,
	GreaterThan: () => Mf,
	GreaterThanOrEqualTo: () => Pf,
	Grid: () => If,
	GridView: () => Rf,
	GroupItem: () => Bf,
	GroupObjects: () => Hf,
	GroupedBarChart: () => Wf,
	Hand: () => Kf,
	HandDown: () => Jf,
	HandLeft: () => Xf,
	HandRight: () => Qf,
	HandUp: () => ep,
	Hat: () => np,
	Header: () => ip,
	HeaderOne: () => op,
	HeaderThree: () => cp,
	HeaderTwo: () => up,
	Headset: () => fp,
	Heart: () => mp,
	HeartBroken: () => gp,
	HeatGrid: () => vp,
	Heatmap: () => bp,
	Helicopter: () => Sp,
	Help: () => wp,
	HelperManagement: () => Ep,
	Hexagon: () => Op,
	HighPriority: () => Ap,
	HighVoltagePole: () => Mp,
	Highlight: () => Pp,
	History: () => Ip,
	Home: () => Rp,
	HorizontalBarChart: () => Bp,
	HorizontalBarChartAsc: () => Hp,
	HorizontalBarChartDesc: () => Wp,
	HorizontalDistribution: () => Kp,
	HorizontalInbetween: () => Jp,
	Hurricane: () => Xp,
	IdNumber: () => Qp,
	ImageRotateLeft: () => em,
	ImageRotateRight: () => nm,
	Import: () => im,
	Inbox: () => om,
	InboxFiltered: () => cm,
	InboxGeo: () => um,
	InboxSearch: () => fm,
	InboxUpdate: () => mm,
	InfoSign: () => gm,
	Inheritance: () => vm,
	InheritedGroup: () => bm,
	InnerJoin: () => Sm,
	Input: () => wm,
	Insert: () => Em,
	Intelligence: () => Om,
	Intersection: () => Am,
	IpAddress: () => Mm,
	Issue: () => Pm,
	IssueClosed: () => Im,
	IssueNew: () => Rm,
	Italic: () => Bm,
	JoinTable: () => Hm,
	Key: () => Wm,
	KeyBackspace: () => Km,
	KeyCommand: () => Jm,
	KeyControl: () => Xm,
	KeyDelete: () => Qm,
	KeyEnter: () => eh,
	KeyEscape: () => nh,
	KeyOption: () => ih,
	KeyShift: () => oh,
	KeyTab: () => ch,
	KnownVehicle: () => uh,
	LabTest: () => fh,
	Label: () => mh,
	Layer: () => gh,
	LayerOutline: () => vh,
	Layers: () => bh,
	Layout: () => Sh,
	LayoutAuto: () => wh,
	LayoutBalloon: () => Eh,
	LayoutBottomRowThreeTiles: () => Oh,
	LayoutBottomRowTwoTiles: () => Ah,
	LayoutCircle: () => Mh,
	LayoutGrid: () => Ph,
	LayoutGroupBy: () => Ih,
	LayoutHierarchy: () => Rh,
	LayoutLeftColumnThreeTiles: () => Bh,
	LayoutLeftColumnTwoTiles: () => Hh,
	LayoutLinear: () => Wh,
	LayoutRightColumnThreeTiles: () => Kh,
	LayoutRightColumnTwoTiles: () => Jh,
	LayoutSkewGrid: () => Xh,
	LayoutSortedClusters: () => Qh,
	LayoutThreeColumns: () => eg,
	LayoutThreeRows: () => ng,
	LayoutTopRowThreeTiles: () => ig,
	LayoutTopRowTwoTiles: () => og,
	LayoutTwoColumns: () => cg,
	LayoutTwoRows: () => ug,
	Learning: () => fg,
	LeftJoin: () => mg,
	LengthenText: () => gg,
	LessThan: () => vg,
	LessThanOrEqualTo: () => bg,
	Lifesaver: () => Sg,
	Lightbulb: () => wg,
	Lightning: () => Eg,
	Link: () => Og,
	LinkedSquares: () => Ag,
	List: () => Mg,
	ListColumns: () => Pg,
	ListDetailView: () => Ig,
	Locate: () => Rg,
	Lock: () => Bg,
	Locomotive: () => Hg,
	LogIn: () => Wg,
	LogOut: () => Kg,
	LowVoltagePole: () => Jg,
	Manual: () => Xg,
	ManuallyEnteredData: () => Qg,
	ManyToMany: () => e_,
	ManyToOne: () => n_,
	Map: () => i_,
	MapCreate: () => o_,
	MapMarker: () => c_,
	Markdown: () => u_,
	Maximize: () => f_,
	Media: () => m_,
	Menu: () => g_,
	MenuClosed: () => v_,
	MenuOpen: () => b_,
	MergeColumns: () => S_,
	MergeLinks: () => w_,
	Microphone: () => E_,
	Minimize: () => O_,
	Minus: () => A_,
	MobilePhone: () => M_,
	MobileVideo: () => P_,
	Modal: () => I_,
	ModalFilled: () => R_,
	Model: () => B_,
	Moon: () => H_,
	More: () => W_,
	Mountain: () => K_,
	Move: () => J_,
	Mugshot: () => X_,
	MultiSelect: () => Q_,
	Music: () => ev,
	Nest: () => nv,
	NewComment: () => iv,
	NewDrawing: () => ov,
	NewGridItem: () => cv,
	NewLayer: () => uv,
	NewLayers: () => fv,
	NewLink: () => mv,
	NewObject: () => gv,
	NewPerson: () => vv,
	NewPrescription: () => bv,
	NewShield: () => Sv,
	NewTextBox: () => wv,
	Ninja: () => Ev,
	NotEqualTo: () => Ov,
	Notifications: () => Av,
	NotificationsAdd: () => Mv,
	NotificationsSnooze: () => Pv,
	NotificationsUpdated: () => Iv,
	NumberedList: () => Rv,
	Numerical: () => Bv,
	ObjectView: () => Hv,
	Office: () => Wv,
	Offline: () => Kv,
	OilField: () => Jv,
	OneColumn: () => Xv,
	OneToMany: () => Qv,
	OneToOne: () => ey,
	OpenApplication: () => ny,
	Outdated: () => iy,
	OuterJoin: () => oy,
	Output: () => cy,
	Package: () => uy,
	PageBreak: () => fy,
	PageLayout: () => my,
	Panel: () => gy,
	PanelStats: () => vy,
	PanelTable: () => by,
	Paperclip: () => Sy,
	Paragraph: () => wy,
	PasteVariable: () => Ey,
	Path: () => Oy,
	PathSearch: () => Ay,
	Pause: () => My,
	People: () => Py,
	Percentage: () => Iy,
	Person: () => Ry,
	Phone: () => By,
	PhoneCall: () => Hy,
	PhoneForward: () => Wy,
	PhoneSearch: () => Ky,
	PieChart: () => Jy,
	Pill: () => Xy,
	Pin: () => Qy,
	Pistol: () => eb,
	Pivot: () => nb,
	PivotTable: () => ib,
	Play: () => ob,
	Playbook: () => cb,
	Plus: () => ub,
	PolygonFilter: () => fb,
	Popout: () => mb,
	Power: () => gb,
	PredictiveAnalysis: () => vb,
	Prescription: () => bb,
	Presentation: () => Sb,
	Print: () => wb,
	Projects: () => Eb,
	Properties: () => Ob,
	Property: () => Ab,
	PublishFunction: () => Mb,
	Pulse: () => Pb,
	Rain: () => Ib,
	Random: () => Rb,
	RangeRing: () => Bb,
	Record: () => Hb,
	RectHeight: () => Wb,
	RectWidth: () => Kb,
	Rectangle: () => Jb,
	Redo: () => Xb,
	Refresh: () => Qb,
	RefreshOff: () => ex,
	Regex: () => nx,
	RegressionChart: () => ix,
	Remove: () => ox,
	RemoveColumn: () => cx,
	RemoveColumnLeft: () => ux,
	RemoveColumnRight: () => fx,
	RemoveRowBottom: () => mx,
	RemoveRowTop: () => gx,
	Repeat: () => vx,
	Reset: () => bx,
	Resolve: () => Sx,
	Rig: () => wx,
	RightJoin: () => Ex,
	Ring: () => Ox,
	Rocket: () => Ax,
	RocketSlant: () => Mx,
	RootFolder: () => Px,
	RotateCcw: () => Ix,
	RotateCw: () => Rx,
	RotateDocument: () => Bx,
	RotatePage: () => Hx,
	Route: () => Wx,
	RunHistory: () => Kx,
	Satellite: () => Jx,
	Saved: () => Xx,
	ScatterPlot: () => Qx,
	Search: () => eS,
	SearchAround: () => nS,
	SearchTemplate: () => iS,
	SearchText: () => oS,
	SegmentedControl: () => cS,
	Select: () => uS,
	Selection: () => fS,
	SelectionBox: () => mS,
	SelectionBoxAdd: () => gS,
	SelectionBoxEdit: () => vS,
	SelectionBoxRemove: () => bS,
	SendBackward: () => SS,
	SendMessage: () => wS,
	SendTo: () => ES,
	SendToGraph: () => OS,
	SendToMap: () => AS,
	Sensor: () => MS,
	SeriesAdd: () => PS,
	SeriesConfiguration: () => IS,
	SeriesDerived: () => RS,
	SeriesFiltered: () => BS,
	SeriesSearch: () => HS,
	Server: () => WS,
	ServerInstall: () => KS,
	Settings: () => JS,
	Shapes: () => XS,
	Share: () => QS,
	SharedFilter: () => eC,
	Shield: () => nC,
	Ship: () => iC,
	Shop: () => oC,
	ShoppingCart: () => cC,
	ShortenText: () => uC,
	SignalSearch: () => fC,
	SimCard: () => mC,
	Slash: () => gC,
	SmallCross: () => vC,
	SmallInfoSign: () => bC,
	SmallMinus: () => SC,
	SmallPlus: () => wC,
	SmallSquare: () => EC,
	SmallTick: () => OC,
	Snowflake: () => AC,
	SoccerBall: () => MC,
	SocialMedia: () => PC,
	Sort: () => IC,
	SortAlphabetical: () => RC,
	SortAlphabeticalDesc: () => BC,
	SortAsc: () => HC,
	SortDesc: () => WC,
	SortNumerical: () => KC,
	SortNumericalDesc: () => JC,
	SpellCheck: () => XC,
	Spin: () => QC,
	SplitColumns: () => ew,
	SportsStadium: () => nw,
	Square: () => iw,
	StackedChart: () => ow,
	StadiumGeometry: () => cw,
	Star: () => uw,
	StarEmpty: () => fw,
	StepBackward: () => mw,
	StepChart: () => gw,
	StepForward: () => vw,
	Stop: () => bw,
	Stopwatch: () => Sw,
	Strikethrough: () => ww,
	Style: () => Ew,
	Subscript: () => Ow,
	SubtractRightJoin: () => Aw,
	Superscript: () => Mw,
	SwapHorizontal: () => Pw,
	SwapVertical: () => Iw,
	Sweep: () => Rw,
	Switch: () => Bw,
	SymbolCircle: () => Hw,
	SymbolCross: () => Ww,
	SymbolDiamond: () => Kw,
	SymbolRectangle: () => Jw,
	SymbolSquare: () => Xw,
	SymbolTriangleDown: () => Qw,
	SymbolTriangleUp: () => eT,
	Syringe: () => nT,
	TableSync: () => iT,
	Tag: () => oT,
	TagAdd: () => cT,
	TagPromote: () => uT,
	TagRefresh: () => fT,
	TagUndo: () => mT,
	Tags: () => gT,
	TakeAction: () => vT,
	Tank: () => bT,
	Target: () => ST,
	Taxi: () => wT,
	Team: () => ET,
	Temperature: () => OT,
	TextHighlight: () => AT,
	Th: () => MT,
	ThAdd: () => PT,
	ThDerived: () => IT,
	ThDisconnect: () => RT,
	ThFiltered: () => BT,
	ThList: () => HT,
	ThListAdd: () => WT,
	ThVirtual: () => KT,
	ThVirtualAdd: () => JT,
	ThirdParty: () => XT,
	ThumbsDown: () => QT,
	ThumbsUp: () => eE,
	Tick: () => nE,
	TickCircle: () => iE,
	Time: () => oE,
	TimelineAreaChart: () => cE,
	TimelineBarChart: () => uE,
	TimelineEvents: () => fE,
	TimelineLineChart: () => mE,
	Tint: () => gE,
	Torch: () => vE,
	Tractor: () => bE,
	Train: () => SE,
	Translate: () => wE,
	Trash: () => EE,
	Tree: () => OE,
	TrendingDown: () => AE,
	TrendingUp: () => ME,
	Trophy: () => PE,
	Truck: () => IE,
	TwoColumns: () => RE,
	Unarchive: () => BE,
	Underline: () => HE,
	Undo: () => WE,
	UngroupObjects: () => KE,
	UnknownVehicle: () => JE,
	Unlink: () => XE,
	Unlock: () => QE,
	Unpin: () => eD,
	Unresolve: () => nD,
	Updated: () => iD,
	Upload: () => oD,
	User: () => cD,
	Variable: () => uD,
	VariableLayer: () => fD,
	Vector: () => mD,
	VerticalBarChartAsc: () => gD,
	VerticalBarChartDesc: () => vD,
	VerticalDistribution: () => bD,
	VerticalInbetween: () => SD,
	Video: () => wD,
	Virus: () => ED,
	VolumeDown: () => OD,
	VolumeOff: () => AD,
	VolumeUp: () => MD,
	Walk: () => PD,
	WarningSign: () => ID,
	WaterfallChart: () => RD,
	Waves: () => BD,
	Widget: () => HD,
	WidgetButton: () => WD,
	WidgetFooter: () => KD,
	WidgetHeader: () => JD,
	Wind: () => XD,
	Won: () => QD,
	WrapLines: () => eO,
	Wrench: () => nO,
	WrenchRedo: () => iO,
	WrenchSnooze: () => oO,
	WrenchTime: () => cO,
	Yen: () => uO,
	ZoomIn: () => fO,
	ZoomOut: () => mO,
	ZoomToFit: () => gO
}), yO = o((() => {
	kn(), jn(), Nn(), Fn(), Ln(), zn(), Vn(), Un(), Gn(), qn(), Yn(), Zn(), $n(), tr(), rr(), ar(), sr(), lr(), dr(), pr(), hr(), _r(), yr(), xr(), Cr(), Tr(), Dr(), kr(), jr(), Nr(), Fr(), Lr(), zr(), Vr(), Ur(), Gr(), qr(), Yr(), Zr(), $r(), ti(), ri(), ai(), si(), li(), di(), pi(), hi(), _i(), vi(), bi(), Si(), wi(), Ei(), Oi(), Ai(), Mi(), Pi(), Ii(), Ri(), Bi(), Hi(), Wi(), Ki(), Ji(), Xi(), Qi(), ea(), na(), M(), N(), aa(), sa(), la(), da(), pa(), ha(), _a(), ya(), xa(), Ca(), Ta(), Da(), ka(), ja(), Na(), Pa(), Ia(), Ra(), Ba(), Ha(), Wa(), Ka(), Ja(), Xa(), Qa(), eo(), no(), io(), oo(), co(), uo(), po(), ho(), _o(), yo(), xo(), Co(), To(), Do(), F(), Ao(), Mo(), Po(), L(), Fo(), Lo(), z(), Bo(), Ho(), Wo(), Ko(), Jo(), Xo(), Qo(), es(), ns(), is(), os(), cs(), us(), fs(), ms(), gs(), vs(), bs(), Ss(), ws(), Es(), Os(), As(), Ms(), Ps(), Is(), Rs(), Bs(), Hs(), Ws(), Ks(), Js(), Xs(), Qs(), ec(), nc(), ic(), oc(), cc(), uc(), fc(), mc(), gc(), _c(), yc(), bc(), xc(), Cc(), Tc(), Dc(), kc(), jc(), U(), Pc(), Ic(), Rc(), Bc(), Hc(), Wc(), Kc(), Jc(), G(), q(), Xc(), Zc(), $c(), tl(), rl(), al(), sl(), ll(), dl(), pl(), hl(), _l(), yl(), xl(), Cl(), Tl(), Dl(), kl(), jl(), Nl(), Fl(), Ll(), zl(), Vl(), Hl(), Wl(), Kl(), Jl(), Xl(), Ql(), eu(), nu(), iu(), ou(), cu(), uu(), fu(), mu(), gu(), vu(), bu(), Su(), wu(), Eu(), Ou(), Au(), Mu(), Pu(), Iu(), Ru(), Bu(), Hu(), Wu(), Ku(), Ju(), Xu(), Qu(), ed(), nd(), id(), od(), cd(), ud(), fd(), md(), gd(), vd(), bd(), Sd(), wd(), Ed(), Od(), Ad(), Md(), Pd(), Id(), Rd(), Bd(), Hd(), Wd(), Kd(), Jd(), Xd(), Qd(), ef(), nf(), af(), sf(), lf(), df(), pf(), hf(), _f(), yf(), xf(), Cf(), Tf(), Df(), kf(), jf(), Nf(), Ff(), Lf(), zf(), Vf(), Uf(), Gf(), qf(), Yf(), Zf(), $f(), tp(), rp(), ap(), sp(), lp(), dp(), pp(), hp(), _p(), yp(), xp(), Cp(), Tp(), Dp(), kp(), jp(), Np(), Fp(), Lp(), zp(), Vp(), Up(), Gp(), qp(), Yp(), Zp(), $p(), tm(), rm(), am(), sm(), lm(), dm(), pm(), hm(), _m(), ym(), xm(), Cm(), Tm(), Dm(), km(), jm(), Nm(), Fm(), Lm(), zm(), Vm(), Um(), Gm(), qm(), Ym(), Zm(), $m(), th(), rh(), ah(), sh(), lh(), dh(), ph(), hh(), _h(), yh(), xh(), Ch(), Th(), Dh(), kh(), jh(), Nh(), Fh(), Lh(), zh(), Vh(), Uh(), Gh(), qh(), Yh(), Zh(), $h(), tg(), rg(), ag(), sg(), lg(), dg(), pg(), hg(), _g(), yg(), xg(), Cg(), Tg(), Dg(), kg(), jg(), Ng(), Fg(), Lg(), zg(), Vg(), Ug(), Gg(), qg(), Yg(), Zg(), $g(), t_(), r_(), a_(), s_(), l_(), d_(), p_(), h_(), __(), y_(), x_(), C_(), T_(), D_(), k_(), j_(), N_(), F_(), L_(), z_(), V_(), U_(), G_(), q_(), Y_(), Z_(), $_(), tv(), rv(), av(), sv(), lv(), dv(), pv(), hv(), _v(), yv(), xv(), Cv(), Tv(), Dv(), kv(), jv(), Nv(), Fv(), Lv(), zv(), Vv(), Uv(), Gv(), qv(), Yv(), Zv(), $v(), ty(), ry(), ay(), sy(), ly(), dy(), py(), hy(), _y(), yy(), xy(), Cy(), Ty(), Dy(), ky(), jy(), Ny(), Fy(), Ly(), zy(), Vy(), Uy(), Gy(), qy(), Yy(), Zy(), $y(), tb(), rb(), ab(), sb(), lb(), db(), pb(), hb(), _b(), yb(), xb(), Cb(), Tb(), Db(), kb(), jb(), Nb(), Fb(), Lb(), zb(), Vb(), Ub(), Gb(), qb(), Yb(), Zb(), $b(), tx(), rx(), ax(), sx(), lx(), dx(), px(), hx(), _x(), yx(), xx(), Cx(), Tx(), Dx(), kx(), jx(), Nx(), Fx(), Lx(), zx(), Vx(), Ux(), Gx(), qx(), Yx(), Zx(), $x(), tS(), rS(), aS(), sS(), lS(), dS(), pS(), hS(), _S(), yS(), xS(), CS(), TS(), DS(), kS(), jS(), NS(), FS(), LS(), zS(), VS(), US(), GS(), qS(), YS(), ZS(), $S(), tC(), rC(), aC(), sC(), lC(), dC(), pC(), hC(), _C(), yC(), xC(), CC(), TC(), DC(), kC(), jC(), NC(), FC(), LC(), zC(), VC(), UC(), GC(), qC(), YC(), ZC(), $C(), tw(), rw(), aw(), sw(), lw(), dw(), pw(), hw(), _w(), yw(), xw(), Cw(), Tw(), Dw(), kw(), jw(), Nw(), Fw(), Lw(), zw(), Vw(), Uw(), Gw(), qw(), Yw(), Zw(), $w(), tT(), rT(), aT(), sT(), lT(), dT(), pT(), hT(), _T(), yT(), xT(), CT(), TT(), DT(), kT(), jT(), NT(), FT(), LT(), zT(), VT(), UT(), GT(), qT(), YT(), ZT(), $T(), tE(), rE(), aE(), sE(), lE(), dE(), pE(), hE(), _E(), yE(), xE(), CE(), TE(), DE(), kE(), jE(), NE(), FE(), LE(), zE(), VE(), UE(), GE(), qE(), YE(), ZE(), $E(), tD(), rD(), aD(), sD(), lD(), dD(), pD(), hD(), _D(), yD(), xD(), CD(), TD(), DD(), kD(), jD(), ND(), FD(), LD(), zD(), VD(), UD(), GD(), qD(), YD(), ZD(), $D(), tO(), rO(), aO(), sO(), lO(), dO(), pO(), hO(), _O();
})), bO, xO = o((() => {
	bO = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m5-9h-4V5c0-.55-.45-1-1-1s-1 .45-1 1v4H5c-.55 0-1 .45-1 1s.45 1 1 1h4v4c0 .55.45 1 1 1s1-.45 1-1v-4h4c.55 0 1-.45 1-1s-.45-1-1-1"];
})), SO, CO = o((() => {
	SO = ["M15 1a1 1 0 0 1 2 0v2h2a1 1 0 0 1 0 2h-2v2a1 1 0 0 1-2 0V5h-2a1 1 0 0 1 0-2h2zm-2 0a3 3 0 0 0-3 3c0 .77.292 1.469.769 2H2v11h16V9.231A3 3 0 0 0 19 7a3 3 0 0 0 1-.175V18c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1zm-2.5 11c.28 0 .5.22.5.5s-.22.5-.5.5h-7c-.28 0-.5-.22-.5-.5s.22-.5.5-.5zm-2-2c.28 0 .5.22.5.5s-.22.5-.5.5h-5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5zm4-2c.28 0 .5.22.5.5s-.22.5-.5.5h-9c-.28 0-.5-.22-.5-.5s.22-.5.5-.5z"];
})), wO, TO = o((() => {
	wO = ["M2 3v8h2v2H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-3v-2h2V3zm9 11h2c.55 0 1 .45 1 1s-.45 1-1 1h-2v2c0 .55-.45 1-1 1s-1-.45-1-1v-2H7c-.55 0-1-.45-1-1s.45-1 1-1h2v-2c0-.55.45-1 1-1s1 .45 1 1z"];
})), EO, DO = o((() => {
	EO = ["M15 0a1 1 0 0 1 1 1v3h3a1 1 0 1 1 0 2h-3v3a1 1 0 1 1-2 0V6h-3a1 1 0 1 1 0-2h3V1a1 1 0 0 1 1-1M1 4a1 1 0 0 0-1 1v4a1 1 0 0 0 2 0V6h3a1 1 0 0 0 0-2zM0 19a1 1 0 0 0 1 1h4a1 1 0 1 0 0-2H2v-3a1 1 0 1 0-2 0zm15 1h-4a1 1 0 1 1 0-2h3v-3a1 1 0 1 1 2 0v4a1 1 0 0 1-1 1m-7-5a3 3 0 1 0 0-6 3 3 0 0 0 0 6"];
})), OO, kO = o((() => {
	OO = ["M4 11h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1H8V7c0-.55-.45-1-1-1s-1 .45-1 1v2H4c-.55 0-1 .45-1 1s.45 1 1 1M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-7 18H2V2h10zm6 0h-5V2h5z"];
})), AO, jO = o((() => {
	AO = ["M10 11h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1h-2V7c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1m9-11H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M7 18H2V2h5zm11 0H8V2h10z"];
})), MO, NO = o((() => {
	MO = ["M12 0H1C.4 0 0 .5 0 1v16c0 .5.4 1 1 1h10v2h7c.5 0 1-.5 1-1V7c0 1.306-.835 2.588-2 3h-5V6.83a3 3 0 0 1-1-.594V8H2V5h8.17A3 3 0 0 1 12 1.17zm0 11h5v3h-5zm5 4v3h-5v-3zm-6 1H2v-3h9zm0-7v3H2V9zm4-8a1 1 0 0 1 2 0v2h2a1 1 0 0 1 0 2h-2v2a1 1 0 0 1-2 0V5h-2a1 1 0 0 1 0-2h2z"];
})), PO, FO = o((() => {
	PO = ["M10 0a1 1 0 0 1 0 2 8 8 0 1 0 8 8 1 1 0 0 1 2 0c0 5.523-4.477 10-10 10S0 15.523 0 10 4.477 0 10 0m0 6a4 4 0 1 1 0 8 4 4 0 0 1 0-8m6-6c.6 0 1 .4 1 1v2h2c.6 0 1 .4 1 1s-.4 1-1 1h-2v2c0 .6-.4 1-1 1s-1-.4-1-1V5h-2c-.6 0-1-.4-1-1 0-.5.4-1 1-1h2V1c0-.6.4-1 1-1"];
})), IO, LO = o((() => {
	IO = ["M18 17V9h-2V7h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1h3v2H2v8zM9 6H7c-.55 0-1-.45-1-1s.45-1 1-1h2V2c0-.55.45-1 1-1s1 .45 1 1v2h2c.55 0 1 .45 1 1s-.45 1-1 1h-2v2c0 .55-.45 1-1 1s-1-.45-1-1z"];
})), RO, zO = o((() => {
	RO = ["M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2V8h16zm0-11H2V2h16zM7 14h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1h-2v-2c0-.55-.45-1-1-1s-1 .45-1 1v2H7c-.55 0-1 .45-1 1s.45 1 1 1"];
})), BO, VO = o((() => {
	BO = ["M7 8h2v2c0 .55.45 1 1 1s1-.45 1-1V8h2c.55 0 1-.45 1-1s-.45-1-1-1h-2V4c0-.55-.45-1-1-1s-1 .45-1 1v2H7c-.55 0-1 .45-1 1s.45 1 1 1m12-8H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2v-5h16zm0-6H2V2h16z"];
})), HO, UO = o((() => {
	HO = ["M0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm11 0a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zm4.5 10a.9.9 0 0 1 .9.9v2.7h2.7a.9.9 0 0 1 0 1.8h-2.7v2.7a.9.9 0 0 1-1.8 0v-2.7h-2.7a.9.9 0 1 1 0-1.8h2.7v-2.7a.9.9 0 0 1 .9-.9"];
})), WO, GO = o((() => {
	WO = ["M13 12H1c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1m0 4H1c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1M1 6h9c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m12 2H1c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1m6-4h-2V2c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V6h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), KO, qO = o((() => {
	KO = ["M.01 10V6H20v10c0 .55-.45 1-1 1H9.995v-3.99C9.965 11.332 8.635 10 6.987 10zM19 3c.55 0 1 .45.99 1v1H0V2c0-.55.45-1 1-1h5.997c.28 0 .53.11.71.29L9.414 3zM6.987 12c.55 0 .999.45 1.009 1.01v5c0 .55-.45 1-1 1s-.999-.45-.999-1v-2.59l-4.288 4.29a1.003 1.003 0 0 1-1.42-1.42L4.579 14h-2.59c-.55 0-1-.45-1-1s.45-1 1-1z"];
})), JO, YO = o((() => {
	JO = ["M2.296 12.163a4.5 4.5 0 0 0-1.792.98A10 10 0 0 1 0 10C0 4.477 4.477 0 10 0a10 10 0 0 1 3.143.504 4.5 4.5 0 0 0-.98 1.792 8 8 0 0 0-9.867 9.867M18 10c0-.75-.103-1.475-.296-2.163a4.5 4.5 0 0 0 1.792-.98c.327.99.504 2.046.504 3.143 0 5.523-4.477 10-10 10a10 10 0 0 1-3.142-.504 4.5 4.5 0 0 0 .98-1.792A8 8 0 0 0 18 10m1-6.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0m-13 13a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0M10 4a1 1 0 0 0-1 1v3a1 1 0 0 0 2 0V5a1 1 0 0 0-1-1m1 6a1 1 0 0 1 1-1h3a1 1 0 0 1 0 2h-3a1 1 0 0 1-1-1m-7 0a1 1 0 0 1 1-1h3a1 1 0 0 1 0 2H5a1 1 0 0 1-1-1m5 2a1 1 0 0 1 2 0v3a1 1 0 0 1-2 0z"];
})), XO, ZO = o((() => {
	XO = ["M20 2c0-1.1-.9-2-2-2-.55 0-1.05.22-1.41.59l-4.84 4.84L2 1 1 3l7.53 5.64L4.17 13H1l-1 1 4 2 2 4 1-1v-3.17l4.36-4.36L17 19l2-1-4.43-9.74 4.84-4.84c.37-.37.59-.87.59-1.42"];
})), QO, $O = o((() => {
	QO = ["M5 5c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1zM1 3h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m12 12c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1zm4 2H3c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m2-8H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), ek, tk = o((() => {
	ek = ["M1 3h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m18 14H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0-12H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0 4H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0 4H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), nk, rk = o((() => {
	nk = ["M1 7h10c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m0-4h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m14 14H1c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1m4-8H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M1 15h6c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), ik, ak = o((() => {
	ik = ["M19 17H5c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1M1 3h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m18 10h-6c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1m0-4H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0-4H9c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1"];
})), ok, sk = o((() => {
	ok = ["M12 16h4c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1m7 2H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M4 16h4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1"];
})), ck, lk = o((() => {
	ck = ["M19 9h-2V7c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v2H9V3c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v6H1c-.55 0-1 .45-1 1s.45 1 1 1h2v6c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-6h2v2c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), uk, dk = o((() => {
	uk = ["M1 0C.45 0 0 .45 0 1v18c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m11 11H5c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1m7-8H5c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), fk, pk = o((() => {
	fk = ["M19 0c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m-4 11H8c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1m0-8H1c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), mk, hk = o((() => {
	mk = ["M8 4H4c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m11-4H1C.45 0 0 .45 0 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m-3 4h-4c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1"];
})), gk, _k = o((() => {
	gk = ["M17 3h-6V1c0-.55-.45-1-1-1S9 .45 9 1v2H3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h6v2H7c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1h-2V9h6c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), vk, yk = o((() => {
	vk = ["M6 6v-.172C6 4.018 5.28 2.281 4 1a6.83 6.83 0 0 0-2 4.828V6zm0 12v1H2v-1zm0-1V7H2v10zm2 2v-1h4v1zm4-13.172V6H8v-.172c0-1.81.72-3.547 2-4.828 1.28 1.28 2 3.017 2 4.828M12 7v10H8V7zm2 11v1h4v-1zm4-12v-.172c0-1.81-.72-3.547-2-4.828a6.83 6.83 0 0 0-2 4.828V6zm0 11V7h-4v10z"];
})), bk, xk = o((() => {
	bk = ["M11 5.83a3.001 3.001 0 1 0-2 0V7H6v2h3v8.917a6 6 0 0 1-4.985-5.488l.278.278a1 1 0 0 0 1.414-1.414l-2-2a1 1 0 0 0-1.414 0l-2 2a1 1 0 1 0 1.414 1.414l.303-.303a8 8 0 0 0 15.98 0l.303.303a1 1 0 0 0 1.414-1.414l-2-2a1 1 0 0 0-1.414 0l-2 2a1 1 0 0 0 1.414 1.414l.278-.278A6 6 0 0 1 11 17.917V9h3V7h-3zM11 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0"];
})), Sk, Ck = o((() => {
	Sk = ["m9.41 13.41 7.65-7.65-2.83-2.83-7.65 7.65zm10-10c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2-.55 0-1.05.22-1.41.59l-1.65 1.65 2.83 2.83zM18 18H2V2h8.93l2-2H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V7.07l-2 2zM4 16l4.41-1.59-2.81-2.79z"];
})), wk, Tk = o((() => {
	wk = ["M8 6H2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h2v5a1 1 0 1 0 2 0v-5h2l5.293 5.293c.63.63 1.707.184 1.707-.707V1.414c0-.89-1.077-1.337-1.707-.707zm8.537 7.752C18.068 12.946 19 11.538 19 10c0-1.527-.94-2.933-2.461-3.747-.25-.134-.539.058-.539.342v6.814c0 .283.286.475.537.343"];
})), Ek, Dk = o((() => {
	Ek = ["M2.01 10.758a8 8 0 0 0 1.01 3.204l.02.035q.05.087.084.178c.163.44.054.951-.33 1.239-.435.328-1.059.242-1.342-.224a10 10 0 0 1-.221-.383 10 10 0 1 1 17.48.106c-.269.474-.89.58-1.335.267-.392-.275-.518-.783-.37-1.228a1 1 0 0 1 .078-.18l.019-.036A8.026 8.026 0 1 0 2.01 10.758m4.272.772a1.5 1.5 0 0 1 .091.32c.07.425-.052.87-.402 1.128-.44.325-1.068.235-1.316-.252a6 6 0 1 1 10.734-.09c-.24.492-.867.593-1.312.275-.354-.253-.483-.695-.42-1.122a1.5 1.5 0 0 1 .085-.321 4.021 4.021 0 0 0-5.87-4.878 4.02 4.02 0 0 0-1.59 4.94m4.712 2.583A1 1 0 0 0 11 14v-4a1 1 0 1 0-2 0v4q0 .057.006.113l-3.753 4.223a1 1 0 0 0 1.494 1.328L10 16.005l3.252 3.66a1 1 0 1 0 1.495-1.33z"];
})), Ok, kk = o((() => {
	Ok = ["M19 0a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zM8 6a1 1 0 0 0-1.993-.117L6 6v8a1 1 0 0 0 1.993.117L8 14v-3h4v3a1 1 0 0 0 1.993.117L14 14V6a1 1 0 0 0-1.993-.117L12 6v3H8z"];
})), Ak, jk = o((() => {
	Ak = ["M3.5 9h9c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-9c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-5c-.28 0-.5.22-.5.5s.22.5.5.5M19 1H1c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1m-1 16H2V6h16zM3.5 13h7c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-7c-.28 0-.5.22-.5.5s.22.5.5.5"];
})), Mk, Nk = o((() => {
	Mk = ["M15 5H1c-.55 0-1 .45-1 1v13c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-1 13H2V8h12zM3.5 10h7c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-7c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h3c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-3c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-5c-.28 0-.5.22-.5.5s.22.5.5.5M19 0H5c-.55 0-1 .45-1 1v3h2V3h12v10h-1v2h2c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), Pk, Fk = o((() => {
	Pk = ["M16.434 0a1 1 0 0 1 .857.486L20 5v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V5L2.709.486A1 1 0 0 1 3.566 0zM10 8c-.55 0-1 .45-1 1v4.58l-1.29-1.29-.081-.073A1 1 0 0 0 7 11.99a1.003 1.003 0 0 0-.71 1.71l3 3 .096.084c.168.13.38.206.614.206.28 0 .53-.11.71-.29l3-3 .084-.096a1.003 1.003 0 0 0-1.504-1.324L11 13.58V9l-.007-.116A1.004 1.004 0 0 0 10 8m6-6H4L2 5.002h16z"];
})), Ik, Lk = o((() => {
	Ik = ["M5 4.664C5 2.09 7.241 0 10 0s4.99 2.091 5 4.664C15 7.245 10 14 10 14S5 7.245 5 4.664M8 5a2 2 0 1 0 4.001-.001A2 2 0 0 0 8 5M.504 12.132l4.302-2.458c.322.576.662 1.145.995 1.681l.025.04-3.294 1.881L6.468 18h7.064l3.936-4.724-3.293-1.882.024-.039c.333-.536.673-1.105.995-1.681l4.302 2.458a1 1 0 0 1 .272 1.508l-5 6A1 1 0 0 1 14 20H6a1 1 0 0 1-.768-.36l-5-6a1 1 0 0 1 .272-1.508"];
})), Rk, zk = o((() => {
	Rk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm5 9a1 1 0 1 1 0 2 1 1 0 0 1 0-2M6 9a1 1 0 1 1 0 2 1 1 0 0 1 0-2m8 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"];
})), Bk, Vk = o((() => {
	Bk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm10 7a1 1 0 0 1 .993.883L16 8v4a1 1 0 0 1-.883.993L15 13H5a1 1 0 0 1-.993-.883L4 12V8a1 1 0 0 1 .883-.993L5 7zm0 1h-5v4h5z"];
})), Hk, Uk = o((() => {
	Hk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm2.5 5a.5.5 0 0 1 .5.5V6h4v-.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5V6h1a1 1 0 0 1 .993.883L16 7v7a1 1 0 0 1-.883.993L15 15H5a1 1 0 0 1-.993-.883L4 14V7a1 1 0 0 1 .883-.993L5 6h1v-.5a.5.5 0 0 1 .5-.5zM15 9H5v5h10z"];
})), Wk, Gk = o((() => {
	Wk = ["M19.992 1.104A1.25 1.25 0 0 0 18.75 0H15c-.47 0-1 .359-1 1s.5 1 1.023 1h3L18 18h-3c-.5 0-1 .359-1 1 0 .69.5 1 1 1h3.75l.146-.008A1.25 1.25 0 0 0 20 18.75V1.25zM6 1c0-.69-.5-1-1-1H1.25l-.146.008A1.25 1.25 0 0 0 0 1.25v17.5l.008.146A1.25 1.25 0 0 0 1.25 20H5c.5 0 1-.359 1-1s-.5-1-1-1H2V2h3c.5 0 1-.359 1-1m-.566 6.325q-.333.058-.684.058v.88h1.68v4.825h1.221V6.25h-.908q-.06.312-.254.528-.186.215-.46.351a2 2 0 0 1-.595.196m8.893-.739q-.441-.329-1.147-.329-.705 0-1.157.33a2.24 2.24 0 0 0-.695.827 3.8 3.8 0 0 0-.339 1.1q-.085.602-.085 1.166t.085 1.166q.095.6.339 1.11.253.498.695.827.452.32 1.157.32t1.147-.32q.451-.33.696-.828.254-.507.338-1.11a7.6 7.6 0 0 0 .094-1.165 7.6 7.6 0 0 0-.094-1.166 3.5 3.5 0 0 0-.338-1.1 2.1 2.1 0 0 0-.696-.828m-.564 5.426a.88.88 0 0 1-.583.197.9.9 0 0 1-.592-.197 1.5 1.5 0 0 1-.367-.546 3.5 3.5 0 0 1-.188-.808 8 8 0 0 1-.057-.978q0-.518.057-.969.056-.46.188-.808.14-.348.367-.546a.86.86 0 0 1 .592-.206.85.85 0 0 1 .583.206q.235.198.367.546.141.348.197.808.056.452.056.969t-.056.978a3.2 3.2 0 0 1-.197.808q-.132.339-.367.546m-4.91-.205h1.358v1.319H8.853z"];
})), Kk, qk = o((() => {
	Kk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm8.995 6.09q.48 0 .85.14t.625.39.39.595.135.755q0 .43-.19.795a1.64 1.64 0 0 1-.57.615v.02l.101.05q.102.058.209.155.16.145.29.355a2.1 2.1 0 0 1 .3 1.09q0 .47-.16.85a1.9 1.9 0 0 1-1.12 1.065 2.4 2.4 0 0 1-.85.145q-.8 0-1.37-.38a1.7 1.7 0 0 1-.73-1.08q-.02-.1.08-.13l.87-.2.041-.003q.057.006.079.073.11.3.36.51t.67.21q.48 0 .74-.285t.26-.725q0-.52-.3-.815t-.81-.295h-.29l-.044-.006q-.056-.02-.056-.094V9.1l.006-.044q.02-.056.094-.056h.27l.145-.008a.93.93 0 0 0 .575-.262q.27-.27.27-.72 0-.41-.24-.665t-.67-.255q-.38 0-.6.19t-.31.51q-.03.09-.12.07l-.85-.2-.042-.015q-.053-.03-.038-.105a1.68 1.68 0 0 1 .645-1.035q.255-.195.6-.305t.755-.11m-7.99.11.044.006q.056.02.056.094v6.6l-.006.044q-.02.056-.094.056h-.92l-.044-.006q-.056-.02-.056-.094V7.54h-.02l-1.04.73-.04.02q-.07.024-.07-.08V7.19l.008-.051a.2.2 0 0 1 .062-.089l1.09-.79.051-.033a.3.3 0 0 1 .129-.027zm3.34-.11q.48 0 .85.15t.625.405.39.6.135.745q0 .46-.17.845a3.2 3.2 0 0 1-.47.745l-1.98 2.4V12h2.52l.044.006q.056.02.056.094v.8l-.006.044q-.02.056-.094.056h-3.82l-.044-.006q-.056-.02-.056-.094v-.75l.006-.05a.2.2 0 0 1 .044-.08l2.4-2.99.124-.167q.116-.166.196-.333.12-.25.12-.54a.92.92 0 0 0-.235-.64q-.235-.26-.665-.26-.41 0-.64.23t-.28.62q-.02.1-.11.08l-.88-.18-.043-.015q-.052-.03-.037-.105.03-.3.17-.59a1.8 1.8 0 0 1 .39-.525q.25-.236.615-.375a2.4 2.4 0 0 1 .845-.14"];
})), Jk, Yk = o((() => {
	Jk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm3.103 4A1.563 1.563 0 0 0 6.54 5.563v2.473c0 .38-.194.734-.514.94l-.718.46a.67.67 0 0 0 0 1.127l.718.46c.32.206.514.56.514.94v2.474c0 .863.7 1.563 1.563 1.563h.344a.67.67 0 0 0 0-1.34h-.345a.223.223 0 0 1-.224-.223v-2.473a2.46 2.46 0 0 0-.98-1.965 2.46 2.46 0 0 0 .98-1.963V5.563a.223.223 0 0 1 .224-.224h.344a.67.67 0 0 0 0-1.339zm3.607 0c.864 0 1.563.7 1.563 1.563v2.473c0 .38.195.734.515.94l.717.46a.67.67 0 0 1 0 1.127l-.718.46a1.12 1.12 0 0 0-.513.94v2.474A1.563 1.563 0 0 1 11.711 16h-.344a.67.67 0 0 1 0-1.34h.344a.223.223 0 0 0 .224-.223v-2.473c0-.777.366-1.502.98-1.965a2.46 2.46 0 0 1-.98-1.963V5.563a.224.224 0 0 0-.224-.224h-.344a.67.67 0 0 1 0-1.339z"];
})), Xk, Zk = o((() => {
	Xk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm2.012 6q.965 0 1.68.797.715.796.715 2.145a4.47 4.47 0 0 1-.965 2.814Q7.476 13 5.395 13.767v-.581l.26-.104a3.87 3.87 0 0 0 1.624-1.285q.686-.949.686-1.971 0-.221-.07-.326-.035-.07-.093-.07t-.186.093q-.372.268-.93.268-.675 0-1.18-.541A1.82 1.82 0 0 1 5 7.965q0-.79.581-1.378A1.93 1.93 0 0 1 7.011 6m5.593 0q.965 0 1.68.797.715.796.715 2.145a4.47 4.47 0 0 1-.965 2.814q-.966 1.245-3.047 2.011v-.581l.26-.104a3.87 3.87 0 0 0 1.624-1.285q.686-.949.686-1.971 0-.221-.07-.326-.034-.07-.093-.07-.057 0-.186.093-.372.268-.93.268-.675 0-1.18-.541a1.82 1.82 0 0 1-.506-1.285q0-.79.581-1.378A1.93 1.93 0 0 1 12.604 6"];
})), Qk, $k = o((() => {
	Qk = ["M19 0a1 1 0 0 1 .993.883L20 1v18a1 1 0 0 1-.883.993L19 20h-4a1 1 0 0 1-.117-1.993L15 18h3V2h-3a1 1 0 0 1-.993-.883L14 1a1 1 0 0 1 .883-.993L15 0zM5 0a1 1 0 0 1 .117 1.993L5 2H2v16h3a1 1 0 0 1 .993.883L6 19a1 1 0 0 1-.883.993L5 20H1a1 1 0 0 1-.993-.883L0 19V1A1 1 0 0 1 .883.007L1 0zm5 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12m0 1a5 5 0 1 0 0 10 5 5 0 0 0 0-10m2.854 2.146a.5.5 0 0 1 .057.638l-.057.07-2.5 2.5a.5.5 0 0 1-.638.057l-.07-.057-1.5-1.5a.5.5 0 0 1 .638-.765l.07.057L10 9.293l2.146-2.147a.5.5 0 0 1 .708 0"];
})), eA, tA = o((() => {
	eA = ["M18 3a1.003 1.003 0 0 0-1.71-.71L4 14.59V7c0-.55-.45-1-1-1s-1 .45-1 1v10c0 .55.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1H5.41l12.3-12.29c.18-.18.29-.43.29-.71"];
})), nA, rA = o((() => {
	nA = ["M17 6c-.55 0-1 .45-1 1v7.59L3.71 2.29a1.003 1.003 0 0 0-1.42 1.42L14.59 16H7c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1"];
})), iA, aA = o((() => {
	iA = ["M16 11c-.3 0-.5.1-.7.3L11 15.6V2c0-.5-.4-1-1-1s-1 .5-1 1v13.6l-4.3-4.3c-.2-.2-.4-.3-.7-.3-.5 0-1 .4-1 1 0 .3.1.5.3.7l6 6c.2.2.4.3.7.3s.5-.1.7-.3l6-6c.2-.2.3-.4.3-.7 0-.6-.5-1-1-1"];
})), oA, sA = o((() => {
	oA = ["M18 9H4.41L8.7 4.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-6 6c-.18.18-.29.43-.29.71s.11.53.29.71l6 6a1.003 1.003 0 0 0 1.42-1.42L4.41 11H18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), cA, lA = o((() => {
	cA = ["m18.71 9.29-6-6a1.003 1.003 0 0 0-1.42 1.42L15.59 9H2c-.55 0-1 .45-1 1s.45 1 1 1h13.59l-4.29 4.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l6-6c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), uA, dA = o((() => {
	uA = ["M17.71 16.29 5.41 4H13c.55 0 1-.45 1-1s-.45-1-1-1H3c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1s1-.45 1-1V5.41L16.29 17.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), fA, pA = o((() => {
	fA = ["M17 2H7c-.55 0-1 .45-1 1s.45 1 1 1h7.59L2.29 16.29a1.003 1.003 0 0 0 1.42 1.42L16 5.41V13c0 .55.45 1 1 1s1-.45 1-1V3c0-.55-.45-1-1-1"];
})), mA, hA = o((() => {
	mA = ["m16.7 7.3-6-6c-.2-.2-.4-.3-.7-.3s-.5.1-.7.3l-6 6c-.2.2-.3.4-.3.7 0 .6.5 1 1 1 .3 0 .5-.1.7-.3L9 4.4V18c0 .5.4 1 1 1s1-.5 1-1V4.4l4.3 4.3c.2.2.4.3.7.3.5 0 1-.4 1-1 0-.3-.1-.5-.3-.7"];
})), gA, _A = o((() => {
	gA = ["M4.246.183a.625.625 0 0 1 .883 0l3.978 3.978a.625.625 0 0 1-.884.883L5.308 2.13v.004c-.01 2.244-.018 3.935.23 5.393.29 1.708.933 3.07 2.403 4.53 1.478 1.471 2.77 2.11 4.432 2.4 1.437.252 3.134.245 5.488.235h.009l-2.914-2.914a.625.625 0 1 1 .883-.884l3.978 3.978a.625.625 0 0 1 0 .883l-3.978 3.978a.625.625 0 1 1-.883-.884l2.906-2.906c-2.333.01-4.157.016-5.704-.255-1.931-.338-3.452-1.106-5.099-2.744C5.404 11.296 4.64 9.7 4.306 7.736c-.266-1.563-.26-3.374-.248-5.597L1.152 5.044a.625.625 0 1 1-.884-.883z"];
})), vA, yA = o((() => {
	vA = ["m19.7 9.3-5-5c-.2-.2-.4-.3-.7-.3-.6 0-1 .4-1 1 0 .3.1.5.3.7L16.6 9H3.4l3.3-3.3c.2-.2.3-.4.3-.7 0-.6-.4-1-1-1-.3 0-.5.1-.7.3l-5 5c-.2.2-.3.4-.3.7s.1.5.3.7l5 5c.2.2.4.3.7.3.6 0 1-.4 1-1 0-.3-.1-.5-.3-.7L3.4 11h13.2l-3.3 3.3c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3l5-5c.2-.2.3-.4.3-.7s-.1-.5-.3-.7"];
})), bA, xA = o((() => {
	bA = ["M15 13c-.3 0-.5.1-.7.3L11 16.6V3.4l3.3 3.3c.2.2.4.3.7.3.6 0 1-.4 1-1 0-.3-.1-.5-.3-.7l-5-5c-.2-.2-.4-.3-.7-.3s-.5.1-.7.3l-5 5c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3L9 3.4v13.2l-3.3-3.3c-.2-.2-.4-.3-.7-.3-.6 0-1 .4-1 1 0 .3.1.5.3.7l5 5c.2.2.4.3.7.3s.5-.1.7-.3l5-5c.2-.2.3-.4.3-.7 0-.5-.4-1-1-1"];
})), SA, CA = o((() => {
	SA = ["m18.52 14.17.01-.02L11.89 10l6.64-4.15-.01-.02A.97.97 0 0 0 19 5c0-.55-.45-1-1-1-.2 0-.37.07-.52.17l-.01-.02L11 8.2V1c0-.55-.45-1-1-1S9 .45 9 1v7.2L2.53 4.15l-.01.02A.9.9 0 0 0 2 4c-.55 0-1 .45-1 1 0 .36.2.66.48.83l-.01.02L8.11 10l-6.64 4.15.01.02A.97.97 0 0 0 1 15c0 .55.45 1 1 1 .2 0 .37-.07.52-.17l.01.02L9 11.8V19c0 .55.45 1 1 1s1-.45 1-1v-7.2l6.47 4.04.01-.02c.15.11.32.18.52.18.55 0 1-.45 1-1 0-.36-.2-.66-.48-.83"];
})), wA, TA = o((() => {
	wA = ["M12.298 6.818a6.5 6.5 0 0 0-1.672-.207q-1.586 0-2.472 1.036-.884 1.037-.884 2.817 0 2.842 2.266 2.842 2.39 0 2.614-3.574zm6.544-2.592Q20 6.256 20 8.916q0 1.743-.556 3.189c-.374.963-.894 1.713-1.569 2.25a3.64 3.64 0 0 1-2.333.803q-.978 0-1.696-.512a2.5 2.5 0 0 1-.967-1.39h-.148q-.607.952-1.498 1.427-.893.476-2.007.475-2.019.001-3.175-1.279-1.16-1.28-1.159-3.463 0-2.514 1.537-4.08 1.532-1.566 4.122-1.567.941 0 2.086.164 1.146.165 2.037.458l-.272 5.67v.294q0 1.95 1.289 1.951.977 0 1.553-1.245.576-1.244.577-3.171-.001-2.085-.868-3.664a5.95 5.95 0 0 0-2.463-2.433q-1.597-.853-3.667-.853-2.636 0-4.588 1.072a7.2 7.2 0 0 0-2.978 3.069Q2.229 8.073 2.23 10.708q0 3.538 1.92 5.438 1.918 1.904 5.509 1.902 2.739 0 5.71-1.096v2.001Q12.769 20 9.709 20q-4.584 0-7.144-2.432Q0 15.134 0 10.781q0-3.183 1.388-5.665 1.386-2.48 3.845-3.798Q7.691.001 10.799 0q2.688 0 4.786 1.098a7.87 7.87 0 0 1 3.257 3.128"];
})), EA, DA = o((() => {
	EA = ["M10 18c-4.42 0-8-3.58-8-8 0-2.52 1.18-4.76 3-6.22V5c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1h2.06C1.61 3.82 0 6.71 0 10c0 5.52 4.48 10 10 10 .55 0 1-.45 1-1s-.45-1-1-1m0-16c1.64 0 3.15.49 4.42 1.34l1.43-1.43A9.87 9.87 0 0 0 10 0c-.55 0-1 .45-1 1s.45 1 1 1m10 8c0-1.13-.2-2.21-.54-3.22L17.84 8.4A7.96 7.96 0 0 1 15 16.22V15c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1h-2.06c2.45-1.82 4.06-4.71 4.06-8m0-7a1.003 1.003 0 0 0-1.71-.71L12 8.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l7-7c.18-.18.29-.43.29-.71"];
})), OA, kA = o((() => {
	OA = ["M2 15h2v.5a.5.5 0 0 0 1 0v-11a.5.5 0 0 0-1 0V5H2zM18 5h-2v-.5a.5.5 0 0 0-1 0v11a.5.5 0 0 0 1 0V15h2zM5 8l1.789.894A1 1 0 0 0 7.236 9h5.528a1 1 0 0 0 .447-.106L15 8v4l-1.789-.894a1 1 0 0 0-.447-.106H7.236a1 1 0 0 0-.447.106L5 12zM0 9h2v2H0zm0-1h1v4H0zm19 0h1v4h-1zm1 3h-2V9h2zM8 9a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1z"];
})), AA, jA = o((() => {
	AA = ["m18.387 19.79-.094-.083L14 15.415V18a1 1 0 0 1-2 0l.003-5.075.017-.126.03-.111.044-.111.052-.098.067-.096.08-.09a1 1 0 0 1 .112-.097l.11-.071.114-.054.105-.035.15-.03L13 12h5a1 1 0 1 1 0 2h-2.585l4.292 4.293a1 1 0 0 1-1.32 1.497M7.036 9.136l-4.45 4.45-.117.127a2 2 0 0 0 2.818 2.818l.127-.117 4.45-4.449a4 4 0 0 1-.885 3.704l-.15.16-2 2A4 4 0 0 1 1.02 12.33l.15-.16 2-2a4 4 0 0 1 3.865-1.035m6.671-3.843a1 1 0 0 1 .083 1.32l-.083.094-7 7a1 1 0 0 1-1.497-1.32l.083-.094 7-7a1 1 0 0 1 1.414 0m4.121-4.121a4 4 0 0 1 .151 5.497l-.15.16-2 2a4 4 0 0 1-3.864 1.036l4.45-4.45.116-.128a2 2 0 0 0-2.818-2.818l-.127.117-4.45 4.45a4 4 0 0 1 .885-3.705l.15-.16 2-2a4 4 0 0 1 5.657 0"];
})), MA, NA = o((() => {
	MA = ["M9.754 20a8.5 8.5 0 0 1-3.417-.693 8.9 8.9 0 0 1-2.772-1.872 8.9 8.9 0 0 1-1.872-2.772A8.5 8.5 0 0 1 1 11.246q0-.413.28-.693a.94.94 0 0 1 .693-.28q.413 0 .693.28t.28.693q0 2.845 1.981 4.827 1.98 1.982 4.827 1.982t4.826-1.982 1.982-4.827q.001-2.845-1.982-4.826-1.984-1.98-4.826-1.982h-.146l.826.827a.9.9 0 0 1 .28.68q-.012.39-.28.681a1 1 0 0 1-1.07.24.9.9 0 0 1-.316-.216L6.544 4.147a.93.93 0 0 1-.292-.68q0-.39.292-.681L9.048.28A.9.9 0 0 1 9.741 0a.994.994 0 0 1 .973.985.9.9 0 0 1-.28.681l-.826.827h.146a8.5 8.5 0 0 1 3.416.693 8.9 8.9 0 0 1 2.772 1.872 8.9 8.9 0 0 1 1.872 2.772 8.5 8.5 0 0 1 .693 3.416 8.5 8.5 0 0 1-.693 3.417 8.9 8.9 0 0 1-1.872 2.772 8.9 8.9 0 0 1-2.772 1.872A8.5 8.5 0 0 1 9.754 20M11.5 9.5v3h1v-3zM11 8h2a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1M9 9v4.25a.75.75 0 1 1-1.5 0V9.5h-.75a.75.75 0 0 1 0-1.5H8a1 1 0 0 1 1 1"];
})), PA, FA = o((() => {
	PA = ["M16.94 5.73c-.19-1.41.62-2.52 1.38-3.59L17.03.65C14.89 1.76 11.88 1.48 10 0 8.12 1.48 5.11 1.76 2.97.65L1.68 2.14c.76 1.07 1.57 2.18 1.38 3.59C2.68 8.59 0 10.94 1.4 14.08c.56 1.43 1.81 2.37 3.4 2.75 1.95.46 4.4.91 5.2 3.17.8-2.26 3.25-2.71 5.2-3.17 1.6-.38 2.84-1.32 3.4-2.75 1.4-3.14-1.28-5.49-1.66-8.35"];
})), IA, LA = o((() => {
	IA = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m5 11H5c-.55 0-1-.45-1-1s.45-1 1-1h10c.55 0 1 .45 1 1s-.45 1-1 1"];
})), RA, zA = o((() => {
	RA = ["m19.2 8.02-.78-.18C18.03 6.4 17.2 5.08 16.08 4l.5-2.28c.11-.42-.22-.78-.61-.72-1.06.12-2 .54-2.67 1.26-1.06-.42-2.34-.66-3.56-.66-3.12 0-5.79 1.5-7.4 3.72-.23-.05-.45-.11-.67-.11C.72 5.21 0 5.98 0 7c0 .72.39 1.32.95 1.62-.06.42-.12.9-.12 1.38 0 2.16.89 4.08 2.28 5.58l-.33 2.04c-.11.72.45 1.38 1.12 1.38h.72c.56 0 1-.42 1.11-1.02l.06-.48c1.17.54 2.5.9 3.95.9 1.39 0 2.78-.3 3.95-.9l.06.48c.11.6.56 1.02 1.11 1.02h.72c.67 0 1.22-.66 1.11-1.38l-.33-1.98c.78-.78 1.34-1.74 1.73-2.76l1-.24c.5-.12.89-.6.89-1.2V9.22c.11-.6-.28-1.08-.78-1.2M15 10c-.6 0-1-.7-1-1.5S14.4 7 15 7s1 .7 1 1.5-.4 1.5-1 1.5M7.55 5.83a.99.99 0 0 1-1.38-.28.99.99 0 0 1 .28-1.38c2.34-1.56 4.77-1.56 7.11 0 .46.31.58.93.28 1.39-.31.46-.93.58-1.39.28-1.67-1.12-3.23-1.12-4.9-.01"];
})), BA, VA = o((() => {
	BA = ["M6 16.98h2v-14H6zm3 0h1v-14H9zm-6 0h2v-14H3zm-3 0h2v-14H0zm16 0h2v-14h-2zm-4 0h1v-14h-1zm7-14v14h1v-14zm-5 14h1v-14h-1z"];
})), HA, UA = o((() => {
	HA = ["M8.011 5.48Q7.365 5 6.331 5 5.3 5 4.639 5.48A3.3 3.3 0 0 0 3.62 6.69a5.6 5.6 0 0 0-.496 1.607A12 12 0 0 0 3 10q0 .825.124 1.703.138.88.496 1.621.371.729 1.018 1.209.66.467 1.694.467 1.032 0 1.68-.467.66-.48 1.018-1.209a5.2 5.2 0 0 0 .496-1.62q.137-.88.137-1.704 0-.825-.137-1.703A5 5 0 0 0 9.03 6.69a3.1 3.1 0 0 0-1.019-1.21m-.826 7.927q-.345.288-.853.288-.524 0-.868-.288-.33-.303-.537-.797a5 5 0 0 1-.275-1.181A12 12 0 0 1 4.57 10q0-.755.083-1.415.083-.673.275-1.181.207-.509.537-.797.345-.302.868-.302.51 0 .853.302.345.288.537.797.207.508.29 1.181.082.66.082 1.415 0 .756-.083 1.429a4.6 4.6 0 0 1-.289 1.18q-.192.495-.537.798m5.817-6.836A6 6 0 0 1 12 6.657v1.286h2.463V15h1.79V5H14.92a1.54 1.54 0 0 1-.372.771q-.273.315-.673.515a3 3 0 0 1-.874.285"];
})), WA, GA = o((() => {
	WA = [];
})), KA, qA = o((() => {
	KA = ["M18 9h-1V4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v5H2c-.55 0-1 .45-1 1s.45 1 1 1h1v5c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-5h1c.55 0 1-.45 1-1s-.45-1-1-1M6.85 13.35a.47.47 0 0 1-.35.15.47.47 0 0 1-.35-.15c-.2-.19-.2-.51 0-.7L8.79 10 6.15 7.35c-.2-.19-.2-.51 0-.7.19-.2.51-.2.7 0l3 3c.2.19.2.51 0 .7zm7-3-3 3a.47.47 0 0 1-.35.15.47.47 0 0 1-.35-.15c-.2-.19-.2-.51 0-.7L12.79 10l-2.64-2.65c-.2-.19-.2-.51 0-.7.19-.2.51-.2.7 0l3 3c.2.19.2.51 0 .7"];
})), JA, YA = o((() => {
	JA = ["M11.55 15.92c-1.48-.65-1.28-1.05-1.33-1.59-.01-.07-.01-.15-.01-.23.51-.45.92-1.07 1.19-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.34-.07.54-.44.61-.78.06-.11.14-.35.17-.62C10.33 9.42 8.92 7.38 8.92 5c0-.3.05-.58.09-.87-.33-.08-.67-.13-.99-.13-.79 0-1.68.25-2.31.73-.61.47-1.07 1.13-1.29 1.86-.05.16-.09.33-.11.5-.12.6-.17 1.51-.17 2.14v.08c-.24.09-.45.32-.49.83-.04.39.12.73.2.87.08.35.28.72.63.78q.06.255.15.48c0 .01.01.02.01.03l.01.01c.27.72.7 1.35 1.22 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.38 1.59S.77 17.26.32 18.31C-.15 19.38.04 20 .04 20h15.95s.18-.62-.27-1.67c-.46-1.06-2.69-1.75-4.17-2.41M14.97 0c-2.78 0-5.03 2.24-5.03 5s2.25 5 5.03 5S20 7.76 20 5s-2.25-5-5.03-5m-3.03 5c0-1.66 1.35-3 3.02-3 .47 0 .9.11 1.29.3l-4.01 3.99c-.18-.4-.3-.83-.3-1.29m3.03 3c-.47 0-.9-.11-1.29-.3l4.01-3.99c.19.39.3.82.3 1.29 0 1.66-1.36 3-3.02 3"];
})), XA, ZA = o((() => {
	XA = ["M14.3 9c.4-.8.7-1.6.7-2.5C15 4 13 2 10.5 2H5c-.6 0-1 .4-1 1v13c0 .6.4 1 1 1h6.5c2.5 0 4.5-2 4.5-4.5 0-1.4-.7-2.7-1.7-3.5M7 5h3.5c.8 0 1.5.7 1.5 1.5S11.3 8 10.5 8H7zm4.5 9H7v-3h4.5c.8 0 1.5.7 1.5 1.5s-.7 1.5-1.5 1.5"];
})), QA, $A = o((() => {
	QA = ["M3 1v18c0 .55.45 1 1 1h2V0H4c-.55 0-1 .45-1 1m14-1h-2v8l-2-2-2 2V0H7v20h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), ej, tj = o((() => {
	ej = ["M6 0c-.55 0-1 .45-1 1v18c0 .55.32.68.71.29L9.3 15.7a.996.996 0 0 1 1.41 0l3.59 3.59c.38.39.7.26.7-.29V1c0-.55-.45-1-1-1z"];
})), nj, rj = o((() => {
	nj = ["m19.89 6.56-2.99-6h-.01C16.72.23 16.39 0 16 0H4c-.39 0-.72.23-.89.56H3.1l-3 6h.01C.05 6.69 0 6.84 0 7v12c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V7c0-.16-.05-.31-.11-.44M11 2h4.38l2 4H11zM4.62 2H9v4H2.62zM18 18H2V8h16zM8 12h4c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1"];
})), ij, aj = o((() => {
	ij = ["M15 2c-1.66 0-3 1.34-3 3 0 1.3.84 2.4 2 2.82V9c0 1.1-.9 2-2 2H8c-.73 0-1.41.21-2 .55V5.82C7.16 5.4 8 4.3 8 3c0-1.66-1.34-3-3-3S2 1.34 2 3c0 1.3.84 2.4 2 2.82v8.37C2.84 14.6 2 15.7 2 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.25-.77-2.3-1.85-2.75C6.45 13.52 7.16 13 8 13h4c2.21 0 4-1.79 4-4V7.82C17.16 7.4 18 6.3 18 5c0-1.66-1.34-3-3-3M5 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 16c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M15 6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m2 10h.5a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1-.5-.5v-3a.5.5 0 0 1 .5-.5h.5v-1c0-.636.243-1.15.637-1.499A2.05 2.05 0 0 1 15 13c.481 0 .98.16 1.363.501.393.35.637.863.637 1.499zm-1-1c0-.364-.132-.6-.3-.751A1.06 1.06 0 0 0 15 14c-.268 0-.52.09-.7.249-.168.15-.3.387-.3.751v1h2z"];
})), oj, sj = o((() => {
	oj = ["M15 2c-1.66 0-3 1.34-3 3 0 1.3.84 2.4 2 2.82V9c0 1.1-.9 2-2 2H8c-.73 0-1.41.21-2 .55V5.82C7.16 5.4 8 4.3 8 3c0-1.66-1.34-3-3-3S2 1.34 2 3c0 1.3.84 2.4 2 2.82v8.37C2.84 14.6 2 15.7 2 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.25-.77-2.3-1.85-2.75C6.45 13.52 7.16 13 8 13h4c2.21 0 4-1.79 4-4V7.82C17.16 7.4 18 6.3 18 5c0-1.66-1.34-3-3-3M5 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 16c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M15 6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m2.5 10a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1-.5-.5v-3a.5.5 0 0 1 .5-.5H16v-1c0-.636.244-1.15.637-1.499A2.05 2.05 0 0 1 18 13c.481 0 .98.16 1.363.501.393.35.637.863.637 1.499a.5.5 0 0 1-1 0c0-.364-.132-.6-.3-.751A1.06 1.06 0 0 0 18 14c-.268 0-.52.09-.7.249-.168.15-.3.387-.3.751v1z"];
})), cj, lj = o((() => {
	cj = ["M19 5h-4V2c0-.55-.45-1-1-1H6c-.55 0-1 .45-1 1v3H1c-.55 0-1 .45-1 1v5h4v-1h2v1h8v-1h2v1h4V6c0-.55-.45-1-1-1m-6 0H7V3h6zm3 8h-2v-1H6v1H4v-1H0v6c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-6h-4z"];
})), uj, dj = o((() => {
	uj = ["M18 18a1 1 0 0 1 0 2H2a1 1 0 0 1 0-2zM9.995 3.005c.55 0 1 .45 1 .999v9.584l1.29-1.288a1.002 1.002 0 0 1 1.42 1.419l-3 2.996a1.015 1.015 0 0 1-1.42 0l-3-2.997a1.002 1.002 0 0 1 1.42-1.419l1.29 1.29V4.013c0-.55.45-1.009 1-1.009M16 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2m-3 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2m-3 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M4 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"];
})), fj, pj = o((() => {
	fj = ["M9.293.293a1 1 0 0 1 1.414 0l4 4a1 1 0 0 1-1.414 1.414L11 3.414V9h8a1 1 0 1 1 0 2h-8v3h8a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h8v-3H1a1 1 0 1 1 0-2h8V3.414L6.707 5.707a1 1 0 0 1-1.414-1.414z"];
})), mj, hj = o((() => {
	mj = ["M9.62 5.174A3 3 0 0 0 9 7v2h4a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H9v1.377c0 .987-.187 1.867-.534 2.623H17v3H3v-3h.5c.715 0 1.334-.217 1.754-.59.388-.344.746-.944.746-2.033V12H4a1 1 0 0 1-1-1v-1a1 1 0 0 1 1-1h2V7a6 6 0 0 1 8.296-5.543C15.516 1.962 16.34 2.857 17 4l-2.402 1.5a3 3 0 0 0-4.978-.326"];
})), gj, _j = o((() => {
	gj = ["M6.006 4.272C6.124 2.136 7.866 0 10 0c2.133 0 3.877 2.136 3.994 4.272.49.438.909.956 1.234 1.532L17 5.017V3a1 1 0 1 1 2 0v2.667a1 1 0 0 1-.594.913l-2.5 1.111Q16 8.208 16 8.75V10h3a1 1 0 1 1 0 2h-3v.5c0 .604-.09 1.187-.255 1.737l2.661 1.182a1 1 0 0 1 .594.914V19a1 1 0 1 1-2 0v-2.017l-2.147-.954A6 6 0 0 1 10 18.5a6 6 0 0 1-4.853-2.471L3 16.983V19a1 1 0 1 1-2 0v-2.667a1 1 0 0 1 .594-.913l2.661-1.183A6 6 0 0 1 4 12.5V12H1a1 1 0 1 1 0-2h3V8.75q0-.542.093-1.059l-2.5-1.11A1 1 0 0 1 1 5.666V3a1 1 0 0 1 2 0v2.017l1.772.787a6 6 0 0 1 1.234-1.532M6 11v1.5a4 4 0 0 0 8 0V8.75a4 4 0 0 0-8 0z"];
})), vj, yj = o((() => {
	vj = ["M15.836 1.014a1 1 0 0 1 1.058.539l2.482 4.962.02-.004a.5.5 0 0 1 .604.49v4.5a.5.5 0 0 1-.5.5h-3.93a1.5 1.5 0 0 0-1.248.667l-1.406 2.11A.5.5 0 0 1 12.5 15H8a.5.5 0 0 1-.354-.146l-2.414-2.415A1.5 1.5 0 0 0 4.172 12H.5a.5.5 0 0 1-.5-.5v-3A.5.5 0 0 1 .5 8h.823l1.749-4.37a1 1 0 0 1 .764-.615zm.289 3.472-1.527 3.053 2.758-.591zM14.5 3.264l-2.637.439.825 2.043.252.638zm-9.78 1.63L3.477 8H4.5a.5.5 0 0 1 .354.147L7.707 11h2.525l1.497-2.245-.899-2.27-.988-2.445zM3 19a3 3 0 1 1 0-6 3 3 0 0 1 0 6m14 0a3 3 0 1 1 0-6 3 3 0 0 1 0 6"];
})), bj, xj = o((() => {
	bj = ["M19.43 16.67 9.31 7.81l1.47-1.56c.41-.44-.15-.8.15-1.6 1.08-2.76 4.19-2.99 4.19-2.99s.45-.47.87-.92C11.98-1 9.26.7 8.04 1.8L3.83 6.25l-.86.92c-.48.51-.48 1.33 0 1.84l-.87.92c-.48-.51-1.26-.51-1.74 0s-.48 1.33 0 1.84l1.74 1.84c.48.51 1.26.51 1.74 0s.48-1.33 0-1.84l.87-.92c.48.51 1.26.51 1.74 0l1.41-1.49 8.81 10.07c.76.76 2 .76 2.76 0s.76-2 0-2.76"];
})), Sj, Cj = o((() => {
	Sj = ["M19.707.293a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-1.414-1.414l9-9a1 1 0 0 1 1.414 0m-5.081.839A9.96 9.96 0 0 0 10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10a9.96 9.96 0 0 0-1.132-4.626l-1.501 1.502a8 8 0 1 1-4.243-4.243zm-3.072 3.071a6 6 0 1 0 4.243 4.243l-1.805 1.804A4 4 0 1 1 9.75 6.008z"];
})), wj, Tj = o((() => {
	wj = ["M16 0H4c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M7 18H5v-2h2zm0-4H5v-2h2zm0-4H5V8h2zm4 8H9v-2h2zm0-4H9v-2h2zm0-4H9V8h2zm4 8h-2v-6h2zm0-8h-2V8h2zm0-4H5V2h10z"];
})), Ej, Dj = o((() => {
	Ej = ["M15 5c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1s-1 .5-1 1v2c0 .6.4 1 1 1M5 5c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1s-1 .5-1 1v2c0 .6.4 1 1 1m13-2h-1v1c0 1.1-.9 2-2 2s-2-.9-2-2V3H7v1c0 1.1-.9 2-2 2s-2-.9-2-2V3H2c-.5 0-1 .5-1 1v14c0 .5.5 1 1 1h16c.5 0 1-.5 1-1V4c0-.5-.5-1-1-1M7 17H3v-4h4zm0-5H3V8h4zm5 5H8v-4h4zm0-5H8V8h4zm5 5h-4v-4h4zm0-5h-4V8h4z"];
})), Oj, kj = o((() => {
	Oj = ["M10 8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3m9-4h-3.59L13.7 2.29A.96.96 0 0 0 13 2H7c-.28 0-.53.11-.71.29L4.59 4H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h4.11c1.26 1.24 2.99 2 4.89 2s3.63-.76 4.89-2H19c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1M4 8H2V6h2zm6 8c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), Aj, jj = o((() => {
	Aj = ["M16 7c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1 0 .24.1.46.24.63l-.01.01 5 6 .01-.01c.19.22.45.37.76.37s.57-.15.76-.37l.01.01 5-6-.01-.01c.14-.17.24-.39.24-.63"];
})), Mj, Nj = o((() => {
	Mj = ["M13 4c-.24 0-.46.1-.63.24l-.01-.01-6 5 .01.01c-.22.19-.37.45-.37.76s.15.57.37.76l-.01.01 6 5 .01-.01c.17.14.39.24.63.24.55 0 1-.45 1-1V5c0-.55-.45-1-1-1"];
})), Pj, Fj = o((() => {
	Pj = ["M14 10c0-.31-.15-.57-.37-.76l.01-.01-6-5-.01.01C7.46 4.1 7.24 4 7 4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1 .24 0 .46-.1.63-.24l.01.01 6-5-.01-.01c.22-.19.37-.45.37-.76"];
})), Ij, Lj = o((() => {
	Ij = ["m15.76 12.37.01-.01-5-6-.01.01C10.57 6.15 10.31 6 10 6s-.57.15-.76.37l-.01-.01-5 6 .01.01c-.14.17-.24.39-.24.63 0 .55.45 1 1 1h10c.55 0 1-.45 1-1 0-.24-.1-.46-.24-.63"];
})), Rj, zj = o((() => {
	Rj = ["M12.5 1.25h4a1 1 0 0 1 1 1V5h-5zM2.75 5a.25.25 0 0 0-.25.25v6H.883a.5.5 0 0 0-.429.757l1.672 2.787c.17.284.384.533.63.741-.458.057-.959.09-1.506.09a.625.625 0 1 0 0 1.25c2.583 0 4.268-.68 5.202-1.146.687.466 1.88 1.146 3.548 1.146 1.65 0 2.837-.666 3.528-1.132l.005.003c.244.131.6.3 1.07.468.938.335 2.321.661 4.147.661a.625.625 0 1 0 0-1.25q-.478 0-.91-.03c.398-.318.717-.738.914-1.23l.972-2.43a.5.5 0 0 0-.464-.685H5v-6A.25.25 0 0 0 4.75 5zm3.455 11.95a.63.63 0 0 1 .658.041c.569.407 1.597 1.134 3.137 1.134s2.568-.727 3.137-1.134a.625.625 0 0 1 .724-.001l.007.005.045.029q.066.042.21.12a6.6 6.6 0 0 0 .9.392c.812.29 2.053.589 3.727.589a.625.625 0 1 1 0 1.25c-1.826 0-3.21-.326-4.148-.661a8 8 0 0 1-1.069-.468l-.005-.003c-.691.466-1.878 1.132-3.528 1.132-1.667 0-2.861-.68-3.548-1.146-.934.467-2.619 1.146-5.202 1.146a.625.625 0 1 1 0-1.25c2.66 0 4.23-.787 4.955-1.176M17.5 6.25h-5V10h4a1 1 0 0 0 1-1zm-11.25-4a1 1 0 0 1 1-1h4V5h-5zm5 4h-5V9a1 1 0 0 0 1 1h4z"];
})), Bj, Vj = o((() => {
	Bj = ["M11.5 8.32c.31-.35.51-.81.51-1.32 0-1.1-.9-2-2-2s-2 .9-2 2c0 .51.2.97.51 1.32L5.06 18.69c-.17.52.11 1.09.63 1.26s1.09-.11 1.26-.63L8.39 15h3.23l1.44 4.32c.17.52.74.81 1.26.63s.81-.74.63-1.26zM10.95 13H9.06l.95-2.84zm-5.64-2.27a.996.996 0 1 0 1.37-1.45c-1.4-1.33-1.28-3.35-.01-4.54.4-.38.43-1.01.05-1.41-.36-.41-1-.43-1.4-.06-2.09 1.95-2.28 5.3-.01 7.46M4.6 12.2C3 11.1 2 9 2 7c0-2.1.9-3.9 2.6-5.2.5-.3.5-1 .2-1.4-.3-.5-1-.5-1.4-.2C1.2 1.9-.1 4.2 0 7c.1 2.7 1.4 5.3 3.4 6.8.2.1.4.2.6.2.3 0 .6-.1.8-.4.4-.5.3-1.1-.2-1.4m8.67-1.51c.38.4 1.01.42 1.41.04 2.27-2.16 2.08-5.51-.01-7.46a.996.996 0 1 0-1.36 1.46c1.28 1.19 1.39 3.21-.01 4.54-.39.39-.41 1.02-.03 1.42M16.6.2c-.4-.3-1.1-.3-1.4.2-.3.4-.3 1.1.2 1.4C17.1 3.1 18 4.9 18 7c0 2-1 4.1-2.6 5.2-.5.3-.6.9-.2 1.4.2.3.5.4.8.4.2 0 .4-.1.6-.2C18.7 12.3 20 9.7 20 7c.09-2.8-1.2-5.1-3.4-6.8"];
})), Hj, Uj = o((() => {
	Hj = ["M18 16H2c-1.1 0-2 .9-2 2s.9 2 2 2h16c1.1 0 2-.9 2-2s-.9-2-2-2M3 5c.28 0 .53-.11.71-.29L5 3.41V13c0 .55.45 1 1 1s1-.45 1-1V3.41L8.29 4.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-3-3C6.53.11 6.28 0 6 0s-.53.11-.71.29l-3 3A1.003 1.003 0 0 0 3 5m7.29 5.71 3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3a1.003 1.003 0 0 0-1.42-1.42L15 10.59V1c0-.55-.45-1-1-1s-1 .45-1 1v9.59L11.71 9.3A.97.97 0 0 0 11 9a1.003 1.003 0 0 0-.71 1.71"];
})), Wj, Gj = o((() => {
	Wj = ["M7 11v8c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-8l-2 2zm-7 8c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-8l-6 3zM17 7l-3 3v9c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V8.74c-.26.15-.58.26-1 .26-1.92 0-2-2-2-2m2-6h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.59L10.8 8.78 7.45 7.11v.01C7.31 7.05 7.16 7 7 7s-.31.05-.44.11V7.1l-6 3v.01c-.33.17-.56.5-.56.89 0 .55.45 1 1 1 .16 0 .31-.05.44-.11v.01L7 9.12l3.55 1.78v-.01c.14.06.29.11.45.11.28 0 .53-.11.71-.29L18 4.41V6c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1"];
})), Kj, qj = o((() => {
	Kj = ["M19 0H7c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h5.59l3.71 3.71c.17.18.42.29.7.29.55 0 1-.45 1-1v-3h1c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M7 13c-1.1 0-2-.9-2-2V4H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h1v3a1.003 1.003 0 0 0 1.71.71L7.41 16H13c.55 0 1-.45 1-1v-.17L12.17 13z"];
})), Jj, Yj = o((() => {
	Jj = ["m8.41 10 5.29-5.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L7 8.59V4c0-.55-.45-1-1-1s-1 .45-1 1v12c0 .55.45 1 1 1s1-.45 1-1v-4.59l5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), Xj, Zj = o((() => {
	Xj = ["M16 6c-.28 0-.53.11-.71.29L10 11.59l-5.29-5.3a1.003 1.003 0 0 0-1.42 1.42l6 6c.18.18.43.29.71.29s.53-.11.71-.29l6-6A1.003 1.003 0 0 0 16 6"];
})), Qj, $j = o((() => {
	Qj = ["M13 3c-.55 0-1 .45-1 1v4.59l-5.29-5.3a1.003 1.003 0 0 0-1.42 1.42l5.3 5.29-5.29 5.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l5.29-5.3V16c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1"];
})), eM, tM = o((() => {
	eM = ["m8.41 10 5.29-5.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-6 6c-.18.18-.29.43-.29.71s.11.53.29.71l6 6a1.003 1.003 0 0 0 1.42-1.42z"];
})), nM, rM = o((() => {
	nM = ["m13.71 9.29-6-6a1.003 1.003 0 0 0-1.42 1.42l5.3 5.29-5.29 5.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l6-6c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), iM, aM = o((() => {
	iM = ["m16.71 12.29-6-6C10.53 6.11 10.28 6 10 6s-.53.11-.71.29l-6 6a1.003 1.003 0 0 0 1.42 1.42L10 8.41l5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), oM, sM = o((() => {
	oM = ["M10 0C4.5 0 0 4.5 0 10s4.5 10 10 10 10-4.5 10-10S15.5 0 10 0m0 18c-4.4 0-8-3.6-8-8s3.6-8 8-8 8 3.6 8 8-3.6 8-8 8"];
})), cM, lM = o((() => {
	cM = ["M14 10c-.28 0-.53.11-.71.29L11 12.59V5c0-.55-.45-1-1-1s-1 .45-1 1v7.59L6.71 10.3A.97.97 0 0 0 6 10a1.003 1.003 0 0 0-.71 1.71l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 14 10M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8"];
})), uM, dM = o((() => {
	uM = ["M15 9H7.41L9.7 6.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4c-.18.18-.29.43-.29.71s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L7.41 11H15c.55 0 1-.45 1-1s-.45-1-1-1m-5-9C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8"];
})), fM, pM = o((() => {
	fM = ["m15.71 9.29-4-4a1.003 1.003 0 0 0-1.42 1.42L12.59 9H5c-.55 0-1 .45-1 1s.45 1 1 1h7.59l-2.29 2.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8"];
})), mM, hM = o((() => {
	mM = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m.71-13.71C10.53 4.11 10.28 4 10 4s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L9 7.41V15c0 .55.45 1 1 1s1-.45 1-1V7.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), gM, _M = o((() => {
	gM = ["M8.533 17.357q.71.142 1.467.143V20c-.668 0-1.32-.067-1.951-.192zm3.417 2.45A10 10 0 0 1 10 20v-2.5q.758-.002 1.467-.143zm-8.188-5.642a7.6 7.6 0 0 0 2.073 2.073l-.696 1.038-.493.738-.203.3a10.1 10.1 0 0 1-2.757-2.758zm14.545 1.386.007.005a10.1 10.1 0 0 1-2.758 2.758l-.696-1.037-.695-1.039a7.6 7.6 0 0 0 2.073-2.073zM0 10c0-.668.067-1.32.191-1.951l1.226.242 1.226.242a7.6 7.6 0 0 0 0 2.934l-1.227.241.001.001-1.226.241A10 10 0 0 1 0 10m20 0c0 .668-.068 1.32-.192 1.95l-1.225-.241-1.226-.242q.142-.71.143-1.467-.002-.758-.143-1.467l2.45-.484q.191.948.193 1.951M5.14 2.723l.695 1.039a7.6 7.6 0 0 0-2.073 2.073L1.686 4.443a10.1 10.1 0 0 1 2.757-2.757zm10.416-1.037c1.09.73 2.028 1.667 2.758 2.757l-1.037.697v-.001l-1.039.696a7.6 7.6 0 0 0-2.073-2.073zM10 0c.667 0 1.32.067 1.95.191l-.483 2.452a7.6 7.6 0 0 0-2.934 0L8.05.19A10 10 0 0 1 10 0"];
})), vM, yM = o((() => {
	vM = ["M4 1C1.79 1 0 2.79 0 5s1.79 4 4 4c.1 0 .2-.01.3-.02C3.82 11.32 2.53 13 1 13c-.55 0-1 .45-1 1s.45 1 1 1c3.87 0 7-4.48 7-10 0-2.21-1.79-4-4-4m12 0c-2.21 0-4 1.79-4 4s1.79 4 4 4c.1 0 .2-.01.3-.02C15.82 11.32 14.53 13 13 13c-.55 0-1 .45-1 1s.45 1 1 1c3.87 0 7-4.48 7-10 0-2.21-1.79-4-4-4"];
})), bM, xM = o((() => {
	bM = ["M7 0 5 5 0 6.998 5 9l2 5 2-5 5-1.995L9 5zm8 10-1.5 3.496-3.5 1.499 3.5 1.498L15 20l1.5-3.507L20 15l-3.5-1.504z"];
})), SM, CM = o((() => {
	SM = ["M0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 0 2H2v4a1 1 0 0 1-2 0zm1 19a1 1 0 0 1-1-1v-5a1 1 0 1 1 2 0v4h4a1 1 0 1 1 0 2zm18 0a1 1 0 0 0 1-1v-5a1 1 0 1 0-2 0v4h-4a1 1 0 1 0 0 2zm0-20a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0V2h-4a1 1 0 1 1 0-2zm-9 14a4 4 0 1 0 0-8 4 4 0 0 0 0 8"];
})), wM, TM = o((() => {
	wM = ["M13 2c0-.55-.45-1-1-1h-.78a1.98 1.98 0 0 0-3.44 0H7c-.55 0-1 .45-1 1v2h7zm3 0h-2v3H5V2H3c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1"];
})), EM, DM = o((() => {
	EM = ["M7 9a1 1 0 0 1 1-1h6.586a1 1 0 0 1 .707.293l1.414 1.414a1 1 0 0 1 .293.707V19a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1zm2.5 2a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zM12 1.943c0-.534-.45-.972-1-.972h-.78A1.99 1.99 0 0 0 8.5 0c-.74 0-1.38.389-1.72.971H6c-.55 0-1 .438-1 .972V3h7zM13 4H4.04V2H3a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h3V8a1 1 0 0 1 1-1h8V3a1 1 0 0 0-1-1h-1z"];
})), OM, kM = o((() => {
	OM = ["M15 7c-.12 0-.24.03-.36.04C13.83 4.69 11.62 3 9 3 5.69 3 3 5.69 3 9c0 .05.01.09.01.14A3.98 3.98 0 0 0 0 13c0 2.21 1.79 4 4 4h11c2.76 0 5-2.24 5-5s-2.24-5-5-5"];
})), AM, jM = o((() => {
	AM = ["M15 4c-.12 0-.24.03-.36.04C13.83 1.69 11.62 0 9 0 5.69 0 3 2.69 3 6c0 .05.01.09.01.14A3.98 3.98 0 0 0 0 10c0 2.21 1.79 4 4 4h.78c.55-.61 1.34-1 2.22-1v-2c0-1.66 1.34-3 3-3s3 1.34 3 3v2c.88 0 1.66.38 2.2.98C17.87 13.87 20 11.69 20 9c0-2.76-2.24-5-5-5m-2 11c-.28 0-.53.11-.71.29L11 16.59V11c0-.55-.45-1-1-1s-1 .45-1 1v5.59L7.71 15.3A.97.97 0 0 0 7 15a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 13 15"];
})), MM, NM = o((() => {
	MM = ["M9 15h11v4H9zm3 2a1 1 0 1 0-2 0 1 1 0 0 0 2 0m2-1a1 1 0 0 0 0 2h4a1 1 0 0 0 0-2zm.784-10.978C14.856 5.01 14.928 5 15 5a5.004 5.004 0 0 1 4.9 4H9a1 1 0 0 0-1 1v5H4c-2.21 0-4-1.79-4-4a3.98 3.98 0 0 1 3.01-3.86l-.005-.07L3 7c0-3.31 2.69-6 6-6 2.62 0 4.83 1.69 5.64 4.04zM9 10h11v4H9zm3 2a1 1 0 1 0-2 0 1 1 0 0 0 2 0m2-1a1 1 0 0 0 0 2h4a1 1 0 0 0 0-2z"];
})), PM, FM = o((() => {
	PM = ["M14.784 4.022a2 2 0 0 1-.144.018C13.83 1.69 11.62 0 9 0 5.69 0 3 2.69 3 6q0 .037.005.07l.005.07A3.98 3.98 0 0 0 0 10c0 2.21 1.79 4 4 4h1.17a3 3 0 0 1 4.95-1.121l.88.878 4.879-4.878a3 3 0 0 1 4.115-.12A5 5 0 0 0 15 4q-.108.002-.216.022m-3.077 14.685a1 1 0 0 1-1.414 0l-3-3a1 1 0 1 1 1.414-1.414L11 16.586l6.293-6.293a1 1 0 0 1 1.414 1.414z"];
})), IM, LM = o((() => {
	IM = ["M10.71 10.29c-.18-.18-.43-.29-.71-.29s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L9 13.41V19c0 .55.45 1 1 1s1-.45 1-1v-5.59l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM15 4c-.12 0-.24.03-.36.04C13.83 1.69 11.62 0 9 0 5.69 0 3 2.69 3 6c0 .05.01.09.01.14A3.98 3.98 0 0 0 0 10c0 2.21 1.79 4 4 4 0-.83.34-1.58.88-2.12l3-3a2.993 2.993 0 0 1 4.24 0l3 3-.01.01c.52.52.85 1.23.87 2.02C18.28 13.44 20 11.42 20 9c0-2.76-2.24-5-5-5"];
})), RM, zM = o((() => {
	RM = ["M6 6a1.003 1.003 0 0 0-1.71-.71l-4 4C.11 9.47 0 9.72 0 10s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L2.41 10 5.7 6.71c.19-.18.3-.43.3-.71m6-4c-.46 0-.83.31-.95.73l-4 14c-.02.09-.05.17-.05.27 0 .55.45 1 1 1 .46 0 .83-.31.95-.73l4-14c.02-.09.05-.17.05-.27 0-.55-.45-1-1-1m7.71 7.29-4-4a1.003 1.003 0 0 0-1.42 1.42l3.3 3.29-3.29 3.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), BM, VM = o((() => {
	BM = ["M19 5h-2V3c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v2H9V3c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v2H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1M8.71 15.29a1.003 1.003 0 0 1-1.42 1.42l-4-4C3.11 12.53 3 12.28 3 12s.11-.53.29-.71l4-4a1.003 1.003 0 0 1 1.42 1.42L5.41 12zm8-2.58-4 4a1.003 1.003 0 0 1-1.42-1.42l3.3-3.29-3.29-3.29A.97.97 0 0 1 11 8a1.003 1.003 0 0 1 1.71-.71l4 4c.18.18.29.43.29.71s-.11.53-.29.71"];
})), HM, UM = o((() => {
	HM = ["M19 8h-2.31c-.14-.46-.33-.89-.56-1.3l1.7-1.7a.996.996 0 0 0 0-1.41l-1.41-1.41a.996.996 0 0 0-1.41 0l-1.7 1.7c-.41-.22-.84-.41-1.3-.55V1c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v2.33c-.48.14-.94.34-1.37.58L5 2.28a.97.97 0 0 0-1.36 0L2.28 3.64c-.37.38-.37.99 0 1.36L3.9 6.62c-.24.44-.44.89-.59 1.38H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h2.31c.14.46.33.89.56 1.3L2.17 15a.996.996 0 0 0 0 1.41l1.41 1.41c.39.39 1.02.39 1.41 0l1.7-1.7c.41.22.84.41 1.3.55V19c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-2.33c.48-.14.94-.35 1.37-.59L15 17.72c.37.37.98.37 1.36 0l1.36-1.36c.37-.37.37-.98 0-1.36l-1.62-1.62c.24-.43.45-.89.6-1.38H19c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-9 6c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4"];
})), WM, GM = o((() => {
	WM = ["M9.29 8.71c.18.18.43.29.71.29s.53-.11.71-.29l6-6a1.003 1.003 0 0 0-1.42-1.42L10 6.59l-5.29-5.3a1.003 1.003 0 0 0-1.42 1.42zm1.42 2.58c-.18-.18-.43-.29-.71-.29s-.53.11-.71.29l-6 6a1.003 1.003 0 0 0 1.42 1.42l5.29-5.3 5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), KM, qM = o((() => {
	KM = ["M2.188 9c.217-.52.623-.983 1.226-1.586L8 2.828 14.172 9zM8 0 6.586 1.414 2 6c-1 1-2 2.11-2 4 0 2 1 3 2 4l1 1c1 1 2 2 4 2 2.009 0 2.918-.913 3.868-1.867L11 15l4.586-4.586L17 9l-1.414-1.414-6.172-6.172zm10.5 13.5L17 11l-1.5 2.5c-.318.53-.5 1-.5 1.5 0 1 .5 2 2 2s2-1 2-2c0-.5-.182-.97-.5-1.5M1 18a1 1 0 1 0 0 2h18a1 1 0 1 0 0-2z"];
})), JM, YM = o((() => {
	JM = ["M19 1H1c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M5 17H2V3h3zm4 0H6V3h3zm9 0h-8V3h8z"];
})), XM, ZM = o((() => {
	XM = ["M19 1H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3v4a1.003 1.003 0 0 0 1.71.71l4.7-4.71H19c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M4 10c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2m6 0c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2m6 0c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2"];
})), QM, $M = o((() => {
	QM = ["M6 8H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m13-6h-5c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m0 3h-5V3h5zM6 14H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1M6 2H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m4-2c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m9 14h-5c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1m0 3h-5v-2h5zm0-9h-5c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m0 3h-5V9h5z"];
})), eN, tN = o((() => {
	eN = ["M15 10c0 .14-.03.28-.09.4l-3.99 8.98-.01.02a.991.991 0 0 1-1.82 0l-.01-.02-3.99-8.98c-.06-.12-.09-.26-.09-.4s.03-.28.09-.4L9.08.62 9.09.6a.991.991 0 0 1 1.82 0l.01.02 3.99 8.98c.06.12.09.26.09.4m-5-6.54L7.09 10h5.81z"];
})), nN, rN = o((() => {
	nN = ["m19.89 6.56-2.99-6h-.01C16.72.23 16.39 0 16 0H4c-.39 0-.72.23-.89.56H3.1l-3 6h.01C.05 6.69 0 6.84 0 7v12c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V7c0-.16-.05-.31-.11-.44M11 2h4.38l2 4H11zM4.62 2H9v4H2.62zM18 18H2V8h7v4.59L6.71 10.3A.97.97 0 0 0 6 10a1.003 1.003 0 0 0-.71 1.71l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4a1.003 1.003 0 0 0-1.42-1.42L11 12.59V8h7z"];
})), iN, aN = o((() => {
	iN = ["M9.71 5.29a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l7-7a1.003 1.003 0 0 0-1.42-1.42L12 7.59zm7.93 2.32c.23.75.36 1.56.36 2.39 0 4.42-3.58 8-8 8s-8-3.58-8-8a7.998 7.998 0 0 1 11.8-7.04l1.46-1.46C13.73.56 11.93 0 10 0 4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10c0-1.4-.29-2.73-.81-3.95z"];
})), oN, sN = o((() => {
	oN = ["M19 19H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1h18c.55 0 1 .45 1 1v16c0 .55-.45 1-1 1M18 6H2v11h16zM4 8c.28 0 .53.11.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2a1.003 1.003 0 0 1-1.42-1.42L4.59 11l-1.3-1.29A1.003 1.003 0 0 1 4 8m5 4h3c.55 0 1 .45 1 1s-.45 1-1 1H9c-.55 0-1-.45-1-1s.45-1 1-1"];
})), cN, lN = o((() => {
	cN = ["M15 6H2v11h16v-5a2.98 2.98 0 0 0 2-.769V18c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1h14zM4 8c.28 0 .53.11.71.29l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2a1.003 1.003 0 0 1-1.42-1.42L4.59 11l-1.3-1.29A1.003 1.003 0 0 1 4 8m8 4c.55 0 1 .45 1 1s-.45 1-1 1H9c-.55 0-1-.45-1-1s.45-1 1-1zm6-4a1 1 0 1 1 0 2 1 1 0 0 1 0-2m0-8a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0V1a1 1 0 0 1 1-1"];
})), uN, dN = o((() => {
	uN = ["M6 1a1 1 0 0 1 1 1v2h6V2a1 1 0 1 1 2 0v2h2.038c.216 0 .453 0 .65.022.202.022.584.086.894.396s.374.692.396.893c.022.198.022.435.022.65v6.077c0 .216 0 .453-.022.65-.022.202-.086.584-.396.894s-.692.374-.893.396a6 6 0 0 1-.65.022H15v4a1 1 0 1 1-2 0v-4H7v4a1 1 0 1 1-2 0v-4H2.962c-.216 0-.453 0-.65-.022-.202-.022-.584-.086-.894-.396s-.374-.692-.396-.893C1 12.49 1 12.254 1 12.039V5.961c0-.216 0-.453.022-.65.022-.202.086-.584.396-.894s.692-.374.893-.396C2.51 4 2.746 4 2.961 4H5V2a1 1 0 0 1 1-1m0 5H4.201l4 6h2.596l-4-6zm3.202 0 4 6h2.596l-4-6zm5 0L17 10.197V6zm-8.404 6L3 7.803V12z"];
})), fN, pN = o((() => {
	fN = ["M19 8h-1.26c-.19-.73-.48-1.42-.85-2.06l.94-.94a.996.996 0 0 0 0-1.41l-1.41-1.41a.996.996 0 0 0-1.41 0l-.94.94c-.65-.38-1.34-.67-2.07-.86V1c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v1.26c-.76.2-1.47.5-2.13.89L5 2.28a.97.97 0 0 0-1.36 0L2.28 3.64c-.37.38-.37.98 0 1.36l.87.87c-.39.66-.69 1.37-.89 2.13H1c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h1.26c.19.73.48 1.42.85 2.06l-.94.94a.996.996 0 0 0 0 1.41l1.41 1.41c.39.39 1.02.39 1.41 0l.94-.94c.64.38 1.33.66 2.06.85V19c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-1.26c.76-.2 1.47-.5 2.13-.89l.88.87c.37.37.98.37 1.36 0l1.36-1.36c.37-.38.37-.98 0-1.36l-.87-.87c.4-.65.7-1.37.89-2.13H19c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1m-9 7c-2.76 0-5-2.24-5-5s2.24-5 5-5z"];
})), mN, hN = o((() => {
	mN = ["M17 10h-7v7h7zm0-7h-7v6h7zM9 3H3v14h6zm10-3H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2V2h16z"];
})), gN, _N = o((() => {
	gN = ["M19 3H1c-.55 0-1 .45-1 1v2h20V4c0-.55-.45-1-1-1M0 16c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V8H0zm6.5-2h7c.28 0 .5.22.5.5s-.22.5-.5.5h-7c-.28 0-.5-.22-.5-.5s.22-.5.5-.5m-4 0h2c.28 0 .5.22.5.5s-.22.5-.5.5h-2c-.28 0-.5-.22-.5-.5s.22-.5.5-.5"];
})), vN, yN = o((() => {
	vN = ["M14 19a1 1 0 1 0 2 0v-3h3a1 1 0 1 0 0-2H6V1a1 1 0 1 0-2 0v3H1a1 1 0 1 0 0 2h3v9a1 1 0 0 0 1 1h9zm1-15H8v2h6v6h2V5a1 1 0 0 0-1-1"];
})), bN, xN = o((() => {
	bN = ["m11.41 10 4.29-4.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L10 8.59l-4.29-4.3a1.003 1.003 0 0 0-1.42 1.42L8.59 10 4.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4.29-4.3 4.29 4.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), SN, CN = o((() => {
	SN = ["M10 20c5.523 0 10-4.477 10-10S15.523 0 10 0 0 4.477 0 10s4.477 10 10 10m4.7-13.29L11.41 10l3.3 3.29A1.003 1.003 0 0 1 14 15c-.28 0-.53-.11-.71-.3L10 11.41l-3.29 3.3A1.003 1.003 0 0 1 5 14c0-.28.11-.53.3-.71L8.59 10l-3.3-3.29a1.003 1.003 0 0 1 1.42-1.42L10 8.59l3.29-3.3A1.003 1.003 0 0 1 15 6c0 .28-.11.53-.3.71"];
})), wN, TN = o((() => {
	wN = ["m2 8 4 2 4-5 4 5 4-2-1 7H3zm8-6a1 1 0 1 1 0 2 1 1 0 0 1 0-2M1 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2m18 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M3 16h14v2H3z"];
})), EN, DN = o((() => {
	EN = ["m14.5 2 1.047 2.953L18.5 6l-2.953 1.047L14.5 10l-1.046-2.953L10.5 6l2.954-1.047zM10 1c1.08 0 2.11.203 3.06.57l-.668 1.886a6.5 6.5 0 1 0 4.081 5.464l.248-.7 1.577-.558a8.47 8.47 0 0 1-2.23 7.786c.267.271.432.642.432 1.052 0 .822-.422 1.452-.862 1.868-.437.413-.988.716-1.545.939-1.123.449-2.57.693-4.093.693s-2.97-.244-4.093-.693c-.557-.223-1.108-.526-1.545-.939-.44-.416-.862-1.046-.862-1.868 0-.41.164-.781.43-1.052A8.5 8.5 0 0 1 10 1m0 7 .764 2.236L13 11l-2.236.764L10 14l-.764-2.236L7 11l2.236-.764z"];
})), ON, kN = o((() => {
	ON = ["M3 1a1 1 0 0 1 1-1h9l6 6v13a1 1 0 0 1-1 1h-3.708c.4-.44.708-1.042.708-1.75q0-.13-.012-.25H17V7h-5V2H5v11.72l-.04.035c-.164.141-.32.308-.458.497a2.7 2.7 0 0 0-.546-.605A2.8 2.8 0 0 0 3 13.142zM2 14c-.518 0-.982.158-1.34.463A1.93 1.93 0 0 0 0 15.75v2.5c0 .492.26.933.613 1.238C.97 19.797 1.46 20 2 20c1.015 0 2-.702 2-1.75a.5.5 0 0 0-1 0c0 .333-.358.75-1 .75a1.13 1.13 0 0 1-.734-.27c-.19-.163-.266-.347-.266-.48v-2.5a.84.84 0 0 1 .308-.526C1.463 15.092 1.69 15 2 15c.334 0 .55.081.69.196.139.113.26.304.317.638a.5.5 0 0 0 .986-.168c-.086-.51-.3-.943-.67-1.244C2.957 14.122 2.494 14 2 14m3.613.512A2.13 2.13 0 0 1 7 14c1.015 0 2 .702 2 1.75a.5.5 0 0 1-1 0c0-.333-.358-.75-1-.75-.289 0-.549.11-.734.27-.19.163-.266.347-.266.48 0 .121.049.229.25.366.221.15.533.27.925.416l.03.01c.353.132.776.29 1.107.516.362.245.688.623.688 1.192 0 .492-.26.933-.613 1.238A2.13 2.13 0 0 1 7 20c-1.015 0-2-.702-2-1.75a.5.5 0 0 1 1 0c0 .333.358.75 1 .75.289 0 .549-.11.734-.27.19-.163.266-.347.266-.48 0-.121-.049-.229-.25-.366-.288-.195-.632-.306-.955-.427-.353-.131-.776-.289-1.107-.515C5.326 16.697 5 16.32 5 15.75c0-.492.26-.933.613-1.238M12 14c-.54 0-1.03.203-1.387.512-.353.305-.613.746-.613 1.238 0 .57.326.947.688 1.192.331.226.754.384 1.107.515.323.12.667.232.955.427.201.137.25.245.25.366 0 .133-.076.317-.266.48A1.13 1.13 0 0 1 12 19c-.642 0-1-.417-1-.75a.5.5 0 0 0-1 0c0 1.048.985 1.75 2 1.75.54 0 1.03-.203 1.387-.512.353-.305.613-.746.613-1.238 0-.57-.326-.947-.688-1.192-.331-.226-.754-.384-1.107-.515l-.03-.011c-.392-.146-.704-.266-.925-.416-.201-.137-.25-.245-.25-.366 0-.133.076-.317.266-.48.185-.16.445-.27.734-.27.642 0 1 .417 1 .75a.5.5 0 0 0 1 0c0-1.048-.985-1.75-2-1.75"];
})), AN, jN = o((() => {
	AN = ["m1.953 4.481 7.41-4.02a1.34 1.34 0 0 1 1.275 0l7.409 4.02L10 9.22zm-.817.68L9.5 10.085v9.281a1 1 0 0 1-.138-.064l-7.714-4.186A1.21 1.21 0 0 1 1 14.057v-8.35c0-.193.048-.38.136-.547m17.728 0c.088.166.136.353.136.546v8.35c0 .438-.247.842-.648 1.06l-7.714 4.186q-.067.037-.138.064v-9.281z"];
})), MN, NN = o((() => {
	MN = ["M17 3h2a1 1 0 0 1 0 2h-2v2a1 1 0 0 1-2 0V5h-2a1 1 0 0 1 0-2h2V1a1 1 0 0 1 2 0zm-3.969 4.435L10 9.22 1.953 4.48 9.363.46a1.34 1.34 0 0 1 1.275 0l1.33.721A3.001 3.001 0 0 0 13 7q0 .222.031.435m.319.972A3 3 0 0 0 19 7v7.057c0 .438-.247.842-.648 1.06l-7.714 4.186q-.067.037-.138.064v-9.281zM1.136 5.16 9.5 10.086v9.281a1 1 0 0 1-.138-.064l-7.714-4.186A1.21 1.21 0 0 1 1 14.057v-8.35c0-.193.048-.38.136-.547"];
})), PN, FN = o((() => {
	PN = ["M18.75 0C19.44 0 20 .56 20 1.25v17.5c0 .69-.56 1.25-1.25 1.25H1.25C.56 20 0 19.44 0 18.75V1.25C0 .56.56 0 1.25 0zM10.5 10v7l4.964-2.397c.474-.215.786-.735.786-1.314V6.627l-.001-.012C14.357 7.743 12.398 8.882 10.5 10M3.75 6.71v6.663c0 .536.268 1.026.69 1.266L9.5 17v-7L3.756 6.619q-.004.045-.006.091m6.752-3.506a1.12 1.12 0 0 0-1.023-.047l-4.943 2.24q-.105.047-.196.113L10 9c1.1-.648 4.733-2.935 5.723-3.526a1 1 0 0 0-.164-.113z"];
})), IN, LN = o((() => {
	IN = ["M19 4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm-4.43 6.731-1.604.947-.466.273v5.485l3.871-1.753c.38-.172.629-.589.629-1.052V9.3l-.001-.009c-.487.29-1.48.88-2.429 1.44M7 9.368v5.33c0 .429.214.821.553 1.013l3.947 1.682V11.95L7.005 9.295Q7 9.332 7 9.368m5.401-2.805a.9.9 0 0 0-.818-.038L7.629 8.317a1 1 0 0 0-.157.091L12 11.086l.458-.27 1.604-.946a646 646 0 0 0 2.516-1.491 1 1 0 0 0-.13-.09zM0 1a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2H4a1 1 0 0 0-1 1v14H1a1 1 0 0 1-1-1z"];
})), RN, zN = o((() => {
	RN = ["M13.809 2.2 10.638.48a1.35 1.35 0 0 0-1.276 0L1.953 4.5l6.014 3.542zM7.237 8.773 1.136 5.18A1.2 1.2 0 0 0 1 5.726v8.35c0 .438.247.843.648 1.06l7.714 4.186q.068.037.138.065v-5.543l-3.168 1.101a1 1 0 0 1-1.274-1.27l1.345-3.893a1 1 0 0 1 .254-.43zm3.263 4.69v5.924q.07-.028.138-.065l7.714-4.186c.4-.217.648-.622.648-1.06v-8.35c0-.193-.048-.38-.136-.546l-.154.09-.58.58a1 1 0 0 1-.068.077l-7.415 7.415a1 1 0 0 1-.147.121M8.067 9.355l2.575 2.575 6.709-6.709-2.576-2.575zM6 14.002l3.935-1.367-2.573-2.574zM18.221-.004c-.49 0-.969.161-1.29.491l-1.45 1.454 2.57 2.574L19.5 3.06c.32-.33.499-.792.499-1.282 0-.98-.8-1.783-1.779-1.783"];
})), BN, VN = o((() => {
	BN = ["M11.968 1.182A3.001 3.001 0 0 0 13 7h.77L10 9.22 1.953 4.48 9.363.46a1.34 1.34 0 0 1 1.275 0zM19 7v7.057c0 .438-.247.842-.648 1.06l-7.714 4.186q-.067.037-.138.064v-9.281L15.74 7zM1.136 5.16 9.5 10.086v9.281a1 1 0 0 1-.138-.064l-7.714-4.186A1.21 1.21 0 0 1 1 14.057v-8.35c0-.193.048-.38.136-.547M13 3h6a1 1 0 0 1 0 2h-6a1 1 0 0 1 0-2"];
})), HN, UN = o((() => {
	HN = ["m9.707 6.408 4.894-2.293c.367-.172.794-.15 1.142.06l3.662 2.205c.369.223.595.624.595 1.058v5.037c0 .48-.276.916-.707 1.118l-4.894 2.292c-.367.172-.794.15-1.142-.06L9.595 13.62A1.23 1.23 0 0 1 9 12.562V7.525c0-.48.276-.915.707-1.117M.812 2.098 4.923.139a1.43 1.43 0 0 1 1.365.072l3.031 1.857c.423.26.681.718.681 1.213v1.885l-.717.336A2.23 2.23 0 0 0 8 7.525v1.562l-1.19-.729a2.43 2.43 0 0 0-2.317-.122L1.71 9.563.68 8.932A1.42 1.42 0 0 1 0 7.719V3.382c0-.548.316-1.048.812-1.284M8 10.26v2.302c0 .782.408 1.51 1.08 1.914l.92.555v1.587c0 .548-.316 1.048-.812 1.284l-4.111 1.959a1.43 1.43 0 0 1-1.365-.072L.681 17.932A1.42 1.42 0 0 1 0 16.719v-4.337c0-.548.316-1.048.812-1.284l4.111-1.959a1.43 1.43 0 0 1 1.365.072z"];
})), WN, GN = o((() => {
	WN = ["M8 3c-1.292 0-2.303.369-2.832 1.305-.234.415-.32.859-.353 1.245a9 9 0 0 0-.001 1.12c.034.758.055 1.255-.08 1.644a.85.85 0 0 1-.253.385c-.124.108-.34.235-.724.33a1 1 0 0 0 0 1.941c.384.096.6.223.724.331a.85.85 0 0 1 .254.386c.134.388.113.885.079 1.643a9 9 0 0 0 .001 1.12c.033.386.119.83.353 1.245C5.697 16.63 6.708 17 8 17a1 1 0 1 0 0-2c-.933 0-1.066-.244-1.089-.286l-.001-.003c-.04-.069-.082-.196-.102-.43a7 7 0 0 1 .003-.86l.007-.145c.03-.613.073-1.475-.193-2.244A2.9 2.9 0 0 0 6.01 10c.293-.314.489-.668.615-1.032.266-.769.223-1.63.193-2.244l-.007-.144a7 7 0 0 1-.003-.86c.02-.235.063-.362.102-.432l.001-.002C6.934 5.244 7.067 5 8 5a1 1 0 0 0 0-2m4 0c1.293 0 2.303.369 2.832 1.305.234.415.32.859.353 1.245.032.384.017.781.002 1.12-.035.758-.056 1.255.078 1.644.056.16.134.282.254.385.124.108.34.235.723.33a1 1 0 0 1 0 1.941c-.383.096-.599.223-.723.331a.85.85 0 0 0-.254.386c-.134.388-.113.885-.079 1.643a9 9 0 0 1-.001 1.12c-.033.386-.119.83-.353 1.245C14.302 16.63 13.292 17 12 17a1 1 0 1 1 0-2c.933 0 1.066-.244 1.088-.286l.002-.003c.04-.069.082-.196.102-.43a7 7 0 0 0-.004-.86l-.006-.145c-.03-.613-.073-1.475.193-2.244A2.9 2.9 0 0 1 13.99 10a2.9 2.9 0 0 1-.615-1.032c-.266-.769-.223-1.63-.193-2.244l.006-.144a7 7 0 0 0 .004-.86c-.02-.235-.063-.362-.102-.432l-.002-.002C13.067 5.244 12.934 5 12 5a1 1 0 1 1 0-2"];
})), KN, qN = o((() => {
	KN = ["M19 16H3.02l2.14-1.74c2.25 1.7 7.33.46 11.83-2.99l-1.29-1.5c-3.56 2.74-7.31 4.03-8.93 3.19l10.55-8.57-.63-.78-10.59 8.6c-.64-1.64 1.46-4.91 5.09-7.7L9.9 3.01c-4.6 3.54-6.91 8.12-5.41 10.51L2 15.54V3c0-.55-.45-1-1-1s-1 .45-1 1v14a1 1 0 0 0 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), JN, YN = o((() => {
	JN = ["M16 2s.72-1.28 0-2l-5.29 6.25 1.28 1.54zm.08 10c-.55 0-1.07.12-1.54.32L4.31 0c-.7.72 0 2 0 2l4.45 6.56-3.19 3.77C5.09 12.12 4.56 12 4 12c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4c0-.65-.17-1.26-.45-1.8l2.54-3.67 2.49 3.67c-.27.54-.44 1.15-.44 1.8 0 2.21 1.76 4 3.92 4 2.17 0 3.92-1.79 3.92-4 .02-2.21-1.74-4-3.9-4M4 18c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2m12.08 0c-1.08 0-1.96-.9-1.96-2s.88-2 1.96-2 1.96.9 1.96 2-.88 2-1.96 2"];
})), XN, ZN = o((() => {
	XN = ["M16 10a4 4 0 1 1 0 8 4 4 0 0 1 0-8M4 10a4 4 0 1 1 0 8 4 4 0 0 1 0-8m7.299-5.543.087.089 1.93 2.232 2.048.708a1 1 0 0 1 .65 1.16l-.031.112a1 1 0 0 1-1.16.65l-.112-.031-2.302-.796a1 1 0 0 1-.337-.197l-.092-.094-1.387-1.603-1.891 1.982 2.046 2.274a1 1 0 0 1 .25.547l.007.122v4.24a1 1 0 0 1-1.993.117l-.007-.117-.001-3.857-2.408-2.676a1 1 0 0 1-.063-1.26l.082-.099 3.29-3.45a1 1 0 0 1 1.394-.053M16 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4M4 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m9.5-10a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3"];
})), QN, $N = o((() => {
	QN = ["M6 5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1M4 9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m6-4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1m0-5C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m6-9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m-8 5c0 1.1.9 2 2 2s2-.9 2-2c0-.33-2-8-2-8s-2 7.67-2 8m6-9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1"];
})), eP, tP = o((() => {
	eP = ["M19 11c0 .552-2.239 1-5 1s-5-.448-5-1 2.239-1 5-1 5 .448 5 1m-1.268 1.688c.47-.094.913-.216 1.268-.379V15c0 .197-.285.38-.776.535l-.003.001c-.887.279-2.446.464-4.221.464s-3.334-.185-4.221-.464h-.003C9.285 15.38 9 15.196 9 15v-2.69c.355.162.799.284 1.268.378.987.197 2.306.312 3.732.312s2.745-.115 3.732-.312M9 16.31c.355.163.798.284 1.268.378.987.197 2.306.312 3.732.312s2.745-.115 3.732-.312c.469-.094.913-.216 1.268-.378V19c0 .552-2.239 1-5 1s-5-.448-5-1zm5.784-12.288q.108-.02.216-.022a5.002 5.002 0 0 1 4.814 6.354 1.4 1.4 0 0 0-.217-.27 2 2 0 0 0-.562-.377c-.36-.17-.818-.298-1.303-.395C16.745 9.115 15.426 9 14 9s-2.745.115-3.732.312c-.485.097-.942.224-1.303.395a2 2 0 0 0-.562.376A1.28 1.28 0 0 0 8 11v3H4c-2.21 0-4-1.79-4-4a3.98 3.98 0 0 1 3.01-3.86l-.005-.07L3 6c0-3.31 2.69-6 6-6 2.62 0 4.83 1.69 5.64 4.04z"];
})), nP, rP = o((() => {
	nP = ["M2 11.9c.935.674 2.339 1.217 4.023 1.536A7 7 0 0 0 9.393 20c-3.988-.019-7.231-1.083-7.387-2.4L2 17.5zM13 8c3.315 0 6 2.685 6 6s-2.685 6-6 6-6-2.685-6-6 2.685-6 6-6m1 1-4 6h2.5l-.5 4 4-6h-2.5zm3-4.6v3.855a7.003 7.003 0 0 0-10.779 3.992c-2.408-.391-4.097-1.202-4.214-2.142L2 10V4.4c1.525 1.1 4.3 1.85 7.5 1.85S15.475 5.5 17 4.4M9.5 0C13.637 0 17 1.125 17 2.5S13.637 5 9.5 5C5.35 5 2 3.875 2 2.5S5.35 0 9.5 0"];
})), iP, aP = o((() => {
	iP = ["M1.053 0C.47 0 0 .471 0 1.053V4.21c0 .58.471 1.052 1.053 1.052h3.275A6.33 6.33 0 0 0 8.056 10a6.33 6.33 0 0 0-3.728 4.737l-3.275-.001A1.053 1.053 0 0 0 0 15.789v3.158C0 19.53.471 20 1.053 20h7.435c.581 0 1.053-.471 1.053-1.053V15.79c0-.58-.472-1.052-1.053-1.052H5.406a5.29 5.29 0 0 1 5.195-4.21v2.105c0 .58.471 1.052 1.052 1.052h7.294c.582 0 1.053-.471 1.053-1.052V7.368c0-.58-.471-1.052-1.053-1.052h-7.294c-.581 0-1.052.471-1.052 1.052v2.106a5.29 5.29 0 0 1-5.194-4.21h3.081c.581 0 1.053-.472 1.053-1.053V1.053A1.053 1.053 0 0 0 8.488 0z"];
})), oP, sP = o((() => {
	oP = ["M2 9.5V4.1C3.5 5.23 6.52 6 10 6c3.49 0 6.51-.77 8-1.9v5.4a1 1 0 0 1-.016.159 6.002 6.002 0 0 0-10.87 2.173C4.12 11.47 2 10.562 2 9.5m5 3.406V13a6.005 6.005 0 0 0 5.017 5.92c-.644.052-1.32.08-2.017.08-4.42 0-8-1.12-8-2.5v-5.4c1.047.789 2.835 1.402 5.003 1.701zM18 2.5C18 3.88 14.42 5 10 5 5.59 5 2 3.88 2 2.5S5.58 0 10 0s8 1.12 8 2.5m-2.243 14.672A5.003 5.003 0 0 1 8 13v-.078a5.002 5.002 0 0 1 9.67-1.71 5 5 0 0 1-.498 4.545l2.534 2.534a1 1 0 1 1-1.415 1.415zM13 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6"];
})), cP, lP = o((() => {
	cP = ["M1 4.1v5.4c0 1.293 3.145 2.358 7.179 2.487l.404-.404A2 2 0 0 1 10 11c.548 0 1.052.217 1.417.583l.272.272q.16-.017.318-.038c.037-.462.218-.906.56-1.25.389-.387.906-.567 1.433-.567a4.96 4.96 0 0 1 2.268.546c.47-.318.732-.672.732-1.046V4.1C15.51 5.23 12.49 6 9 6c-3.48 0-6.5-.77-8-1.9m0 7c1.24.934 3.516 1.622 6.233 1.832l-.65.65A2.003 2.003 0 0 0 8.1 16.998c.15.74.465 1.42.904 2.003H9c-4.42 0-8-1.12-8-2.5zM9 5c4.42 0 8-1.12 8-2.5S13.42 0 9 0 1 1.12 1 2.5 4.59 5 9 5m5 6c2.2 0 4 1.8 4 4v.59l.29-.29c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71l-2 2c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-2-2a1.003 1.003 0 0 1 1.42-1.42l.29.3V15c0-1.1-.9-2-2-2-.6 0-1-.4-1-1s.4-1 1-1m-6 5c.28 0 .53-.11.71-.29l.29-.3V16c0 2.2 1.8 4 4 4 .6 0 1-.4 1-1s-.4-1-1-1c-1.1 0-2-.9-2-2v-.59l.29.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-2-2A1 1 0 0 0 10 12c-.28 0-.53.11-.71.29l-2 2A1.003 1.003 0 0 0 8 16"];
})), uP, dP = o((() => {
	uP = ["M2.01 5.1v5.4c0 1.38 3.58 2.5 8 2.5s8-1.12 8-2.5V5.1c-1.49 1.13-4.51 1.9-8 1.9-3.48 0-6.5-.77-8-1.9m8 .9c4.42 0 8-1.12 8-2.5s-3.58-2.5-8-2.5-8 1.12-8 2.5S5.6 6 10.01 6m-8 6.1v5.4c0 1.38 3.58 2.5 8 2.5s8-1.12 8-2.5v-5.4c-1.49 1.13-4.51 1.9-8 1.9-3.48 0-6.5-.77-8-1.9"];
})), fP, pP = o((() => {
	fP = ["M15 6a1.003 1.003 0 0 0-1.71-.71L10 8.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42L8.59 10 5.3 13.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3.29-3.3 3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L11.41 10l3.29-3.29c.19-.18.3-.43.3-.71m-5-6C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8"];
})), mP, hP = o((() => {
	mP = ["M19.707.293a1 1 0 0 0-1.414 0L15.5 3.086 12.707.293a1 1 0 1 0-1.414 1.414L14.086 4.5l-2.793 2.793a1 1 0 0 0 1.414 1.414L15.5 5.914l2.793 2.793a1 1 0 1 0 1.414-1.414L16.914 4.5l2.793-2.793a1 1 0 0 0 0-1.414M0 5a1 1 0 0 1 1-1h4a1 1 0 0 1 0 2H2v3a1 1 0 0 1-2 0zm1 15a1 1 0 0 1-1-1v-4a1 1 0 1 1 2 0v3h3a1 1 0 1 1 0 2zm10 0h4a1 1 0 0 0 1-1v-4a1 1 0 1 0-2 0v3h-3a1 1 0 1 0 0 2m0-8a3 3 0 1 1-6 0 3 3 0 0 1 6 0"];
})), gP, _P = o((() => {
	gP = ["M10 0 0 20h20zM9 6l6 12H3z"];
})), vP, yP = o((() => {
	vP = ["M7.1 8.2h-.99c.28-1.11.66-1.92 1.12-2.43.28-.32.56-.48.83-.48.05 0 .1.02.13.05s.05.07.05.12c0 .04-.04.13-.11.25a.64.64 0 0 0-.12.35q0 .225.18.39c.12.11.27.16.45.16.2 0 .36-.07.49-.2s.2-.31.2-.54q0-.39-.3-.63C8.84 5.08 8.52 5 8.08 5c-.68 0-1.3.19-1.85.58-.56.38-1.09 1.02-1.59 1.91-.17.3-.34.5-.49.59-.15.08-.4.13-.74.12l-.23.77h.95l-1.39 5.24c-.23.86-.39 1.39-.47 1.59q-.18.435-.54.75c-.1.08-.21.12-.35.12-.04 0-.07-.01-.1-.03l-.03-.04c0-.02.03-.07.1-.13.07-.07.1-.17.1-.31 0-.15-.05-.28-.16-.38s-.27-.15-.47-.15c-.25 0-.44.07-.59.2-.15.12-.23.28-.23.46 0 .19.09.36.27.5.19.14.47.21.86.21.61 0 1.16-.15 1.63-.46.48-.31.89-.78 1.25-1.43.35-.64.72-1.68 1.09-3.11l.8-3.03h.96zM19 0h-9c-.55 0-1 .45-1 1v3h2V2h7v16h-7v-2H9v3c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-8.79 13.49c.15.28.32.49.52.61.19.12.44.19.73.19.28 0 .57-.1.86-.3.38-.25.77-.69 1.17-1.31l-.25-.14c-.27.37-.48.6-.61.69-.09.06-.19.09-.31.09-.14 0-.28-.09-.42-.26q-.345-.435-.93-2.4c.35-.59.64-.97.87-1.15.17-.13.35-.2.55-.2.07 0 .2.03.39.08s.36.08.5.08c.2 0 .37-.07.5-.2.15-.14.22-.31.22-.52 0-.22-.07-.4-.2-.53s-.33-.2-.58-.2q-.33 0-.63.15c-.2.1-.45.32-.75.67-.23.25-.56.7-1.01 1.33a6.5 6.5 0 0 0-.91-2.15l-2.39.39-.05.25c.18-.03.33-.05.45-.05.24 0 .43.1.59.3.25.31.59 1.24 1.02 2.8-.34.44-.58.73-.7.87-.21.22-.38.36-.52.43-.1.05-.22.08-.35.08-.1 0-.26-.05-.49-.16a1 1 0 0 0-.42-.11c-.23 0-.42.07-.57.22-.15.14-.23.33-.23.55q0 .315.21.51c.14.13.33.2.56.2s.44-.05.64-.14.45-.29.75-.59.72-.78 1.25-1.43q.315.915.54 1.35"];
})), bP, xP = o((() => {
	bP = ["M3 14a1 1 0 0 1-1-1V1a1 1 0 0 0-2 0v12a3 3 0 0 0 3 3h2.872l-2.293 2.293a1 1 0 1 0 1.414 1.414l4.215-4.215q.141-.142.22-.316V18.9a1.1 1.1 0 0 0 1.1 1.1H18.9a1.1 1.1 0 0 0 1.1-1.1v-8.371a1.1 1.1 0 0 0-1.1-1.1h-8.371a1.1 1.1 0 0 0-1.1 1.1v3.723a1.1 1.1 0 0 0-.221-.316L4.993 9.722a1 1 0 1 0-1.414 1.415L6.443 14zm8.429 4v-6.571H18v6.57z"];
})), SP, CP = o((() => {
	SP = ["M19 0H1C.45 0 0 .45 0 1v13c0 .55.45 1 1 1h5.67l-.5 3H5c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1h-1.17l-.5-3H19c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 13H2V2h16z"];
})), wP, TP = o((() => {
	wP = ["M1 0h5a1 1 0 0 1 0 2H2v4a1 1 0 0 1-2 0V1a1 1 0 0 1 1-1M0 19v-5a1 1 0 1 1 2 0v4h4a1 1 0 0 1 0 2H1a1 1 0 0 1-1-1m19 1h-5a1 1 0 0 1 0-2h4v-4a1 1 0 0 1 2 0v5a1 1 0 0 1-1 1m1-19v5a1 1 0 0 1-2 0V2h-4a1 1 0 1 1 0-2h5a1 1 0 0 1 1 1M5 6a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1zm2 7h6V7H7z"];
})), EP, DP = o((() => {
	EP = ["M4 2a1 1 0 0 1 .117 1.993L4 4v5a2 2 0 0 0 1.85 1.995L6 11a2 2 0 0 0 1.995-1.85L8 9V4a1 1 0 0 1-.117-1.993L8 2h1a1 1 0 0 1 .993.883L10 3v6a4 4 0 0 1-3 3.874V13a3 3 0 0 0 3 3 4 4 0 0 0 3.995-3.8L14 12V8.792a2.5 2.5 0 1 1 2 0V12a6 6 0 0 1-6 6 5 5 0 0 1-4.995-4.783L5 13v-.126A4 4 0 0 1 2.005 9.2L2 9V3a1 1 0 0 1 .883-.993L3 2z"];
})), OP, kP = o((() => {
	OP = ["M19 10v5h-2v-4h-6v4H9v-4H3v4H1v-5a1 1 0 0 1 1-1h7V5h2v4h7a1 1 0 0 1 1 1M1 16h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1m16 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1m-8 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1M9 0h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1"];
})), AP, jP = o((() => {
	AP = ["m20 3.02-20 7 20 7-5-7z"];
})), MP, NP = o((() => {
	MP = ["m20 10.02-20-7 5 7-5 7z"];
})), PP, FP = o((() => {
	PP = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0M2 10c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L3.69 14.9A7.9 7.9 0 0 1 2 10m8 8c-1.85 0-3.55-.63-4.9-1.69L16.31 5.1A7.9 7.9 0 0 1 18 10c0 4.42-3.58 8-8 8"];
})), IP, LP = o((() => {
	IP = ["M11.25 6.25a1.25 1.25 0 1 1-2.5 0 1.25 1.25 0 0 1 2.5 0M6 9c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1zm4 6a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5"];
})), RP, zP = o((() => {
	RP = ["M11.98 0h-8c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V6zm4 18h-11V2h6v5h5z"];
})), BP, VP = o((() => {
	BP = ["M3 0h8l6 6v4.759A3 3 0 0 0 15 10V7h-5V2H4v16h2.758q.057.064.118.124L8.752 20H3c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1m9 12c.55 0 1 .45 1 1 0 .28-.11.53-.3.71L10.41 16l2.3 2.29a1.003 1.003 0 0 1-1.42 1.42l-3-3A1 1 0 0 1 8 16c0-.28.11-.53.29-.71l3-3c.18-.18.43-.29.71-.29m3.71.29 3 3c.18.18.29.43.29.71s-.11.53-.29.71l-3 3A1.003 1.003 0 0 1 14 19c0-.28.11-.53.3-.71L16.59 16l-2.3-2.29a1.003 1.003 0 0 1 1.42-1.42"];
})), HP, UP = o((() => {
	HP = ["M3 0h8l6 6v3.555A4 4 0 0 0 15 9V7h-5V2H4v16h5v1.5q0 .247.052.5H3c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1m13.965 15.005h1.465c.275 0 .535.22.535.495v4c0 .275-.26.505-.535.505h-6.965c-.275 0-.465-.23-.465-.505v-4c0-.275.19-.495.465-.495h1.5V13a2 2 0 1 1 4 0zm-3-2v2.005h2v-2.005c0-.55-.45-1-1-1s-1 .45-1 1"];
})), WP, GP = o((() => {
	WP = ["M8 15c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1h2.59L1.3 16.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L8 12.41zm5-15H5c-.55 0-1 .45-1 1v6h2V2h6v5h5v11H6v-.76L4.04 19.2c.1.45.48.8.96.8h13c.55 0 1-.45 1-1V6z"];
})), KP, qP = o((() => {
	KP = ["M14.09 10.09c-.31.31-.67.57-1.09.72V18H2V2h6v5h1.18c.15-.42.39-.8.7-1.11v-.01l2.45-2.45c-.42-.29-.78-.65-1.01-1.11L9 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V9.24l-.88.88zM19 0h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L11.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 3.41V6c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), JP, YP = o((() => {
	JP = ["M15.57 11.19c-.27-.51-.63-.93-1.07-1.26s-.95-.6-1.51-.79c-.56-.2-1.14-.36-1.72-.5-.6-.14-1.19-.26-1.75-.38-.57-.13-1.07-.27-1.51-.44s-.8-.38-1.07-.63-.41-.59-.41-1c0-.33.09-.6.28-.81s.42-.36.69-.47.57-.18.88-.22.58-.06.8-.06c.71 0 1.35.14 1.9.41s.91.81 1.06 1.62h3.36q-.135-1.26-.69-2.16c-.37-.6-.83-1.08-1.38-1.45q-.84-.555-1.86-.81c-.19-.05-.38-.07-.57-.1V1c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v1.1c-.22.03-.43.05-.66.1-.73.13-1.39.37-1.98.71-.6.34-1.09.8-1.47 1.35-.39.56-.58 1.25-.58 2.08 0 .76.13 1.41.4 1.93.26.52.62.95 1.06 1.28s.94.6 1.5.79c.55.2 1.13.36 1.74.5.58.14 1.16.26 1.72.38s1.07.26 1.51.43.8.39 1.09.66c.28.27.43.63.45 1.06s-.08.78-.3 1.04-.49.47-.83.6c-.34.14-.7.23-1.09.28s-.73.07-1.03.07c-.87 0-1.61-.2-2.23-.59s-.98-1.08-1.07-2.06H3c.02.9.19 1.68.52 2.34q.495.99 1.35 1.65c.57.44 1.25.77 2.03.98.35.1.71.16 1.08.21V19c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1.13c.25-.04.5-.07.76-.13.77-.18 1.47-.46 2.1-.85s1.14-.9 1.54-1.53.59-1.39.59-2.29c.01-.75-.13-1.37-.4-1.88"];
})), XP, ZP = o((() => {
	XP = ["M10 6a4 4 0 1 1 0 8 4 4 0 0 1 0-8"];
})), QP, $P = o((() => {
	QP = ["M8 4c-.24 0-.46.1-.63.24l-.01-.01-6 5 .01.01c-.22.19-.37.45-.37.76s.15.57.37.76l-.01.01 6 5 .01-.01c.17.14.39.24.63.24.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m11 6c0-.31-.15-.57-.37-.76l.01-.01-6-5-.01.01C12.46 4.1 12.24 4 12 4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1 .24 0 .46-.1.63-.24l.01.01 6-5-.01-.01c.22-.19.37-.45.37-.76"];
})), eF, tF = o((() => {
	eF = ["M5 9h10c.55 0 1-.45 1-1 0-.24-.1-.46-.24-.63l.01-.01-5-6-.01.01C10.57 1.15 10.31 1 10 1s-.57.15-.76.37l-.01-.01-5 6 .01.01C4.1 7.54 4 7.76 4 8c0 .55.45 1 1 1m10 2H5c-.55 0-1 .45-1 1 0 .24.1.46.24.63l-.01.01 5 6 .01-.01c.19.22.45.37.76.37s.57-.15.76-.37l.01.01 5-6-.01-.01c.14-.17.24-.39.24-.63 0-.55-.45-1-1-1"];
})), nF, rF = o((() => {
	nF = ["M9.29 10.71c.18.18.43.29.71.29s.53-.11.71-.29l6-6a1.003 1.003 0 0 0-1.42-1.42L10 8.59l-5.29-5.3a1.003 1.003 0 0 0-1.42 1.42zM16 9c-.28 0-.53.11-.71.29L10 14.59l-5.29-5.3a1.003 1.003 0 0 0-1.42 1.42l6 6c.18.18.43.29.71.29s.53-.11.71-.29l6-6A1.003 1.003 0 0 0 16 9"];
})), iF, aF = o((() => {
	iF = ["m5.41 10 5.29-5.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-6 6c-.18.18-.29.43-.29.71s.11.53.29.71l6 6a1.003 1.003 0 0 0 1.42-1.42zm6 0 5.29-5.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-6 6c-.18.18-.29.43-.29.71s.11.53.29.71l6 6a1.003 1.003 0 0 0 1.42-1.42z"];
})), oF, sF = o((() => {
	oF = ["M11 10c0-.28-.11-.53-.29-.71l-6-6a1.003 1.003 0 0 0-1.42 1.42L8.59 10 3.3 15.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l6-6c.18-.18.29-.43.29-.71m5.71-.71-6-6a1.003 1.003 0 0 0-1.42 1.42l5.3 5.29-5.29 5.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l6-6c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), cF, lF = o((() => {
	cF = ["M4 11c.28 0 .53-.11.71-.29L10 5.41l5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-6-6A1 1 0 0 0 10 3c-.28 0-.53.11-.71.29l-6 6A1.003 1.003 0 0 0 4 11m6.71-1.71A1 1 0 0 0 10 9c-.28 0-.53.11-.71.29l-6 6a1.003 1.003 0 0 0 1.42 1.42l5.29-5.3 5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), uF, dF = o((() => {
	uF = ["M16 10c0 3.31-2.69 6-6 6s-6-2.69-6-6 2.69-6 6-6V0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10zm-.09-1h4.04C19.48 4.28 15.72.52 11 .05V4.1A5.98 5.98 0 0 1 15.91 9"];
})), fF, pF = o((() => {
	fF = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m4.71 11.71-4 4c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-4-4a1.003 1.003 0 0 1 1.42-1.42L9 12.59V5c0-.55.45-1 1-1s1 .45 1 1v7.59l2.29-2.29c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71"];
})), mF, hF = o((() => {
	mF = ["M7.5 11c-.83 0-1.5.67-1.5 1.5S6.67 14 7.5 14 9 13.33 9 12.5 8.33 11 7.5 11m-5-5C1.67 6 1 6.67 1 7.5S1.67 9 2.5 9 4 8.33 4 7.5 3.33 6 2.5 6m0 5c-.83 0-1.5.67-1.5 1.5S1.67 14 2.5 14 4 13.33 4 12.5 3.33 11 2.5 11m15-2c.83 0 1.5-.67 1.5-1.5S18.33 6 17.5 6 16 6.67 16 7.5 16.67 9 17.5 9m-5 2c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5m5 0c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5m-10-5C6.67 6 6 6.67 6 7.5S6.67 9 7.5 9 9 8.33 9 7.5 8.33 6 7.5 6m5 0c-.83 0-1.5.67-1.5 1.5S11.67 9 12.5 9 14 8.33 14 7.5 13.33 6 12.5 6"];
})), gF, _F = o((() => {
	gF = ["M7.5 6C6.67 6 6 6.67 6 7.5S6.67 9 7.5 9 9 8.33 9 7.5 8.33 6 7.5 6m0 5c-.83 0-1.5.67-1.5 1.5S6.67 14 7.5 14 9 13.33 9 12.5 8.33 11 7.5 11m0 5c-.83 0-1.5.67-1.5 1.5S6.67 19 7.5 19 9 18.33 9 17.5 8.33 16 7.5 16m5-12c.83 0 1.5-.67 1.5-1.5S13.33 1 12.5 1 11 1.67 11 2.5 11.67 4 12.5 4m-5-3C6.67 1 6 1.67 6 2.5S6.67 4 7.5 4 9 3.33 9 2.5 8.33 1 7.5 1m5 10c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5m0 5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5m0-10c-.83 0-1.5.67-1.5 1.5S11.67 9 12.5 9 14 8.33 14 7.5 13.33 6 12.5 6"];
})), vF, yF = o((() => {
	vF = ["M17.7 12.7c0-.1 0-.2-.1-.3l-2-7c-.1-.3-.3-.6-.6-.7L1.8 0l-.6.5L7.7 7c.3-.2.6-.3 1-.3 1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2c0-.4.1-.7.3-1L.5 1.2l-.5.6L4.7 15c.1.3.4.5.7.6l7 2c.1 0 .2.1.3.1.3 0 .5-.1.7-.3l4-4c.2-.2.3-.5.3-.7m1 1c-.3 0-.5.1-.7.3l-4 4c-.2.2-.3.4-.3.7 0 .5.4 1 1 1 .3 0 .5-.1.7-.3l4-4c.2-.2.3-.4.3-.7 0-.6-.5-1-1-1"];
})), bF, xF = o((() => {
	bF = ["M9 0a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zM8 2H2v16h6zm2 7h6.59L14.3 6.71A.97.97 0 0 1 14 6a1.003 1.003 0 0 1 1.71-.71l4 4c.18.18.29.43.29.71s-.11.53-.29.71l-4 4a1.003 1.003 0 0 1-1.42-1.42l2.3-2.29H10z"];
})), SF, CF = o((() => {
	SF = ["M1 0h8a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1m9 9h6.59L14.3 6.71A.97.97 0 0 1 14 6a1.003 1.003 0 0 1 1.71-.71l4 4c.18.18.29.43.29.71s-.11.53-.29.71l-4 4a1.003 1.003 0 0 1-1.42-1.42l2.3-2.29H10z"];
})), wF, TF = o((() => {
	wF = ["M19 0a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zm-1 2h-6v16h6zm-8 7H3.41L5.7 6.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C.11 9.47 0 9.72 0 10s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L3.41 11H10z"];
})), EF, DF = o((() => {
	EF = ["M11 0h8a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1m-1 9H3.41L5.7 6.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C.11 9.47 0 9.72 0 10s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L3.41 11H10z"];
})), OF, kF = o((() => {
	OF = ["M20.01 7.7c0-.63-.5-1.14-1.1-1.14h-1.32l-.95-2.57c-.24-.64-.95-1.31-1.59-1.5 0 0-1.65-.49-5.05-.49s-5.04.49-5.04.49c-.63.19-1.35.86-1.59 1.5l-.95 2.57H1.1C.5 6.56 0 7.07 0 7.7s.5 1.14 1.1 1.14h.47l-.34.91c-.24.64-.43 1.72-.43 2.4v5.39c0 .8.63 1.45 1.4 1.45s1.4-.65 1.4-1.45v-.83h12.8v.83c0 .8.63 1.45 1.4 1.45s1.4-.65 1.4-1.45v-5.39c0-.68-.19-1.77-.43-2.4l-.34-.91h.47c.61 0 1.11-.51 1.11-1.14m-16.47.34 1.12-3.16c.08-.22.32-.39.54-.39h9.6c.22 0 .46.17.54.39l1.12 3.16c.08.21-.04.39-.26.39H3.8c-.22-.01-.34-.18-.26-.39m.96 4.94c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.68 1.5 1.5c0 .83-.67 1.5-1.5 1.5m11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5"];
})), AF, jF = o((() => {
	AF = ["M14.128.143c.578-.597 1.786.804 2.45 1.95a1 1 0 0 1 1.309 1.365c1.113.668 2.552 1.815 1.985 2.4-.578.596-1.788-.806-2.452-1.953a1 1 0 0 1-.683.059.86.86 0 0 1-.13.626c-3.476 5.227-3.476 5.593 0 10.82.126.19.166.413.13.625a1 1 0 0 1 .722.076c.668-1.113 1.814-2.55 2.399-1.983.595.578-.806 1.786-1.953 2.45A.996.996 0 0 1 17 18a1 1 0 0 1-.459-.113c-.668 1.113-1.814 2.55-2.398 1.985-.597-.578.804-1.788 1.95-2.452a1 1 0 0 1-.058-.684.86.86 0 0 1-.625-.13c-5.227-3.476-5.593-3.475-10.82 0a.86.86 0 0 1-.626.13Q4 16.863 4 17c0 .165-.042.32-.113.458 1.113.668 2.552 1.815 1.985 2.4-.578.596-1.788-.806-2.452-1.953a1 1 0 0 1-1.309-1.365c-1.113-.668-2.55-1.813-1.983-2.397.578-.597 1.786.804 2.45 1.95a1 1 0 0 1 .685-.058.86.86 0 0 1 .13-.625c3.476-5.227 3.476-5.593 0-10.82a.86.86 0 0 1-.13-.627 1 1 0 0 1-.722-.076C1.873 5 .727 6.437.143 5.872c-.597-.578.804-1.788 1.95-2.452a1 1 0 0 1 1.365-1.309C4.126.998 5.273-.439 5.858.128c.595.578-.806 1.786-1.952 2.45a1 1 0 0 1 .057.685.86.86 0 0 1 .627.13c5.227 3.476 5.593 3.476 10.82 0a.86.86 0 0 1 .625-.13 1 1 0 0 1 .077-.723c-1.113-.668-2.55-1.813-1.984-2.397"];
})), MF, NF = o((() => {
	MF = ["M10 0c2.897 0 2 4 1 6v3l9 2.25V12h-9v4l5 1v1h-5.065l-.041 1H12v1H8v-1h1.106l-.042-1H4v-1l5-1v-4H0v-.75L9 9V6c-1-2-1.897-6 1-6"];
})), PF, FF = o((() => {
	PF = ["M15 4H1c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m-1 14H2V6h12zm5-18H5c-.55 0-1 .45-1 1v2h2V2h12v12h-1v2h2c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), IF, LF = o((() => {
	IF = ["m4.59 12.59 2.83 2.83 7.65-7.65-2.83-2.83zM2 18l4.41-1.59-2.81-2.79zM16 2c-.55 0-1.05.22-1.41.59l-1.65 1.65 2.83 2.83 1.65-1.65A2.006 2.006 0 0 0 16 2"];
})), RF, zF = o((() => {
	RF = ["M4 12h12c.55 0 1-.45 1-1 0-.25-.1-.47-.25-.64l.01-.01-6-7-.01.01C10.57 3.14 10.3 3 10 3s-.57.14-.75.36l-.01-.01-6 7 .01.01c-.15.17-.25.39-.25.64 0 .55.45 1 1 1m12 1H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1"];
})), BF, VF = o((() => {
	BF = ["M10 0c5.523 0 10 4.477 10 10s-4.477 10-10 10S0 15.523 0 10 4.477 0 10 0m0 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16m-4 8 .015.215C6.219 12.42 7.925 14 10 14a4 4 0 0 0 3.995-3.8L14 10h2l-.013.238C15.754 13.552 13.163 16 10 16a6 6 0 0 1-5.996-5.775L4 10zm1.5-4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3m5 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3"];
})), HF, UF = o((() => {
	HF = ["M16.943 1.571q-.459.087-.943.086v1.286h2.317V10H20V0h-1.253q-.08.458-.35.771-.255.315-.633.515a2.7 2.7 0 0 1-.821.285M12.833 20q-.612 0-1.242-.29l-.168-.083c-.3-.146-.487-.238-.804-.556v.712H8.55V7h2.07v3.295l-.054 1.485a5.2 5.2 0 0 1 1.206-.797 3.2 3.2 0 0 1 1.35-.308q.828.001 1.476.326.648.308 1.098.906.45.58.684 1.412.234.833.234 1.865 0 1.14-.324 2.046a4.6 4.6 0 0 1-.828 1.503q-.522.615-1.206.941T12.833 20m-.432-1.72q.882 0 1.476-.76.594-.78.594-2.3 0-1.34-.45-2.082t-1.458-.742q-.936 0-1.944.995v4.147q.468.416.918.579.468.163.864.163M2.61 20q-1.17 0-1.89-.706Q0 18.569 0 17.393q0-.707.288-1.25.306-.561.936-.96.648-.397 1.62-.67.99-.271 2.358-.416a3 3 0 0 0-.108-.652 1.3 1.3 0 0 0-.27-.56 1.1 1.1 0 0 0-.486-.381 1.8 1.8 0 0 0-.756-.145q-.648 0-1.278.254a9 9 0 0 0-1.206.615l-.756-1.394a9 9 0 0 1 1.656-.815 5.6 5.6 0 0 1 1.98-.344q1.656 0 2.466.996.828.978.828 2.843v5.268h-2.07v-.87a5 5 0 0 1-1.134.744A3.1 3.1 0 0 1 2.61 20m.666-1.63q.54 0 .972-.253.45-.254.954-.724V15.4q-.9.108-1.512.29-.612.181-.99.416-.378.218-.54.507a1.24 1.24 0 0 0-.162.616q0 .597.36.869.36.27.918.271"];
})), WF, GF = o((() => {
	WF = ["M19.83 9.38 18.81 7.6V5.62c0-.45-.23-.85-.61-1.08l-1.71-1-1.02-1.76a1.25 1.25 0 0 0-1.08-.61h-2.03l-1.74-1c-.38-.23-.87-.23-1.25 0l-1.74 1H5.65c-.44 0-.85.23-1.08.61L3.58 3.5l-1.8 1.04c-.38.24-.62.64-.62 1.08v2.06L.17 9.4c-.11.19-.17.4-.17.61s.06.42.17.61l.99 1.72v2.06c0 .45.23.85.61 1.08l1.78 1.02.99 1.72c.23.38.63.61 1.08.61h1.99l1.74 1c.19.11.41.17.62.17s.42-.06.61-.17l1.74-1h2.03c.44 0 .85-.23 1.08-.61l1.02-1.76 1.71-1c.38-.23.61-.64.61-1.08v-1.97l1.02-1.78c.27-.38.27-.85.04-1.25m-5.08-.71-5.01 5.01c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-3.01-3.01a1.003 1.003 0 0 1 1.42-1.42l2.3 2.3 4.31-4.3a1.003 1.003 0 0 1 1.71.71c0 .28-.12.53-.3.71"];
})), KF, qF = o((() => {
	KF = ["M8.4 0H.6C.27 0 0 .27 0 .6v5.25c0 .33.313.579.643.579h3.354l2.177 2.397A.602.602 0 0 0 7.2 8.4V6.429h1.2c.33 0 .6-.27.6-.6V.6c0-.33-.27-.6-.6-.6m8.482 16.777c1.185.482 2.52 1.025 2.846 1.77.363.827.264 1.35.247 1.44l-.002.013H6.034s-.166-.543.236-1.462c.326-.744 1.662-1.288 2.846-1.77.28-.113.55-.223.797-.332 1.15-.508 1.168-.841 1.19-1.244q.003-.072.01-.148 0-.045.004-.092.004-.045.004-.091a3.9 3.9 0 0 1-1.068-1.577l-.009-.008-.004-.013q-.004-.008-.005-.014a4 4 0 0 1-.13-.429c-.307-.052-.482-.376-.553-.683-.06-.122-.2-.42-.175-.752.044-.447.228-.648.438-.727v-.07c0-.56.044-1.357.149-1.883.018-.148.053-.289.096-.437a3.25 3.25 0 0 1 1.121-1.629c.552-.42 1.33-.639 2.023-.639.691 0 1.47.228 2.031.64a3.2 3.2 0 0 1 1.217 2.065c.096.526.149 1.331.149 1.883v.079c.192.078.368.28.411.718.027.341-.105.639-.175.761-.061.298-.236.622-.534.683a3.4 3.4 0 0 1-.149.464c-.236.622-.595 1.165-1.042 1.559 0 .07 0 .14.01.201q.007.09.009.176c.013.39.025.72 1.155 1.216.247.109.517.219.796.332M19.973 20"];
})), JF, YF = o((() => {
	JF = ["M0 4.01v11.91l6.27-6.27zm18.91-1.03H1.09L10 10.97zm-5.18 6.66L20 15.92V4.01zm-3.23 2.9c-.13.12-.31.19-.5.19s-.37-.07-.5-.19l-2.11-1.89-6.33 6.33h17.88l-6.33-6.33z"];
})), XF, ZF = o((() => {
	XF = ["M4 7h12a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2m0 4h12a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2"];
})), QF, $F = o((() => {
	QF = ["M18.71 8.43c.39-.4.39-1.05 0-1.45l-5.53-5.72a.967.967 0 0 0-1.4 0L1.29 12.1c-.39.4-.39 1.05 0 1.45l4.25 4.39 2.13 2.05h9.27c.02 0 .03.01.05.01.55 0 1-.45 1-1s-.45-1-1-1H9.46l.05-.05h.01l.81-.84zM7.52 17.94l-4.95-5.12 4.46-4.61 4.95 5.12z"];
})), eI, tI = o((() => {
	eI = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m1 16H9v-2h2zm0-3H9V4h2z"];
})), nI, rI = o((() => {
	nI = ["M8.89 4.47c.56-.31 1.23-.47 2.03-.47.44 0 .85.07 1.25.22.4.14.76.35 1.07.6.17.14.33.3.47.47l2.32-2.32c-.16-.15-.3-.32-.47-.46-.62-.49-1.33-.87-2.12-1.13-.8-.25-1.64-.38-2.52-.38q-1.86 0-3.33.66C6.6 2.1 5.77 2.71 5.1 3.48c-.68.78-1.2 1.68-1.56 2.72-.09.26-.13.54-.2.8H2c-.55 0-1 .45-1 1s.45 1 1 1h1.04c-.01.2-.04.38-.04.58 0 .15.03.28.03.42H2c-.55 0-1 .45-1 1s.45 1 1 1h1.31c.07.3.13.6.23.89.36 1.02.88 1.92 1.56 2.67.68.76 1.51 1.35 2.49 1.79.98.43 2.09.65 3.33.65.99 0 1.9-.15 2.73-.46.83-.3 1.55-.74 2.17-1.32.03-.03.05-.06.08-.09l-2.41-2.15c-.01.01-.02.02-.02.03-.61.67-1.46 1-2.54 1-.8 0-1.47-.16-2.03-.47s-1.01-.72-1.35-1.24c-.28-.38-.47-.83-.63-1.3H12c.55 0 1-.45 1-1s-.45-1-1-1H6.56c0-.14-.02-.28-.02-.42 0-.2.02-.39.03-.58H13c.55 0 1-.45 1-1s-.45-1-1-1H6.94c.15-.46.34-.9.59-1.28.35-.52.8-.94 1.36-1.25M18 11.38v.02z"];
})), iI, aI = o((() => {
	iI = ["m19.16 9.804.6 2A1 1 0 0 1 18.78 13H9a1 1 0 0 1-1-1V9.272a1 1 0 0 1 .139-.506L9.76 6l.94-1.6a1 1 0 0 1 .8-.4H15a1 1 0 0 1 1 1v4h2.18a1 1 0 0 1 .98.804M10 9h4V6h-2.24zM4.25.5l4.739 2.494a.998.998 0 0 1 .383 1.449L9 5 4 2.994 2 10h4l-2.642 2.642a.95.95 0 0 1-.857.27C.952 12.595 0 11.94 0 10l2.658-8.861C2.837.544 3.695.222 4.25.5M3 17a3 3 0 0 1 3-3h11a3 3 0 0 1 0 6H6a3 3 0 0 1-3-3m2 0a1 1 0 0 0 1 1h11a1 1 0 0 0 0-2H6a1 1 0 0 0-1 1"];
})), oI, sI = o((() => {
	oI = ["M2.5 8a2.5 2.5 0 0 0 0 5 2.5 2.5 0 0 0 0-5m10.35 3.15a.495.495 0 1 0-.7.7L13.3 13H5.5c-.28 0-.5.22-.5.5s.22.5.5.5h7.79l-1.15 1.15c-.08.09-.14.21-.14.35a.495.495 0 0 0 .85.35l2-2c.09-.09.15-.21.15-.35s-.06-.26-.15-.35zM17.5 8a2.5 2.5 0 0 0 0 5 2.5 2.5 0 0 0 0-5M7.15 9.85a.495.495 0 1 0 .7-.7L6.71 8h7.79c.28 0 .5-.22.5-.5s-.22-.5-.5-.5H6.71l1.15-1.15c.08-.09.14-.21.14-.35a.495.495 0 0 0-.85-.35l-2 2c-.09.09-.15.21-.15.35s.06.26.15.35z"];
})), cI, lI = o((() => {
	cI = ["M1 3h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1M0 13a1.003 1.003 0 0 0 1.71.71L4 11.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L5.41 10 7.7 7.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L4 8.59l-2.29-2.3A1.003 1.003 0 0 0 .29 7.71L2.59 10 .3 12.29c-.19.18-.3.43-.3.71m18-5h-7c-1.1 0-2 .9-2 2s.9 2 2 2h7c1.1 0 2-.9 2-2s-.9-2-2-2m1 9H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), uI, dI = o((() => {
	uI = ["M4 9c.28 0 .53-.11.71-.29L10 3.41l5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-6-6C10.53 1.11 10.28 1 10 1s-.53.11-.71.29l-6 6A1.003 1.003 0 0 0 4 9m12 2c-.28 0-.53.11-.71.29L10 16.59 4.71 11.3A.97.97 0 0 0 4 11a1.003 1.003 0 0 0-.71 1.71l6 6c.18.18.43.29.71.29s.53-.11.71-.29l6-6A1.003 1.003 0 0 0 16 11"];
})), fI, pI = o((() => {
	fI = ["M10 0c5.523 0 10 4.477 10 10v10H10C4.477 20 0 15.523 0 10S4.477 0 10 0M8 11a1 1 0 0 1 1 1v4.37a.63.63 0 0 0 1.18.307l3.74-6.733A.635.635 0 0 0 13.365 9H12a1 1 0 0 1-1-1V3.63a.63.63 0 0 0-1.18-.306l-3.74 6.732a.635.635 0 0 0 .555.944z"];
})), mI, hI = o((() => {
	mI = ["M5 7c.28 0 .53-.11.71-.29L9 3.41V15c0 .55.45 1 1 1s1-.45 1-1V3.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-5-5C10.53.11 10.28 0 10 0s-.53.11-.71.29l-5 5A1.003 1.003 0 0 0 5 7m14 7c-.55 0-1 .45-1 1v3H2v-3c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1"];
})), gI, _I = o((() => {
	gI = ["M20 9.96v-.08a.8.8 0 0 0-.21-.43c-.55-.69-1.19-1.3-1.85-1.87l-3.93 2.62a3.966 3.966 0 0 1-3.96 3.77c-.47 0-.91-.1-1.33-.24l-2.24 1.49c.52.21 1.05.39 1.6.51 1.21.27 2.43.28 3.64.05 1.11-.21 2.17-.64 3.17-1.18 1.56-.84 2.99-2 4.23-3.3.23-.24.46-.49.67-.75a.87.87 0 0 0 .21-.43zm-.46-5.14c.27-.18.46-.47.46-.82 0-.55-.45-1-1-1-.21 0-.39.08-.54.18l-.01-.02L15 5.46c-.95-.53-1.95-.96-3.01-1.2a9.2 9.2 0 0 0-3.65-.04c-1.11.21-2.17.64-3.17 1.18-1.56.84-2.99 2-4.23 3.3-.23.24-.46.48-.67.75-.27.34-.27.76 0 1.1.64.79 1.39 1.5 2.16 2.15.26.21.52.41.79.61L.44 15.16l.01.02A1 1 0 0 0 0 16c0 .55.45 1 1 1 .21 0 .39-.08.54-.18l.01.02 18-12zm-8.67 3.4c-.25-.12-.53-.2-.83-.2-1.1 0-1.99.89-1.99 1.99 0 .03.02.06.02.09l-1.78 1.19c-.14-.4-.22-.83-.22-1.28 0-2.19 1.78-3.97 3.98-3.97 1.01 0 1.91.38 2.61 1z"];
})), vI, yI = o((() => {
	vI = ["M13.3 8.71c.18.18.43.29.71.29s.53-.11.71-.29l4.99-5a1.003 1.003 0 0 0-1.42-1.42L14 6.58l-2.29-2.29a.96.96 0 0 0-.7-.29 1.003 1.003 0 0 0-.71 1.71zM20 9.96v-.08a.8.8 0 0 0-.21-.44c-.44-.55-.94-1.05-1.46-1.52l-2.2 2.2c-.55.54-1.3.88-2.12.88-.05 0-.09-.01-.14-.01a3.98 3.98 0 0 1-3.86 3.02 4.007 4.007 0 0 1-1.66-7.65A3 3 0 0 1 8.02 5c0-.28.05-.54.12-.8-1.05.22-2.07.64-3.02 1.15-1.57.85-3 2.02-4.24 3.33-.23.25-.46.5-.67.76-.28.35-.28.77 0 1.12.64.8 1.4 1.52 2.17 2.17 1.66 1.41 3.56 2.58 5.66 3.06 1.21.27 2.43.29 3.65.05 1.11-.21 2.18-.65 3.18-1.19 1.57-.85 3-2.02 4.24-3.33.23-.24.46-.49.67-.76.11-.12.18-.27.21-.44V10c.01-.01.01-.03.01-.04m-9.99 2.05c1.03 0 1.87-.79 1.98-1.8l-.09-.09-.01.01-2.1-2.11c-1 .11-1.77.95-1.77 1.98-.01 1.11.89 2.01 1.99 2.01"];
})), bI, xI = o((() => {
	bI = ["M10.01 7.984A2.01 2.01 0 0 0 8.012 9.99c0 1.103.9 2.006 1.998 2.006a2.01 2.01 0 0 0 1.998-2.006c0-1.103-.9-2.006-1.998-2.006M20 9.96v-.08a.83.83 0 0 0-.21-.442c-.64-.802-1.398-1.514-2.168-2.166-1.658-1.404-3.566-2.587-5.664-3.058a9 9 0 0 0-3.656-.05c-1.11.2-2.178.641-3.177 1.183-1.569.852-2.997 2.016-4.246 3.33-.23.25-.46.49-.67.761-.279.351-.279.773 0 1.124.64.802 1.4 1.514 2.169 2.166 1.658 1.404 3.566 2.577 5.664 3.058a9 9 0 0 0 3.656.05c1.11-.21 2.178-.651 3.177-1.193 1.569-.852 2.997-2.016 4.246-3.33.23-.24.46-.49.67-.751A.86.86 0 0 0 20 10.12zM10.01 14a4.003 4.003 0 0 1-3.996-4.01 4.003 4.003 0 0 1 3.996-4.011 4.003 4.003 0 0 1 3.996 4.011 4.003 4.003 0 0 1-3.996 4.011"];
})), SI, CI = o((() => {
	SI = ["M18 3c-.23 0-.42.09-.59.21l-.01-.01L11 8V4c0-.55-.45-1-1-1-.23 0-.42.09-.59.21L9.4 3.2l-8 6 .01.01C1.17 9.4 1 9.67 1 10s.17.6.41.79l-.01.01 8 6 .01-.01c.17.12.36.21.59.21.55 0 1-.45 1-1v-4l6.4 4.8.01-.01c.17.12.36.21.59.21.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), wI, TI = o((() => {
	wI = ["M19 10c0-.33-.17-.6-.41-.79l.01-.01-8-6-.01.01C10.42 3.09 10.23 3 10 3c-.55 0-1 .45-1 1v4L2.6 3.2l-.01.01C2.42 3.09 2.23 3 2 3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1 .23 0 .42-.09.59-.21l.01.01L9 12v4c0 .55.45 1 1 1 .23 0 .42-.09.59-.21l.01.01 8-6-.01-.01c.24-.19.41-.46.41-.79"];
})), EI, DI = o((() => {
	EI = ["M2.5 15a2.5 2.5 0 0 0 0 5 2.5 2.5 0 0 0 0-5m.5-5c-.55 0-1 .45-1 1s.45 1 1 1c2.76 0 5 2.24 5 5 0 .55.45 1 1 1s1-.45 1-1c0-3.87-3.13-7-7-7M3 0c-.55 0-1 .45-1 1s.45 1 1 1c8.28 0 15 6.72 15 15 0 .55.45 1 1 1s1-.45 1-1C20 7.61 12.39 0 3 0m0 5c-.55 0-1 .45-1 1s.45 1 1 1c5.52 0 10 4.48 10 10 0 .55.45 1 1 1s1-.45 1-1C15 10.37 9.63 5 3 5"];
})), OI, kI = o((() => {
	OI = ["M2.5 15a2.5 2.5 0 0 0 0 5 2.5 2.5 0 0 0 0-5M3 2c1.76 0 3.44.31 5.01.87.03-.71.31-1.35.75-1.85C6.96.37 5.03 0 3 0c-.55 0-1 .45-1 1s.45 1 1 1m10.32 4.67a.99.99 0 0 0 1.4 0l4.98-4.98c.19-.17.3-.42.3-.7 0-.55-.45-1-1-1a1 1 0 0 0-.7.29l-4.27 4.27-2.28-2.28a1 1 0 0 0-.7-.29c-.55 0-.99.45-.99 1 0 .28.11.52.29.7zM3 10c-.55 0-1 .45-1 1s.45 1 1 1c2.76 0 5 2.24 5 5 0 .55.45 1 1 1s1-.45 1-1c0-3.87-3.13-7-7-7m13.94-2.69-.82.82-.02-.02c-.2.2-.42.37-.67.51A14.8 14.8 0 0 1 18 17c0 .55.45 1 1 1s1-.45 1-1c0-3.61-1.14-6.94-3.06-9.69M3 5c-.55 0-1 .45-1 1s.45 1 1 1c5.52 0 10 4.48 10 10 0 .55.45 1 1 1s1-.45 1-1C15 10.37 9.63 5 3 5"];
})), AI, jI = o((() => {
	AI = ["M14.724 2.724a.5.5 0 0 0 .61.075l3.98-2.387c.178-.108.381.095.274.274l-2.387 3.98a.5.5 0 0 0 .075.61l.37.37a.5.5 0 0 1 0 .708L15.17 8.83a.5.5 0 0 0-.143.409l.947 8.522a.5.5 0 0 1-.144.409l-.575.575a.5.5 0 0 1-.577.094l-5.389-2.694a.2.2 0 0 0-.289.178v2.868a.5.5 0 0 1-.724.447l-2.934-1.467a.5.5 0 0 1-.267-.546l.404-2.02a.2.2 0 0 0-.055-.18l-.848-.85a.2.2 0 0 0-.181-.054l-2.02.404a.5.5 0 0 1-.546-.266L.362 11.724A.5.5 0 0 1 .809 11h1.914a.2.2 0 0 0 .19-.263L1.097 5.293a.5.5 0 0 1 .12-.511l.612-.612a.5.5 0 0 1 .409-.143l8.522.947a.5.5 0 0 0 .409-.144l2.476-2.476a.5.5 0 0 1 .708 0z"];
})), MI, NI = o((() => {
	MI = ["M19 2h-5v3H6V2H1c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h5v-3h8v3h5c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1M4 17H2v-2h2zm0-3H2v-2h2zm0-3H2V9h2zm0-3H2V6h2zm0-3H2V3h2zm10 8H6V7h8zm4 4h-2v-2h2zm0-3h-2v-2h2zm0-3h-2V9h2zm0-3h-2V6h2zm0-3h-2V3h2z"];
})), PI, FI = o((() => {
	PI = ["M18 1H2a1.003 1.003 0 0 0-.71 1.71L7 8.41V18a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71V8.41l5.71-5.71c.18-.17.29-.42.29-.7 0-.55-.45-1-1-1"];
})), II, LI = o((() => {
	II = ["M15 2c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L5 7.41V16a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71V7.41l4.71-4.71c.18-.17.29-.42.29-.7m4 11c-.28 0-.53.11-.71.29L15 16.59l-1.29-1.29A.97.97 0 0 0 13 15a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 19 13"];
})), RI, zI = o((() => {
	RI = ["M15 2c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L5 7.41V16a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71V7.41l4.71-4.71c.18-.17.29-.42.29-.7m-4 8c0 .55.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1h-7c-.55 0-1 .45-1 1m8 7h-7c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1m0-4h-7c-.55 0-1 .45-1 1s.45 1 1 1h7c.55 0 1-.45 1-1s-.45-1-1-1"];
})), BI, VI = o((() => {
	BI = ["M15 2c0 .28-.11.53-.29.7L10 7.41V13c0 .28-.11.53-.29.71l-3 3A1.003 1.003 0 0 1 5 16V7.41L.29 2.71A1.003 1.003 0 0 1 1 1h13c.55 0 1 .45 1 1m4.707 11.293a1 1 0 0 1 0 1.414l-4 4c-.63.63-1.707.184-1.707-.707v-8c0-.89 1.077-1.337 1.707-.707z"];
})), HI, UI = o((() => {
	HI = ["M15 2c0-.55-.45-1-1-1H1a1.003 1.003 0 0 0-.71 1.71L5 7.41V16a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71V7.41l4.71-4.71c.18-.17.29-.42.29-.7m2.91 13.5 1.79-1.79c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-1.79 1.79-1.79-1.79a1.003 1.003 0 0 0-1.42 1.42l1.79 1.79-1.79 1.79a1.003 1.003 0 0 0 1.42 1.42l1.79-1.79 1.79 1.79a1.003 1.003 0 0 0 1.42-1.42z"];
})), WI, GI = o((() => {
	WI = ["M20 2c0-.55-.45-1-1-1H6a1.003 1.003 0 0 0-.71 1.71L10 7.41V16a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71V7.41l4.71-4.71c.18-.17.29-.42.29-.7M4.71 10.29A1 1 0 0 0 4 10c-.28 0-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L3 13.41V19c0 .55.45 1 1 1s1-.45 1-1v-5.59l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), KI, qI = o((() => {
	KI = ["M20 2c0-.55-.45-1-1-1H6a1.003 1.003 0 0 0-.71 1.71L10 7.41V16a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71V7.41l4.71-4.71c.18-.17.29-.42.29-.7M4.71 19.71c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-3-3a1.003 1.003 0 0 1 1.42-1.42L3 16.59V11c0-.55.45-1 1-1s1 .45 1 1v5.59l1.29-1.29c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71z"];
})), JI, YI = o((() => {
	JI = ["M3 3c-.55 0-1 .45-1 1v15c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1m0-3c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m2 4.08v8.28c3.01-2.41 8.67 2.64 13 0V4.08C13.61 7.14 8.01 1 5 4.08"];
})), XI, ZI = o((() => {
	XI = ["M11.622 0q0 2.565 1.472 4.103Q18 7.693 18 12.308q0 5.128-5.887 7.692c2.887-3 2.453-4.23-.49-8C8.5 13.5 9 14.5 9.5 16.5c-1.048 0-2 0-2.5-.5 0 .684 1.197 2.5 1.952 4-3.924-1.026-8.123-7.18-6.651-7.692q1.472-.513 3.434.513Q3.282 3.59 11.622 0"];
})), QI, $I = o((() => {
	QI = ["M4.96 6.37a1.003 1.003 0 0 0 1.42-1.42l-2-2a1.07 1.07 0 0 0-.71-.28 1.003 1.003 0 0 0-.71 1.71zm9.37.3c.28 0 .53-.11.71-.29l2-2a1.003 1.003 0 0 0-1.42-1.42l-2 2a1.003 1.003 0 0 0 .71 1.71M10 5c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1S9 .45 9 1v3c0 .55.45 1 1 1m-5 5c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1m14-1h-3c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1m-9-3c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4m0 6c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2m5.04 1.63a1.003 1.003 0 0 0-1.42 1.42l2 2a1.003 1.003 0 0 0 1.42-1.42zM10 15c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1s1-.45 1-1v-3c0-.55-.45-1-1-1m-4.33-1.67c-.28 0-.53.11-.71.29l-2 2a1.003 1.003 0 0 0 1.42 1.42l2-2a1.003 1.003 0 0 0-.71-1.71"];
})), eL, tL = o((() => {
	eL = ["M1 6.648q.514 0 1-.085t.871-.284q.4-.199.672-.512.285-.312.371-.767h1.329v9.947H3.457v-7.02H1zm13.965-1.635q1.032 0 1.677.478.66.465 1.018 1.204.371.724.495 1.6.137.875.137 1.696 0 .82-.137 1.696a5.2 5.2 0 0 1-.495 1.614 3.2 3.2 0 0 1-1.018 1.203q-.646.465-1.677.465-1.03 0-1.691-.465-.646-.479-1.018-1.203a5.7 5.7 0 0 1-.495-1.614 12 12 0 0 1-.123-1.696q0-.821.123-1.696a5.5 5.5 0 0 1 .495-1.6 3.26 3.26 0 0 1 1.018-1.204q.66-.478 1.691-.478m0 8.657q.509 0 .853-.287.343-.3.536-.794a4.6 4.6 0 0 0 .288-1.176q.084-.67.083-1.422 0-.753-.083-1.409a4.6 4.6 0 0 0-.288-1.176q-.193-.506-.536-.793-.345-.3-.853-.301-.522 0-.866.3-.33.288-.537.794-.193.506-.274 1.176-.083.657-.083 1.409 0 .751.082 1.422.083.671.275 1.176.207.493.537.794.344.287.866.287m-5.104-.588H7.875V15h1.986z"];
})), nL, rL = o((() => {
	nL = ["M14 1h-3v5h3zm5.71 2.29-3-3A1 1 0 0 0 16 0h-1v7H5V0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V4c0-.28-.11-.53-.29-.71M17 19H3v-8c0-.55.45-1 1-1h12c.55 0 1 .45 1 1z"];
})), iL, aL = o((() => {
	iL = ["M14.425 7.953a4 4 0 0 1 .562 2.045 4 4 0 0 1-.583 2.08L18 15.671V12.98c0-.248.097-.496.29-.689a1.035 1.035 0 0 1 1.426 0 .94.94 0 0 1 .283.696l-.001 5.049a.96.96 0 0 1-.276.69.96.96 0 0 1-.69.273h-5.059a.97.97 0 0 1-.689-.289 1.026 1.026 0 0 1 0-1.417.97.97 0 0 1 .69-.29h2.702l-3.634-3.573a3.998 3.998 0 0 1-5.924-2.431H1a1 1 0 0 1 0-2h6.12a3.998 3.998 0 0 1 5.96-2.409L16.665 3l-2.694-.001a.97.97 0 0 1-.689-.29 1.035 1.035 0 0 1 0-1.425.94.94 0 0 1 .696-.283l5.05.001a.96.96 0 0 1 .69.276.95.95 0 0 1 .272.69l.001 5.052a.97.97 0 0 1-.29.689 1.03 1.03 0 0 1-1.419 0 .97.97 0 0 1-.29-.69V4.323z"];
})), oL, sL = o((() => {
	oL = ["M12 9.919a4 4 0 0 1 4-3.92c2.21 0 4 1.79 4 3.997a4 4 0 0 1-4 3.996 4 4 0 0 1-4-3.916.97.97 0 0 1-.28.612L7.685 14.71a.96.96 0 0 1-.686.285c-.536 0-.994-.461-.994-.997 0-.273.107-.528.283-.704l2.379-2.302H.98c-.537 0-.976-.46-.976-.996s.44-.992.976-.992h7.676L6.287 6.687a.96.96 0 0 1-.283-.686c0-.536.458-.996.994-.996.274 0 .51.1.686.285l4.027 4.024c.159.158.27.365.29.605"];
})), cL, lL = o((() => {
	cL = ["M5.125 10.997H.976C.439 10.997 0 10.537 0 10s.44-.993.976-.993h4.148a4.002 4.002 0 0 1 7.752 0h3.776L14.293 6.69a.96.96 0 0 1-.285-.687c0-.537.46-1.001.996-1.001a.96.96 0 0 1 .698.3l4.005 4.015c.176.176.293.41.293.683a.97.97 0 0 1-.283.693L15.702 14.7a1 1 0 0 1-.698.297c-.537 0-.996-.453-.996-.99 0-.273.107-.517.283-.692l2.371-2.318h-3.787a4.002 4.002 0 0 1-7.75 0"];
})), uL, dL = o((() => {
	uL = ["M6.13 9.004A4.005 4.005 0 0 1 10.012 6c1.87 0 3.44 1.278 3.881 3.005h2.768l-2.354-2.317a.97.97 0 0 1-.283-.691c0-.536.462-.995 1-.995.273 0 .517.107.693.283l4 4.041a.97.97 0 0 1 .284.692.96.96 0 0 1-.293.682l-3.991 3.997a.94.94 0 0 1-.694.292c-.537 0-1-.46-1-.997a.97.97 0 0 1 .284-.692l2.345-2.29h-2.765a4.005 4.005 0 0 1-3.875 2.981 4.005 4.005 0 0 1-3.874-2.981H3.349l2.376 2.308a.97.97 0 0 1 .283.691 1 1 0 0 1-.994.983 1 1 0 0 1-.713-.291L.293 10.699A.96.96 0 0 1 0 10.017a.97.97 0 0 1 .283-.692l4.03-4.037a1 1 0 0 1 .701-.283c.537 0 .994.464.994 1a.97.97 0 0 1-.283.691L3.34 9.004z"];
})), fL, pL = o((() => {
	fL = ["M13.04 13.424c-.6.36-1.302.568-2.052.568a4 4 0 0 1-3.868-2.999H3.342l2.372 2.31c.176.176.283.42.283.694 0 .537-.452.998-.988.998a.94.94 0 0 1-.691-.289L.292 10.683A.96.96 0 0 1 0 9.999c0-.274.107-.518.283-.694l4.035-4.04a.97.97 0 0 1 .691-.288c.536 0 .988.47.988 1.007a.98.98 0 0 1-.283.694L3.332 8.984h3.786a4 4 0 0 1 3.87-3.006c.771 0 1.492.22 2.102.599l3.565-3.57-2.538-.003a.97.97 0 0 1-.69-.29c-.38-.38-.38-1.052-.002-1.431A.94.94 0 0 1 14.122 1l4.896.005a.96.96 0 0 1 .69.277c.193.193.27.442.27.69l.005 4.9a.97.97 0 0 1-.289.69 1.023 1.023 0 0 1-1.416 0 .98.98 0 0 1-.29-.691l-.003-2.54-3.554 3.62c.351.596.553 1.291.553 2.034 0 .763-.213 1.477-.583 2.084l3.595 3.595.003-2.54c0-.249.097-.497.29-.69.38-.38 1.05-.381 1.429-.002a.94.94 0 0 1 .282.697l-.005 4.9a.93.93 0 0 1-.277.675.97.97 0 0 1-.69.291L13.974 19a.97.97 0 0 1-.69-.29 1.03 1.03 0 0 1 .002-1.42.97.97 0 0 1 .69-.29l2.696-.003z"];
})), mL, hL = o((() => {
	mL = ["M17.5 7.93a2.5 2.5 0 0 0-2.45 2h-2.3l-4.01-4-.75.75 3.26 3.25h-6.3a2.5 2.5 0 1 0 0 1h6.3l-3.26 3.25.75.75 4.01-4h2.3a2.5 2.5 0 1 0 2.45-3"];
})), gL, _L = o((() => {
	gL = ["M0 17c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V7H0zM19 4H9.41l-1.7-1.71A1 1 0 0 0 7 2H1c-.55 0-1 .45-1 1v3h20V5c0-.55-.45-1-1-1"];
})), vL, yL = o((() => {
	vL = ["M12.994 7c0 1.655 1.344 3 2.998 3a3 3 0 0 0 2.999-3H20v10c0 .55-.45 1-1 1H1.01c-.55 0-1-.45-1-1V7zM10.76 6H0V3c0-.55.45-1 1-1h3.998c.28 0 .53.11.71.29L7.415 4h2.579c0 .768.29 1.469.765 2m8.23-3c.55 0 1 .45 1 1s-.45 1-1 1h-1.998v2c0 .55-.45 1-1 1s-1-.45-1-1V5h-1.998c-.55 0-1-.45-1-1s.45-1 1-1h1.999V1c0-.55.45-1 .999-1 .55 0 1 .45 1 1v2z"];
})), bL, xL = o((() => {
	bL = ["M20 9c0-.55-.45-1-1-1H5c-.43 0-.79.27-.93.65h-.01l-3 8h.01c-.04.11-.07.23-.07.35 0 .55.45 1 1 1h14c.43 0 .79-.27.93-.65h.01l3-8h-.01c.04-.11.07-.23.07-.35M3.07 7.63C3.22 7.26 3.58 7 4 7h14V5c0-.55-.45-1-1-1H8.41l-1.7-1.71A1 1 0 0 0 6 2H1c-.55 0-1 .45-1 1v12.31z"];
})), SL, CL = o((() => {
	SL = ["M11 4H9.41l-1.7-1.71A1 1 0 0 0 7 2H1c-.55 0-1 .45-1 1v3h11.78C11.3 5.47 11 4.77 11 4m8-1h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L12.3 9.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 6.41V9c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1m-2.46 7.7-1.42 1.42a2.996 2.996 0 1 1-4.24-4.24l.88-.88H0v10c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-5.18c-.31.11-.65.18-1 .18-1.02 0-1.92-.52-2.46-1.3"];
})), wL, TL = o((() => {
	wL = ["M3.07 7.63C3.22 7.26 3.58 7 4 7h7.76l.54-.54A2.97 2.97 0 0 1 11 4H8.41l-1.7-1.71A1 1 0 0 0 6 2H1c-.55 0-1 .45-1 1v12.31zm13.47 3.07-1.42 1.42A2.996 2.996 0 0 1 10 10c0-.77.3-1.47.78-2H5c-.43 0-.79.27-.93.65h-.01l-3 8h.01c-.04.11-.07.23-.07.35 0 .55.45 1 1 1h14c.43 0 .79-.27.93-.65h.01l2.01-5.36c-1-.01-1.88-.52-2.41-1.29M19 3h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L12.3 9.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 6.41V9c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1"];
})), EL, DL = o((() => {
	EL = ["M11.54 15.92c-1.48-.65-1.28-1.05-1.33-1.59-.01-.07-.01-.15-.01-.23.51-.45.92-1.07 1.19-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.34-.07.54-.44.61-.78.08-.14.23-.48.2-.87-.05-.5-.25-.73-.47-.82v-.09c0-.63-.06-1.55-.17-2.15-.02-.17-.06-.33-.11-.5a3.7 3.7 0 0 0-1.29-1.86C9.69 4.25 8.8 4 8.01 4c-.8 0-1.69.25-2.32.73-.61.47-1.06 1.13-1.28 1.86-.05.17-.09.33-.11.5-.12.6-.18 1.51-.18 2.14v.08c-.23.09-.44.32-.49.83-.04.39.12.73.2.87.08.35.28.72.63.78q.06.255.15.48c0 .01.01.02.01.03l.01.01c.27.72.7 1.35 1.22 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.38 1.59S.75 17.26.3 18.31C-.16 19.38.02 20 .02 20h15.95s.18-.62-.27-1.67c-.46-1.06-2.68-1.75-4.16-2.41m8.15-12.63-3-3a.96.96 0 0 0-.7-.29 1.003 1.003 0 0 0-.71 1.71L16.58 3H13c-.55 0-1 .45-1 1s.45 1 1 1h3.58l-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.3-.71"];
})), OL, kL = o((() => {
	OL = ["M11.55 15.92c-1.48-.65-1.28-1.05-1.33-1.59-.01-.07-.01-.15-.01-.23.51-.45.92-1.07 1.19-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.34-.07.54-.44.61-.78.08-.14.23-.48.2-.87-.05-.5-.25-.73-.47-.82v-.09c0-.63-.06-1.55-.17-2.15-.02-.17-.06-.33-.11-.5a3.7 3.7 0 0 0-1.29-1.86C9.7 4.25 8.81 4 8.02 4s-1.68.25-2.31.73c-.61.47-1.07 1.13-1.29 1.86-.05.16-.09.33-.11.5-.12.6-.18 1.51-.18 2.14v.08c-.23.09-.44.32-.48.83-.04.39.12.73.2.87.08.35.28.72.63.78q.06.255.15.48c0 .01.01.02.01.03l.01.01c.27.72.7 1.35 1.22 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.38 1.59S.77 17.26.32 18.31C-.15 19.38.04 20 .04 20h15.95s.18-.62-.27-1.67c-.46-1.06-2.69-1.75-4.17-2.41M19 3h-3.58l1.29-1.29A1.003 1.003 0 0 0 15.29.29l-3 3c-.17.18-.28.43-.28.71s.11.53.29.71l3 3c.18.18.43.29.7.29a1.003 1.003 0 0 0 .71-1.71L15.42 5H19c.55 0 1-.45 1-1s-.45-1-1-1"];
})), AL, jL = o((() => {
	AL = ["M10.933 2.641a1 1 0 0 0-1.866 0L4.075 15.62a1 1 0 1 0 1.867.717L7.225 13h5.55l1.283 3.337a1 1 0 1 0 1.867-.717zM12.005 11h-4.01L10 5.786z"];
})), ML, NL = o((() => {
	ML = ["M16.71 11.29a1.003 1.003 0 0 0-1.42 1.42l1.3 1.29h-2.17l-8-8h10.17L15.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L16.59 4H1c-.55 0-1 .45-1 1s.45 1 1 1h2.59l9.71 9.71c.17.18.42.29.7.29h2.59l-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71z"];
})), PL, FL = o((() => {
	PL = ["M15.293 1.293a1 1 0 0 1 1.414 0l3 3a1 1 0 0 1 .202 1.121 1 1 0 0 1-.074.136l-.006.007-.038.051a1 1 0 0 1-.084.099l-3 3a1 1 0 0 1-1.414-1.414L16.586 6h-2.172l-9.707 9.707a1 1 0 0 1-.297.203l-.026.012-.052.02-.04.014-.062.016-.034.008-.031.004q-.03.007-.062.011L4 16H1a1 1 0 0 1 0-2h2.586l8-8H1a1 1 0 0 1 0-2h15.586l-1.293-1.293a1 1 0 0 1 0-1.414"];
})), IL, LL = o((() => {
	IL = ["M2 13v4h4v-4zm-1-2h6c.55 0 1 .45 1 1v6c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1v-6c0-.55.45-1 1-1m11-7h7c.55 0 1 .45 1 1s-.45 1-1 1h-7c-.55 0-1-.45-1-1s.45-1 1-1M8 1a1.003 1.003 0 0 1 .71 1.71l-5 6C3.53 8.89 3.28 9 3 9s-.53-.11-.71-.29l-2-2a1.003 1.003 0 0 1 1.42-1.42L3 6.59l4.29-5.3C7.47 1.11 7.72 1 8 1m4 13h7c.55 0 1 .45 1 1s-.45 1-1 1h-7c-.55 0-1-.45-1-1s.45-1 1-1"];
})), RL, zL = o((() => {
	RL = ["M9.754 20a8.5 8.5 0 0 1-3.417-.693 8.9 8.9 0 0 1-2.772-1.872 8.9 8.9 0 0 1-1.872-2.772A8.5 8.5 0 0 1 1 11.246a8.5 8.5 0 0 1 .693-3.416 8.9 8.9 0 0 1 1.872-2.772 8.9 8.9 0 0 1 2.772-1.872 8.5 8.5 0 0 1 3.417-.693h.145l-.826-.827a.9.9 0 0 1-.28-.68q.012-.39.28-.682a1 1 0 0 1 1.07-.24.9.9 0 0 1 .316.216l2.504 2.505a.93.93 0 0 1 .292.68q0 .39-.292.681L10.46 6.651a.9.9 0 0 1-.693.28 1 1 0 0 1-.906-1.355.9.9 0 0 1 .213-.311l.826-.827h-.145q-2.846 0-4.827 1.982-1.983 1.98-1.983 4.826t1.982 4.827q1.981 1.982 4.827 1.982t4.826-1.982 1.982-4.827a.94.94 0 0 1 .28-.693.94.94 0 0 1 .693-.28q.413 0 .692.28a.94.94 0 0 1 .28.693 8.5 8.5 0 0 1-.693 3.417 8.9 8.9 0 0 1-1.872 2.772 8.9 8.9 0 0 1-2.772 1.872A8.5 8.5 0 0 1 9.754 20M11.5 9.5v3h1v-3zM11 8h2a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1M9 9v4.25a.75.75 0 1 1-1.5 0V9.5h-.75a.75.75 0 0 1 0-1.5H8a1 1 0 0 1 1 1"];
})), BL, VL = o((() => {
	BL = ["m14.71 9.29-3.5-3.5a1.003 1.003 0 0 0-1.42 1.42L11.59 9H6c-.55 0-1 .45-1 1s.45 1 1 1h5.59L9.8 12.79c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3.5-3.5c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M5 11.73c.29.17.64.27 1 .27h1v6c0 1.1-.9 2-2 2H0v-2h5zM5 0c1.1 0 2 .9 2 2v6H6c-.36 0-.71.1-1 .27V2H0V0zm10 18h5v2h-5c-1.1 0-2-.9-2-2v-4.17l2-2zm5-16h-5v6.17l-2-2V2c0-1.1.9-2 2-2h5z"];
})), HL, UL = o((() => {
	HL = ["M2.196 2H0v2h2c.317 0 .619.139.825.38l3.493 4.075-1.873 1.248a1 1 0 0 0-.445.832V18c0 .5.5 1 1 1h14c.5 0 1-.5 1-1V7.1q0-.05-.004-.1H20V3s0-1-1-1h-8c-.5 0-1 .5-1 1v3L8.12 7.254 4.463 3.035A3 3 0 0 0 2.196 2M18 4v2h-6V4z"];
})), WL, GL = o((() => {
	WL = ["M10 0c5.523 0 10 4.477 10 10s-4.477 10-10 10S0 15.523 0 10 4.477 0 10 0"];
})), KL, qL = o((() => {
	KL = ["M15 16h2c.55 0 1-.45 1-1v-5h-4v5c0 .55.45 1 1 1M12 2c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v4h4zm6 4h-4v3h4zm0-4c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1v3h4zm-6 5H8v5h4zm-9 9h2c.55 0 1-.45 1-1v-3H2v3c0 .55.45 1 1 1m6 0h2c.55 0 1-.45 1-1v-2H8v2c0 .55.45 1 1 1m10 1H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M6 2c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v3h4zm0 4H2v5h4z"];
})), JL, YL = o((() => {
	JL = ["M3.41 2H6c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v5c0 .55.45 1 1 1s1-.45 1-1V3.41L7.29 8.7c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM8 11c-.28 0-.53.11-.71.29L2 16.59V14c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1H3.41l5.29-5.29c.19-.18.3-.43.3-.71 0-.55-.45-1-1-1M19 0h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L11.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 3.41V6c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m0 13c-.55 0-1 .45-1 1v2.59l-5.29-5.29A.97.97 0 0 0 12 11a1.003 1.003 0 0 0-.71 1.71l5.3 5.29H14c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1"];
})), XL, ZL = o((() => {
	XL = ["M10.14 5.82H8.73c.4-1.66.94-2.87 1.6-3.64.4-.48.8-.72 1.18-.72.08 0 .14.02.19.07s.07.1.07.18c0 .07-.05.19-.16.37s-.16.36-.16.52c0 .23.08.43.25.59a.9.9 0 0 0 .64.25c.28 0 .51-.1.7-.3s.28-.47.28-.81c0-.39-.14-.7-.42-.94s-.74-.36-1.36-.36c-.97 0-1.86.29-2.65.87-.79.56-1.54 1.52-2.26 2.85-.24.46-.48.75-.7.88s-.57.19-1.06.19l-.32 1.15H5.9l-1.99 7.85c-.33 1.29-.56 2.09-.67 2.39-.17.44-.43.81-.77 1.12a.74.74 0 0 1-.5.19c-.05 0-.1-.02-.14-.05l-.04-.07c0-.03.05-.1.15-.2s.15-.26.15-.47c0-.23-.08-.42-.23-.57-.16-.15-.38-.23-.67-.23-.35 0-.63.1-.85.29-.21.2-.32.43-.32.7q0 .435.39.75.375.33 1.2.33c.88 0 1.66-.23 2.33-.69.68-.46 1.27-1.17 1.78-2.14.51-.96 1.03-2.52 1.56-4.66l1.14-4.54H9.8zm6.8 1.95c.25-.2.51-.29.78-.29.1 0 .29.04.56.11.27.08.51.11.72.11.29 0 .52-.1.72-.3.18-.19.28-.45.28-.77 0-.33-.1-.6-.29-.8s-.47-.29-.82-.29c-.32 0-.62.08-.9.23s-.64.49-1.08 1c-.33.38-.81 1.05-1.44 2a9.7 9.7 0 0 0-1.31-3.22l-3.4.59-.07.37c.25-.05.47-.08.64-.08.34 0 .62.15.84.44.35.46.84 1.85 1.46 4.19-.49.66-.82 1.09-1 1.3-.3.33-.55.54-.74.64q-.225.12-.51.12c-.14 0-.38-.08-.7-.24-.22-.1-.42-.16-.59-.16-.33 0-.6.11-.82.32-.21.22-.32.49-.32.83 0 .31.1.57.3.77s.47.29.8.29c.32 0 .63-.07.92-.21s.64-.43 1.08-.88c.43-.45 1.03-1.16 1.79-2.14.29.93.55 1.61.76 2.03s.46.73.74.91c.28.19.62.28 1.04.28.4 0 .81-.15 1.23-.44.55-.38 1.1-1.04 1.68-1.97l-.35-.21c-.39.55-.68.89-.87 1.03-.12.09-.27.13-.44.13-.2 0-.4-.13-.59-.38-.33-.43-.77-1.63-1.33-3.6.47-.86.89-1.44 1.23-1.71"];
})), QL, $L = o((() => {
	QL = ["M15 2a1 1 0 1 1 0 2h-2.038a1.5 1.5 0 0 0-1.477 1.227h.001L10.996 8h3.083a1 1 0 0 1 0 2h-3.438l-.908 5.121v.005a3.5 3.5 0 0 1-3.14 2.86L6.289 18H4a1 1 0 1 1 0-2h2.288a1.5 1.5 0 0 0 1.477-1.231L8.609 10H5a1 1 0 0 1 0-2h3.964l.553-3.121v-.005A3.5 3.5 0 0 1 12.963 2z"];
})), eR, tR = o((() => {
	eR = ["M4 7h5c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m3 2v1c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1m12 3h-6c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m0 4H2V3c0-.55-.45-1-1-1s-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), nR, rR = o((() => {
	nR = ["M8 13a1 1 0 0 0-1-1H4.942a.942.942 0 0 1-.81-1.422L10.11.49A1.02 1.02 0 0 1 11 0a1 1 0 0 1 1 1v6a1 1 0 0 0 1 1h2.058a.942.942 0 0 1 .81 1.422L9.89 19.51A1.02 1.02 0 0 1 9 20a1 1 0 0 1-1-1z"];
})), iR, aR = o((() => {
	iR = ["m8 11 .075.003.126.017.111.03.111.044.098.052.096.067.09.08q.054.053.097.112l.071.11.054.114.035.105.03.148L9 12v6a1 1 0 0 1-1.993.117L7 18v-3.586l-5.293 5.293a1 1 0 0 1-1.497-1.32l.083-.094L5.584 13h-3.58a1 1 0 0 1-.117-1.993L2.004 11zm3.018-11a1 1 0 0 1 .39.087l.12.063.031.02.1.078 8.027 7.026.062.064.068.086.044.068.064.128.04.117.024.113.011.108v.1l-.007.073-.019.103-.037.121-.039.09-.05.087-4.996 7.994q-.091.147-.226.254l-.093.067-.095.053-.087.037-.125.037a1 1 0 0 1-.218.026H11v-5a3 3 0 0 0-2.824-2.995L8 9H3V6a1 1 0 0 1 .321-.734l.098-.08 7-5a1 1 0 0 1 .45-.178z"];
})), oR, sR = o((() => {
	oR = ["m0 8.33 9.17 2.5 2.5 9.17L20 0z"];
})), cR, lR = o((() => {
	cR = ["M8 18.88c-3.79 0-6.88-3.09-6.88-6.88 0-.61.08-1.22.23-1.79.03.01.06-.01.1-.01h.09v.55c0 .23.21.42.44.42.04 0 .09-.01.12-.02l.9.88c.09.09.23.09.32 0s.09-.23 0-.32l-.86-.9c0-.02.05-.04.05-.07v-.13c0-.18.1-.25.29-.41h.53c.1 0 .19-.01.27-.05.01-.01.02 0 .03-.01.02-.01.03-.02.05-.04.01-.01.02-.01.02-.02l.02-.02 1.13-1.13q-.24-.48-.42-.99h-.64v-.53c0-.01.06.06.06-.1h.38c-.04-.16-.08-.32-.1-.48h-.71c.2-.16.42-.31.64-.45C4.02 6.09 4 5.8 4 5.5c0-.14.01-.28.02-.43C1.62 6.46 0 9.04 0 12c0 4.41 3.59 8 8 8 3.87 0 7.09-2.77 7.82-6.44l-.97-1.1c-.26 3.57-3.23 6.42-6.85 6.42m-2.12-3.67v-.35h.15c.29 0 .49-.23.49-.53v-.68c0-.01.01-.01 0-.02L4.71 11.8h-.77c-.29 0-.47.24-.47.53v2c0 .29.18.53.47.53h.33v2.02c0 .28.28.51.56.51s.56-.23.56-.51v-1.22h-.01c.29 0 .5-.16.5-.45m13.83-2.92-3.68-3.68c.14-.21.27-.42.38-.65.02-.04.04-.07.05-.11.11-.22.2-.45.28-.69v-.01c.07-.24.13-.48.17-.73l.03-.17q.06-.36.06-.75C17 2.46 14.54 0 11.5 0S6 2.46 6 5.5 8.46 11 11.5 11c.26 0 .51-.02.76-.06l.17-.03c.25-.04.49-.1.73-.17h.01c.24-.08.47-.17.69-.28.04-.02.07-.04.11-.05.23-.11.44-.24.65-.38l3.68 3.68c.17.18.42.29.7.29a1.003 1.003 0 0 0 .71-1.71M11.5 9.5c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4m1.93 5.33v-.65c0-.11-.13-.21-.24-.21s-.24.09-.24.21v.65c0 .11.13.21.24.21s.24-.1.24-.21m-2.41.67h.83c.29 0 .46-.21.46-.5v-1.86l.23-.22c-.34.05-.69.08-1.04.08-.36 0-.7-.03-1.05-.08.03.05.06.1.08.16V15c.01.29.2.5.49.5"];
})), uR, dR = o((() => {
	uR = ["M15.555 7c-2.375 0-4.305 1.867-4.305 4.164 0 2.305 4.305 8.836 4.305 8.836s4.304-6.531 4.304-8.836C19.852 8.867 17.93 7 15.555 7m0 6.25a1.954 1.954 0 1 1 .001-3.908 1.954 1.954 0 0 1-.001 3.908M0 7.5C0 3.356 3.356 0 7.5 0a7.5 7.5 0 0 1 7.359 6.044 5.4 5.4 0 0 0-1.804.566A5.63 5.63 0 0 0 7.5 1.875 5.63 5.63 0 0 0 1.875 7.5 5.63 5.63 0 0 0 7.5 13.125c1.07 0 2.072-.3 2.924-.82.14.525.352 1.078.58 1.608l.078.178A7.5 7.5 0 0 1 7.5 15 7.5 7.5 0 0 1 0 7.5m8.438-3.563v3.179l1.603 1.593A.94.94 0 0 1 8.71 10.04L6.833 8.167a.94.94 0 0 1-.271-.666V3.937A.94.94 0 0 1 7.5 3a.94.94 0 0 1 .938.937"];
})), fR, pR = o((() => {
	fR = ["M8.788.915A3.121 3.121 0 0 0 3.801 4.54H1a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-2.8A3.122 3.122 0 0 0 11.211.915l-1 .999a4 4 0 0 0-.212.23 4 4 0 0 0-.213-.23zm5.424 3-.626.626H11.02a2.14 2.14 0 0 1 .606-1.213l.999-.999a1.121 1.121 0 1 1 1.586 1.586m-5.233.626H6.414l-.626-.626a1.121 1.121 0 1 1 1.586-1.586l1 1c.329.329.54.755.605 1.212M7 11.54H1v7a1 1 0 0 0 1 1h5zm12 0h-6v8h5a1 1 0 0 0 1-1zm-11 0h4v8H8z"];
})), mR, hR = o((() => {
	mR = ["M15 2c-1.66 0-3 1.34-3 3 0 1.3.84 2.4 2 2.82V9c0 1.1-.9 2-2 2H8c-.73 0-1.41.21-2 .55V5.82C7.16 5.4 8 4.3 8 3c0-1.66-1.34-3-3-3S2 1.34 2 3c0 1.3.84 2.4 2 2.82v8.37C2.84 14.6 2 15.7 2 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.25-.77-2.3-1.85-2.75C6.45 13.52 7.16 13 8 13h4c2.21 0 4-1.79 4-4V7.82C17.16 7.4 18 6.3 18 5c0-1.66-1.34-3-3-3M5 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 16c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M15 6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), gR, _R = o((() => {
	gR = ["M19 9h-4.1a5 5 0 0 0-9.8 0H1c-.55 0-1 .45-1 1s.45 1 1 1h4.1a5 5 0 0 0 9.8 0H19c.55 0 1-.45 1-1s-.45-1-1-1m-9 4c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3"];
})), vR, yR = o((() => {
	vR = ["M15 8c-1.3 0-2.4.84-2.82 2H11c-2.49 0-4.54-1.83-4.92-4.21A2.995 2.995 0 0 0 5 0C3.34 0 2 1.34 2 3c0 1.3.84 2.4 2 2.81v8.37C2.84 14.6 2 15.7 2 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.3-.84-2.4-2-2.82V9.86C7.27 11.17 9.03 12 11 12h1.18A2.996 2.996 0 0 0 18 11c0-1.66-1.34-3-3-3M5 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M5 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m10 8c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), bR, xR = o((() => {
	bR = ["M17 3h-1V2c0-.55-.45-1-1-1s-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1V5h1c.55 0 1-.45 1-1s-.45-1-1-1m-3 4.86V9c0 1.1-.9 2-2 2H8c-.73 0-1.41.21-2 .55V5.82C7.16 5.4 8 4.3 8 3c0-1.66-1.34-3-3-3S2 1.34 2 3c0 1.3.84 2.4 2 2.82v8.37C2.84 14.6 2 15.7 2 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.25-.77-2.3-1.85-2.75C6.45 13.52 7.16 13 8 13h4c2.21 0 4-1.79 4-4V7.86c-.32.08-.65.14-1 .14s-.68-.06-1-.14M5 2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1m0 16c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), SR, CR = o((() => {
	SR = ["M17 14.18V7c0-2.21-1.79-4-4-4h-2.59l1.29-1.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C7.11 3.47 7 3.72 7 4s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L10.41 5H13c1.1 0 2 .9 2 2v7.18A2.996 2.996 0 0 0 16 20c1.66 0 3-1.34 3-3 0-1.3-.84-2.4-2-2.82M16 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M4 1C2.34 1 1 2.34 1 4c0 1.3.84 2.4 2 2.82v7.37C1.84 14.6 1 15.7 1 17c0 1.66 1.34 3 3 3s3-1.34 3-3c0-1.3-.84-2.4-2-2.82V6.82C6.16 6.4 7 5.3 7 4c0-1.66-1.34-3-3-3m0 17c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1M4 5c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), wR, TR = o((() => {
	wR = ["M15 11c0-.28-.11-.53-.29-.71l-3-3C11.53 7.11 11.28 7 11 7s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42l1.29-1.3V19c0 .55.45 1 1 1s1-.45 1-1v-8.59l1.29 1.29c.18.19.43.3.71.3.55 0 1-.45 1-1m4-11H1C.45 0 0 .45 0 1v16c0 .55.45 1 1 1h7v-2H2v-2h6v-1H4V2h14v11h-4v1h4v2h-4v2h5c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M5 8h2V6H5zm2-5H5v2h2z"];
})), ER, DR = o((() => {
	ER = ["M3 1a2.998 2.998 0 0 1 1 5.825V13c0 .846.21 1.297.457 1.543.246.246.697.457 1.543.457h4.586l-1.293-1.293a1 1 0 1 1 1.414-1.414l3 3 .064.071a1 1 0 0 1 .205.415l.014.083q.007.045.009.09v.096l-.005.045a1 1 0 0 1-.2.512l-.019.026-.068.076-3 3a1 1 0 0 1-1.414-1.414L10.586 17H6c-1.154 0-2.203-.29-2.957-1.043C2.289 15.203 2 14.154 2 13V6.825A2.998 2.998 0 0 1 3 1M9.293.293a1 1 0 1 1 1.414 1.414L9.414 3H14c1.154 0 2.203.29 2.957 1.043C17.711 4.797 18 5.846 18 7v6.174A2.998 2.998 0 0 1 17 19a3 3 0 0 1-1-5.826V7c0-.846-.21-1.297-.457-1.543C15.297 5.211 14.846 5 14 5H9.414l1.293 1.293a1 1 0 1 1-1.414 1.414l-3-3-.068-.076-.02-.027a1 1 0 0 1-.2-.504q-.001-.027-.004-.052v-.096q.002-.045.009-.09l.014-.083q.014-.057.035-.112a1 1 0 0 1 .17-.303l.064-.071zM17 15a1 1 0 1 0 0 2 1 1 0 0 0 0-2M3 3a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), OR, kR = o((() => {
	OR = ["M7 3H5v2h2zm0 6H5v2h2zm0-3H5v2h2zm12-6H1C.45 0 0 .45 0 1v16c0 .55.45 1 1 1h4v2l2-1 2 1v-2h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 16H9v-1H5v1H2v-2h16zm0-3H4V2h14z"];
})), AR, jR = o((() => {
	AR = ["M17 6V0H3v6c0 3.53 2.61 6.43 6 6.92V18H6c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1h-3v-5.08c3.39-.49 6-3.39 6-6.92"];
})), MR, NR = o((() => {
	MR = ["M7.53 4.37c.1-.1.1-.26 0-.35l-.68-.68c-.1-.1-.25-.1-.35 0s-.1.26 0 .35l.68.68c.1.1.25.1.35 0m3.17.06h.3c.09 0 .16-.01.16-.1s-.07-.1-.16-.1h-.3c-.09 0-.16.01-.16.1s.07.1.16.1m.98 1.15c.09 0 .19-.08.19-.17v-.42c0-.09-.1-.17-.19-.17s-.19.08-.19.17v.42c0 .09.1.17.19.17m-6.5 4.19c-.35 0-.56.28-.56.63v2.37c0 .35.21.62.56.62h.39v2.4c0 .34.33.61.67.61s.67-.27.67-.61v-1.44h-.02c.35 0 .6-.19.6-.54v-.41h.18c.35 0 .58-.28.58-.62v-.81c0-.01.01-.01 0-.02L6.1 9.77zM10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8 0-.74.11-1.46.3-2.14h.03v.65c0 .28.25.5.53.5.05 0 .1-.01.15-.02l1.05 1.05c.1.11.28.11.38 0 .1-.1.11-.27 0-.38L3.42 8.59c0-.03.05-.05.05-.08v-.16c0-.22.12-.3.34-.49h.63c.12 0 .23-.01.32-.07.01-.01.02 0 .03-.01.02-.02.04-.03.06-.04.01-.01.02-.01.03-.02l.02-.02 2.15-2.15c.24-.24.24-.63 0-.86-.23-.24-.62-.19-.86.04l-.41.46H5v-.64c0-.01.07.07.07-.12h.87c.17 0 .3-.12.3-.29s-.13-.29-.3-.29H4.88C6.27 2.7 8.05 2 10 2s3.73.7 5.12 1.86h-1.58l-.01-.04c-.06 0-.12 0-.17.04l-.71.7c-.09.09-.09.23 0 .31.09.09.23.09.32 0l.56-.6.01-.03h.34c0 .19-.1.13-.1.16v.1c0 .29-.2.5-.49.5h-.51c-.25 0-.52.28-.52.54v.23h-.12c-.16 0-.27.08-.27.24v.33h-.32c-.23 0-.41.15-.41.38 0 .22.18.35.41.35.1 0 .19.04.26-.16l.06.01.66-.59h.23l.53.5c.04.04.11.03.16-.01.04-.04.04-.16 0-.2L13 6.15h.32l.12.16c.25.25.65.23.89-.02l.12-.14H15c.02 0 .11.07.11.07v.33s-.06-.01-.07-.01h-.49c-.16 0-.28.13-.28.29s.13.29.28.29h.49c.01 0 .07-.01.07-.01v.2c-.19.28-.33.57-.62.57h-1.28s0-.01-.01-.01l-.58-.58a.62.62 0 0 0-.89 0l-.58.58s0 .01-.01.01h-.34c-.35 0-.67.28-.67.63v1.25c0 .35.32.61.67.61h1.22c.46.19.78.48.97.94v2.28c0 .35.23.6.58.6h.98c.35 0 .54-.25.54-.6v-2.2l1.21-1.17.04-.02.02-.01h.04c.1-.11.2-.26.2-.42V8.49c0-.25-.22-.44-.42-.63h.58c.02.38.29.57.63.57h.43c.13.51.18 1.03.18 1.57 0 4.42-3.58 8-8 8m6.16-5.65c-.14 0-.29.11-.29.25v.77c0 .14.15.25.29.25s.29-.11.29-.25v-.77c0-.14-.15-.25-.29-.25M10.5 3.48c0-.34-.28-.57-.62-.57h-.74c-.34 0-.57.25-.57.59 0 .05-.13.06.06.1v.64c0 .2.09.36.29.36s.29-.16.29-.36v-.19h.68c.33 0 .61-.23.61-.57"];
})), PR, FR = o((() => {
	PR = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m7.39 7h-3.63c-.31-1.99-.92-3.66-1.72-4.73 2.45.65 4.41 2.42 5.35 4.73M13 10c0 .69-.04 1.36-.11 2H7.11a18.4 18.4 0 0 1 0-4h5.77c.08.64.12 1.31.12 2m-3-8c1.07 0 2.25 2.05 2.75 5h-5.5c.5-2.95 1.68-5 2.75-5m-2.04.27C7.16 3.34 6.55 5.01 6.24 7H2.61c.94-2.31 2.9-4.08 5.35-4.73M2 10c0-.69.11-1.36.28-2h3.83a18.4 18.4 0 0 0 0 4H2.28c-.17-.64-.28-1.31-.28-2m.61 3h3.63c.31 1.99.92 3.66 1.72 4.73A8 8 0 0 1 2.61 13M10 18c-1.07 0-2.25-2.05-2.75-5h5.5c-.5 2.95-1.68 5-2.75 5m2.04-.27c.79-1.07 1.4-2.74 1.72-4.73h3.63a8 8 0 0 1-5.35 4.73M13.89 12a18.4 18.4 0 0 0 0-4h3.83c.17.64.28 1.31.28 2s-.11 1.36-.28 2z"];
})), IR, LR = o((() => {
	IR = ["m12.75 7-.002-.01Q12.874 7 13 7c0 .755.26 1.539.86 2.14q.062.06.125.116.058 1.376-.095 2.744h3.83c.17-.64.28-1.31.28-2q0-.37-.04-.732A2.92 2.92 0 0 0 19 7q.264 0 .526-.049C19.834 7.912 20 8.937 20 10c0 5.52-4.48 10-10 10S0 15.52 0 10 4.48 0 10 0c1.06 0 2.084.165 3.043.472A3.3 3.3 0 0 0 13 1c-1.049 0-1.88.5-2.398 1.204A1.1 1.1 0 0 0 10 2C8.93 2 7.75 4.05 7.25 7zm.14 5c.07-.64.11-1.31.11-2s-.04-1.36-.12-2H7.11a18.4 18.4 0 0 0 0 4zM6.24 7c.31-1.99.92-3.66 1.72-4.73A8 8 0 0 0 2.61 7zM2 10c0 .69.11 1.36.28 2h3.83a18.4 18.4 0 0 1 0-4H2.28C2.11 8.64 2 9.31 2 10m4.24 3H2.61c.94 2.31 2.9 4.08 5.35 4.73-.8-1.07-1.41-2.74-1.72-4.73M10 18c1.07 0 2.25-2.05 2.75-5h-5.5c.5 2.95 1.68 5 2.75 5m3.76-5c-.32 1.99-.93 3.66-1.72 4.73A8 8 0 0 0 17.39 13zM13 5c-.6 0-1-.4-1-1 0-.5.4-1 1-1h2V1c0-.6.4-1 1-1 .5 0 1 .4 1 1v2h2c.5 0 1 .4 1 1s-.5 1-1 1h-2v2c0 .6-.5 1-1 1-.6 0-1-.4-1-1V5z"];
})), RR, zR = o((() => {
	RR = ["M17.5 4A2.5 2.5 0 0 0 15 6.5c0 .06.01.12.02.18l-1.9.84C12.38 6.6 11.27 6 10 6c-.83 0-1.59.25-2.23.68L4.91 4.14c.05-.21.09-.42.09-.64a2.5 2.5 0 0 0-5 0A2.5 2.5 0 0 0 2.5 6c.42 0 .81-.11 1.16-.3l2.79 2.48C6.17 8.73 6 9.34 6 10c0 1.41.73 2.64 1.83 3.35l-.56 1.67A2.5 2.5 0 0 0 5 17.5a2.5 2.5 0 0 0 5 0c0-.74-.32-1.39-.83-1.85l.56-1.68c.09.01.18.03.27.03 2.21 0 4-1.79 4-4 0-.22-.03-.44-.07-.65l2.02-.9c.43.34.96.55 1.55.55a2.5 2.5 0 0 0 0-5"];
})), BR, VR = o((() => {
	BR = ["m17.41 4 2.29-2.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L16 2.59 13.71.3A.97.97 0 0 0 13 0a1.003 1.003 0 0 0-.71 1.71L14.59 4 12.3 6.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L16 5.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM19 10c-.83 0-1.55-.36-2.09-.91l-.03.03-.88-.88-.88.88a2.996 2.996 0 1 1-4.24-4.24l.88-.88-.88-.88.03-.03C10.36 2.55 10 1.83 10 1c0-.35.07-.68.18-.99-.06 0-.12-.01-.18-.01C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10c0-.06-.01-.12-.01-.18-.31.11-.64.18-.99.18"];
})), HR, UR = o((() => {
	HR = ["m12.838 10-9.154 3.051a1 1 0 0 0 .632 1.898l12-4c.912-.304.912-1.594 0-1.898l-12-4a1 1 0 0 0-.632 1.898z"];
})), WR, GR = o((() => {
	WR = ["M3.684 11.051a1 1 0 0 0 .632 1.898l12-4c.912-.304.912-1.594 0-1.898l-12-4a1 1 0 0 0-.632 1.898L12.838 8zM4 15h12a1 1 0 1 1 0 2H4a1 1 0 0 1 0-2"];
})), KR, qR = o((() => {
	KR = ["M19 11c.55 0 1-.45 1-1s-.45-1-1-1h-2V5h2c.55 0 1-.45 1-1s-.45-1-1-1h-2V1c0-.55-.45-1-1-1s-1 .45-1 1v2h-4V1c0-.55-.45-1-1-1S9 .45 9 1v2H5V1c0-.55-.45-1-1-1S3 .45 3 1v2H1c-.55 0-1 .45-1 1s.45 1 1 1h2v4H1c-.55 0-1 .45-1 1s.45 1 1 1h2v4H1c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h4v2c0 .55.45 1 1 1s1-.45 1-1v-2h4v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c.55 0 1-.45 1-1s-.45-1-1-1h-2v-4zM9 15H5v-4h4zm0-6H5V5h4zm6 6h-4v-4h4zm0-6h-4V5h4z"];
})), JR, YR = o((() => {
	JR = ["M0 19c0 .55.45 1 1 1h8v-9H0zM0 1v8h9V0H1C.45 0 0 .45 0 1m19-1h-8v9h9V1c0-.55-.45-1-1-1m-8 20h8c.55 0 1-.45 1-1v-8h-9z"];
})), XR, ZR = o((() => {
	XR = ["M15.757.703a1 1 0 0 0-1.414 0l-3.536 3.535a1 1 0 0 0 0 1.415l3.536 3.535a1 1 0 0 0 1.414 0l3.536-3.535a1 1 0 0 0 0-1.415zM1 1.996a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1zm2 5v-4h4v4zm-1 4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1zm1 2v4h4v-4zm8-1a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6a1 1 0 0 1-1-1zm2 5v-4h4v4z"];
})), QR, $R = o((() => {
	QR = ["M6 7c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3m8-3H6c-3.31 0-6 2.69-6 6s2.69 6 6 6h8c3.31 0 6-2.69 6-6s-2.69-6-6-6m0 11H6c-2.76 0-5-2.24-5-5s2.24-5 5-5h8c2.76 0 5 2.24 5 5s-2.24 5-5 5m0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3"];
})), ez, tz = o((() => {
	ez = ["M12 16h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1m7 1H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m-3-1h1c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1m-9 0h1c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1H7c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1m-4 0h1c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v13c0 .55.45 1 1 1"];
})), nz, rz = o((() => {
	nz = ["M17 5c-.42 0-.79.27-.93.64L14.38 10h-.77l1.34-6.67c.03-.1.05-.21.05-.33a.998.998 0 0 0-1.98-.19h-.01L11.57 10H11V1c0-.55-.45-1-1-1S9 .45 9 1v9h-.2L6.97 2.76a.997.997 0 0 0-1.73-.41l-.03.03c-.01.02-.02.03-.03.04-.01.02-.01.03-.02.04v.01c-.01.01-.02.02-.02.03v.01c-.02.01-.02.02-.03.03 0 0 0 .01-.01.01 0 .01 0 .02-.01.03 0 0 0 .01-.01.01 0 .01-.01.02-.01.03 0 0 0 .01-.01.01 0 .01-.01.02-.01.03s0 .01-.01.02c0 .01-.01.02-.01.03s0 .01-.01.02c0 .01-.01.02-.01.03v.02c0 .01 0 .02-.01.03V3c0 .05 0 .09.01.14l1.45 10.25L6 12.7v.01L3.84 9.45h-.01A.98.98 0 0 0 3 9c-.55 0-1 .45-1 1 0 .2.06.39.17.55L6 18.44C7.06 19.4 8.46 20 10 20c3.31 0 6-2.69 6-6v-1.84l.01-.03v-.06l1.94-5.75A1.003 1.003 0 0 0 17 5"];
})), iz, az = o((() => {
	iz = ["M17.68 9.84C15.91 9 14.27 6.49 13.45 4.9 12.41 2.43 12.21 0 7.87 0 5.49 0 3.95.76 3.05 2.65 2.31 4.2 2 5.48 2 9.79v.99c0 .82.69 1.48 1.54 1.48.38 0 .73-.14 1-.36.19.6.78 1.05 1.47 1.05.47 0 .89-.2 1.17-.52.26.47.77.79 1.36.79.65 0 1.2-.39 1.43-.93l.03.77v5.44c0 .48.23.91.59 1.18.21.19.5.32.85.32h.06c.83 0 1.5-.67 1.5-1.5v-8.24l.01-.67c.85.98 1.92 1.76 3.24 1.89 1.79.19 2.09-1.33 1.43-1.64"];
})), oz, sz = o((() => {
	oz = ["M15.1 6.54c-1.58-.81-4.09-2.46-4.94-4.23-.31-.65-1.82-.35-1.64 1.43.13 1.33.91 2.4 1.89 3.24L9.74 7H1.5C.67 7 0 7.67 0 8.5v.06c0 .36.13.64.32.85.27.36.7.59 1.18.59h5.44l.78.01c-.54.23-.93.78-.93 1.43 0 .59.32 1.1.79 1.36-.32.28-.52.7-.52 1.17 0 .69.44 1.28 1.05 1.47-.22.27-.36.62-.36 1 0 .85.66 1.54 1.48 1.54h.99c4.31 0 5.59-.31 7.14-1.05 1.89-.9 2.65-2.44 2.65-4.82-.01-4.32-2.44-4.52-4.91-5.57"];
})), cz, lz = o((() => {
	cz = ["M20 8.5c0-.83-.67-1.5-1.5-1.5h-8.24l-.67-.01c.98-.85 1.76-1.92 1.89-3.24.18-1.79-1.33-2.08-1.65-1.43-.84 1.76-3.35 3.41-4.93 4.23C2.43 7.59 0 7.79 0 12.13c0 2.38.76 3.92 2.65 4.82C4.2 17.69 5.48 18 9.79 18h.99c.82 0 1.48-.69 1.48-1.54 0-.38-.14-.73-.36-1 .6-.19 1.05-.78 1.05-1.47 0-.47-.2-.89-.52-1.17.47-.26.79-.77.79-1.36 0-.65-.39-1.2-.93-1.43l.77-.03h5.44c.48 0 .91-.23 1.18-.59.19-.21.32-.49.32-.85z"];
})), uz, dz = o((() => {
	uz = ["M16.46 7.74c-.38 0-.73.14-1 .36-.19-.6-.78-1.05-1.47-1.05-.47 0-.89.2-1.17.52-.26-.47-.77-.79-1.36-.79-.65 0-1.2.39-1.43.93L10 6.94V1.5c0-.48-.23-.91-.59-1.18C9.2.13 8.92 0 8.56 0H8.5C7.67 0 7 .67 7 1.5v8.24l-.01.67c-.84-.98-1.92-1.76-3.24-1.89-1.79-.18-2.08 1.33-1.43 1.65 1.77.84 3.41 3.35 4.23 4.94 1.05 2.47 1.25 4.9 5.58 4.9 2.38 0 3.92-.76 4.82-2.65.74-1.56 1.05-2.84 1.05-7.15v-.99c0-.81-.69-1.48-1.54-1.48"];
})), fz, pz = o((() => {
	fz = ["M18.5 13c1.118 0 1.466.534 1.498 1.366L20 14.5v.5c0 1.945-5.69 3-10 3S0 16.945 0 15v-.5c0-.908.323-1.5 1.5-1.5.895 0 3.5 1.2 8.5 1.2l.411-.003C15.143 14.134 17.631 13 18.5 13m-5-10q2.587 0 3.688 8.186c-1.455.263-3.805.72-6.392.801l-.434.01L10 12c-2.896 0-5.585-.524-7.189-.814Q3.913 3 6.5 3C8.6 3 8.329 5.5 10 5.5S11.5 3 13.5 3"];
})), mz, hz = o((() => {
	mz = ["M6 11v5a1 1 0 1 1-2 0V3a1 1 0 0 1 2 0v6h8V3a1 1 0 1 1 2 0v13a1 1 0 1 1-2 0v-5z"];
})), gz, _z = o((() => {
	gz = ["M2 11v5a1 1 0 1 1-2 0V3a1 1 0 0 1 2 0v6h7V3a1 1 0 1 1 2 0v13a1 1 0 1 1-2 0v-5zm15.74-1c-.05.31-.17.57-.34.77-.17.21-.38.39-.64.51-.25.13-.52.23-.83.29-.3.05-.61.08-.93.08v1.24h2.5V20H19V10z"];
})), vz, yz = o((() => {
	vz = ["M2 11v5a1 1 0 1 1-2 0V3a1 1 0 0 1 2 0v6h7V3a1 1 0 1 1 2 0v13a1 1 0 1 1-2 0v-5zm16.458 3.64c.487.11.865.38 1.134.82s.408.968.408 1.608q0 .69-.239 1.229-.239.542-.656.919c-.27.25-.588.44-.956.58s-.746.209-1.154.209c-.498 0-.925-.08-1.294-.24a2.54 2.54 0 0 1-.925-.68 3 3 0 0 1-.567-1.058q-.195-.63-.209-1.379h1.383c-.02.58.11 1.07.378 1.459.279.39.677.58 1.224.58q.702 0 1.164-.45c.309-.3.468-.72.468-1.27 0-.369-.07-.668-.2-.888a1.27 1.27 0 0 0-.507-.5 2 2 0 0 0-.706-.21 5.4 5.4 0 0 0-.806-.03v-1.168c.219.01.448 0 .677-.05s.428-.13.607-.24.318-.27.428-.47.159-.45.159-.739q.002-.614-.368-.989c-.25-.25-.568-.37-.956-.37-.239 0-.448.06-.627.17q-.268.165-.447.45c-.12.19-.2.4-.26.63-.049.23-.079.469-.069.719H14.16c.01-.47.09-.9.23-1.3.138-.399.327-.748.566-1.038q.359-.45.866-.69c.338-.17.726-.25 1.154-.25.328 0 .657.05.975.16q.478.165.866.48c.259.21.468.47.617.8.15.32.229.699.229 1.118 0 .48-.09.91-.289 1.27a1.7 1.7 0 0 1-.915.788z"];
})), bz, xz = o((() => {
	bz = ["M2 11v5a1 1 0 1 1-2 0V3a1 1 0 0 1 2 0v6h7V3a1 1 0 1 1 2 0v13a1 1 0 1 1-2 0v-5zm14.033 6.96c.16-.19.34-.38.558-.55.21-.18.449-.36.708-.53.25-.18.498-.36.748-.56.249-.2.488-.41.727-.63.23-.22.439-.47.628-.74.18-.27.329-.56.438-.88.11-.32.16-.67.16-1.07 0-.32-.05-.65-.14-1s-.249-.68-.468-.97c-.22-.3-.508-.55-.867-.74-.359-.2-.807-.29-1.346-.29-.488 0-.926.1-1.295.29q-.557.27-.947.78c-.26.33-.449.73-.578 1.2-.13.46-.2.96-.2 1.5h1.426c.01-.35.04-.67.09-.97s.139-.56.249-.78.259-.39.448-.52c.19-.13.429-.19.708-.19q.463 0 .747.18c.19.12.34.26.449.43.11.17.18.36.219.56q.06.3.06.57c-.01.38-.1.72-.26 1.02-.149.3-.368.57-.627.83-.26.25-.538.49-.847.71-.31.22-.608.45-.887.68a5.3 5.3 0 0 0-1.406 1.58c-.349.61-.518 1.32-.528 2.13h5.97v-1.43h-4.266c.06-.21.17-.42.33-.61"];
})), Sz, Cz = o((() => {
	Sz = ["M18.97 9H19A9 9 0 0 0 1 9h.03C.41 9.73 0 10.8 0 12c0 1.74.84 3.2 2 3.76V16c0 1.66 1.34 3 3 3h3c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1H5c-.55 0-1-.45-1-1 .55 0 1-.45 1-1V9c0-.55-.45-1-1-1h-.92C3.57 4.61 6.47 2 10 2s6.43 2.61 6.92 6H16c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h1c1.66 0 3-1.79 3-4 0-1.2-.41-2.27-1.03-3"];
})), wz, Tz = o((() => {
	wz = ["M20 6.25C20 3.35 17.65 1 14.75 1c-1.02 0-1.95.31-2.75.82v-.04c-.09.06-.17.12-.26.19-.04.03-.09.06-.14.1-.68.51-1.24 1.18-1.6 1.96-.4-.86-1.04-1.57-1.8-2.1-.04-.02-.07-.05-.1-.08a7 7 0 0 0-.6-.33c-.13-.04-.23-.1-.35-.15-.05-.02-.1-.05-.15-.07v.02C6.45 1.13 5.87 1 5.25 1A5.25 5.25 0 0 0 0 6.25c0 .09.01.17.01.25H0c0 .06.01.12.02.18s.01.12.02.18C.13 7.89.44 9 1.07 10.17 2.23 12.33 4.1 14.11 7 16.53v.01c.9.75 1.89 1.55 3 2.46.71-.58 1.38-1.12 2-1.63 3.48-2.86 5.64-4.78 6.93-7.18.63-1.17.94-2.27 1.03-3.3.01-.07.01-.14.02-.21 0-.06.01-.11.02-.17h-.01c0-.09.01-.17.01-.26"];
})), Ez, Dz = o((() => {
	Ez = ["M8.11 7.45C8.05 7.31 8 7.16 8 7c0-.07.03-.13.04-.19h-.02l.86-4.32A5.16 5.16 0 0 0 5.25 1 5.25 5.25 0 0 0 0 6.25c0 .09.01.17.01.25H0c0 .06.01.12.02.18s.01.12.02.18C.13 7.89.44 9 1.07 10.17c1.38 2.58 3.76 4.6 7.71 7.83l-.76-3.8h.02c-.01-.07-.04-.13-.04-.2 0-.21.08-.39.18-.54l-.02-.01 1.68-2.52zM20 6.25C20 3.35 17.65 1 14.75 1c-1.54 0-2.92.67-3.88 1.73l-.83 4.13 1.85 3.69h-.01c.07.14.12.29.12.45 0 .21-.08.39-.18.54l.02.01-1.77 2.66.81 4.07c4.16-3.39 6.63-5.45 8.05-8.1.63-1.17.94-2.27 1.03-3.3.01-.07.01-.14.02-.21 0-.06.01-.11.02-.17h-.01c0-.08.01-.16.01-.25"];
})), Oz, kz = o((() => {
	Oz = ["M14 12h6V8h-6zM0 12h6V8H0zm1-3h4v2H1zm-1 7c0 .55.45 1 1 1h5v-4H0zM19 3h-5v4h6V4c0-.55-.45-1-1-1m0 3h-4V4h4zM0 4v3h6V3H1c-.55 0-1 .45-1 1m7 3h6V3H7zm7 10h5c.55 0 1-.45 1-1v-3h-6zm-7 0h6v-4H7zm1-3h4v2H8zm-1-2h6V8H7z"];
})), Az, jz = o((() => {
	Az = ["M18 16a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2.5 14a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5M6 0a6 6 0 0 1 5.606 8.137 4.5 4.5 0 0 1 1.728.868A3.5 3.5 0 1 1 16.5 14c-.59 0-1.147-.148-1.635-.406a4.5 4.5 0 0 1-8.837-1.595L6 12A6 6 0 1 1 6 0m10.5 0a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5"];
})), Mz, Nz = o((() => {
	Mz = ["M10 3v2H1V3.5a.5.5 0 0 0-1 0v5a.5.5 0 0 0 1 0V7l5 2c0 1.54.824 3.575 3 4.835V16H5.5a.5.5 0 1 0 0 1h11a.5.5 0 0 0 .224-.053l2-1a.5.5 0 1 0-.448-.894L16.382 16H15v-1.1A5.002 5.002 0 0 0 14 5h-1V3h6.5a.5.5 0 0 0 0-1h-16a.5.5 0 0 0 0 1zm4 13v-1c-1.608 0-2.928-.258-4-.683V16zm0-6V6a4 4 0 0 1 4 4z"];
})), Pz, Fz = o((() => {
	Pz = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0M7.41 4.62c.65-.54 1.51-.82 2.56-.82.54 0 1.03.08 1.48.25.44.17.83.39 1.14.68.32.29.56.63.74 1.02.17.39.26.82.26 1.27s-.08.87-.24 1.23c-.16.37-.4.73-.71 1.11l-1.21 1.58c-.14.17-.28.33-.32.48-.05.15-.11.35-.11.6v.97H9v-2s.06-.58.24-.81l1.21-1.64c.25-.3.41-.56.51-.77s.14-.44.14-.67c0-.35-.11-.63-.32-.85s-.5-.33-.88-.33c-.37 0-.67.11-.89.33-.22.23-.37.54-.46.94-.03.12-.11.17-.23.16l-1.95-.29c-.12-.01-.16-.08-.14-.22.13-.93.52-1.67 1.18-2.22M9 14h2.02L11 16H9z"];
})), Iz, Lz = o((() => {
	Iz = ["M17 10h-3v3h3zm0 4h-3v3h3zm0-8h-3v3h3zm2-6H1C.4 0 0 .4 0 1v18c0 .5.4 1 1 1h18c.5 0 1-.5 1-1V1c0-.6-.5-1-1-1m-1 18H2V2h16zm-9-4H6v3h3zm4 0h-3v3h3z"];
})), Rz, zz = o((() => {
	Rz = ["M7.35 5h5.3l2.77 5-2.77 5h-5.3l-2.77-5zm1.15 5c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5-.67-1.5-1.5-1.5-1.5.67-1.5 1.5M4.63 1.51c.18-.31.52-.51.89-.51h8.95c.37 0 .71.19.89.51l4.52 8c.17.3.17.67 0 .97l-4.51 8c-.18.31-.52.51-.89.51H5.53c-.37 0-.71-.19-.89-.51l-4.51-8a.99.99 0 0 1 0-.97zM6.13 17h7.76l3.95-7-3.95-7H6.13l-3.95 7z"];
})), Bz, Vz = o((() => {
	Bz = ["M12 16v4H8v-4zm1-16-1 14H8L7 0z"];
})), Hz, Uz = o((() => {
	Hz = ["M7 0h6a1 1 0 0 1 1 1v3h2V2a1 1 0 1 1 0-2h3a1 1 0 1 1 0 2h-1v2h1a1 1 0 1 1 0 2h-1v2h1a1 1 0 1 1 0 2h-3a1 1 0 1 1 0-2V6h-2v13a1 1 0 0 1-1.927.376L10 14.54l-2.072 4.834A1 1 0 0 1 6 19V6H4v2a1 1 0 0 1 0 2H1a1 1 0 0 1 0-2h1V6H1a1 1 0 0 1 0-2h1V2H1a1 1 0 0 1 0-2h3a1 1 0 0 1 0 2v2h2V1a1 1 0 0 1 1-1m1 2v2h4V2zm4 12.128V9.872L11.088 12zM8.516 6 10 9.462 11.483 6zm.396 6L8 9.872v4.256z"];
})), Wz, Gz = o((() => {
	Wz = ["m11.22 14.09 3.03-3.03.71.71L20 6.73l-5.71-5.71-5.04 5.04.71.71-3.02 3.04zm6.8 3.91h-16c-.55 0-1 .45-1 1s.45 1 1 1h16c.55 0 1-.45 1-1s-.45-1-1-1m-15-1h4.04c.28 0 .53-.11.71-.3l2.02-2.02-3.44-3.45-4.04 4.04c-.18.18-.3.44-.3.71.01.57.46 1.02 1.01 1.02"];
})), Kz, qz = o((() => {
	Kz = ["M10 0C6.71 0 3.82 1.6 2 4.05V2c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.76C5.23 3.17 7.47 2 10 2c4.42 0 8 3.58 8 8s-3.58 8-8 8-8-3.58-8-8c0-.55-.45-1-1-1s-1 .45-1 1c0 5.52 4.48 10 10 10s10-4.48 10-10S15.52 0 10 0m0 3c-.55 0-1 .45-1 1v6c0 .28.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L11 9.59V4c0-.55-.45-1-1-1"];
})), Jz, Yz = o((() => {
	Jz = ["M2 12v7c0 .55.45 1 1 1h5v-7h4v7h5c.55 0 1-.45 1-1v-7l-8-8zm17.71-2.71L17 6.59V3c0-.55-.45-1-1-1s-1 .45-1 1v1.59L10.71.3C10.53.11 10.28 0 10 0s-.53.11-.71.29l-9 9a1.003 1.003 0 0 0 1.42 1.42L10 2.41l8.29 8.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), Xz, Zz = o((() => {
	Xz = ["M1 1c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1m3 5h11c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1m8 8H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1m7-6H4c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h15c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1"];
})), Qz, $z = o((() => {
	Qz = ["M1 9h11c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m0-5h9c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m18 12H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1M1 14h14c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1"];
})), eB, tB = o((() => {
	eB = ["M10 16H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m2-5H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h11c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m3-5H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1m4-5H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1"];
})), nB, rB = o((() => {
	nB = ["M12 2H8c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1M1 0C.45 0 0 .45 0 1v18c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m18 0c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), iB, aB = o((() => {
	iB = ["M11.293 13.707a1 1 0 0 0 1.412 0l2.963-2.962a1 1 0 0 0 0-1.49l-2.963-2.962a.999.999 0 1 0-1.412 1.412L13.587 10l-2.294 2.295a1 1 0 0 0 0 1.412m-3.998 0a.999.999 0 0 0 1.412-1.412L6.413 10l2.294-2.295a.999.999 0 1 0-1.412-1.412L4.332 9.255l-.04.038A1 1 0 0 0 4 10a1 1 0 0 0 .332.745zM0 20V0h1a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1zm20 0V0h-1a1 1 0 0 0-1 1v18a1 1 0 0 0 1 1z"];
})), oB, sB = o((() => {
	oB = ["M0 14c1.648.775 3 1 4 1-1-1-2-3.112-2-5v-.045C2 5.17 6.201 1 11.172 1c3.206 0 6.9.667 8.828 5-1.648-.775-3-1-4-1 1 1 2 3.112 2 5v.045C18 14.83 13.799 19 8.828 19c-3.206 0-6.9-.667-8.828-5m10-7a3 3 0 1 0 0 6 3 3 0 0 0 0-6"];
})), cB, lB = o((() => {
	cB = ["M2 5v10h16V5zm0-2h16c1.1 0 2 .9 2 2v10c0 1.1-.9 2-2 2H2c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2m6.88 9.38c-.17-.39-1.01-.66-1.56-.9-.56-.24-.48-.39-.5-.6v-.09c.19-.17.35-.4.45-.67 0 0 0-.02.01-.02l.06-.18c.13-.03.2-.17.23-.29.03-.05.09-.18.08-.33-.04-.18-.11-.27-.2-.3v-.03c0-.24-.02-.58-.06-.81-.01-.06-.02-.12-.04-.19-.08-.27-.25-.52-.48-.7C6.63 7.09 6.3 7 6 7s-.63.09-.87.27c-.23.17-.4.42-.48.7-.02.06-.03.13-.04.19-.04.22-.06.57-.06.81V9c-.09.03-.17.12-.19.31-.01.14.05.27.08.32.03.14.1.27.23.3.02.06.03.12.06.18v.01c.11.27.27.51.47.68v.08c-.02.2.04.35-.51.6-.56.24-1.39.51-1.56.9-.19.39-.12.62-.12.62h5.98c-.01 0 .06-.23-.11-.62M12 7h4c.55 0 1 .45 1 1s-.45 1-1 1h-4c-.55 0-1-.45-1-1s.45-1 1-1m0 4h4c.55 0 1 .45 1 1s-.45 1-1 1h-4c-.55 0-1-.45-1-1s.45-1 1-1"];
})), uB, dB = o((() => {
	uB = ["M10.5 13c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5-1.5.67-1.5 1.5.67 1.5 1.5 1.5M14 7H1c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-1 10-5-3-1 2-2-4-3 4.5V9h11zm3-15h-1.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2c-.18.18-.29.43-.29.71s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H16c1.1 0 2 .9 2 2v3c0 .55.45 1 1 1s1-.45 1-1V6c0-2.21-1.79-4-4-4"];
})), fB, pB = o((() => {
	fB = ["M5.29 4.29a1.003 1.003 0 0 0 1.42 1.42l2-2C8.89 3.53 9 3.28 9 3s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l.3.29H4C1.79 2 0 3.79 0 6v3c0 .55.45 1 1 1s1-.45 1-1V6c0-1.1.9-2 2-2h1.59zM15.5 13c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5-1.5.67-1.5 1.5.67 1.5 1.5 1.5M19 7H6c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-1 10-5-3-1 2-2-4-3 4.5V9h11z"];
})), mB, hB = o((() => {
	mB = ["M9.29 15.71c.18.18.43.29.71.29s.53-.11.71-.29l5-5a1.003 1.003 0 0 0-1.42-1.42L11 12.59V1c0-.55-.45-1-1-1S9 .45 9 1v11.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42zM19 14c-.55 0-1 .45-1 1v3H2v-3c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1"];
})), gB, _B = o((() => {
	gB = ["m16.92 3.56-.01-.02c-.16-.35-.5-.6-.91-.6H4c-.41 0-.76.25-.91.6l-.01.02L0 10.49v6.46c0 .55.45 1 1 1h18c.55 0 1-.45 1-1v-6.46zM15 10.95c-.55 0-1 .45-1 1v1H6v-1c0-.55-.45-1-1-1H1.98l2.67-6h10.7l2.67 6z"];
})), vB, yB = o((() => {
	vB = ["m10.262 3 1.958 1.958v.05H4.65l-2.67 5.997H5c.55 0 1 .45 1 .999v1h8v-1c0-.55.45-1 1-1h3.02l-.635-1.426.625-.63c.354-.353.598-.8.707-1.289L20 10.545v6.456c0 .55-.45.999-1 .999H1c-.55 0-1-.45-1-1v-6.455L3.08 3.62l.01-.02c.15-.35.5-.6.91-.6zm9.088-3a.642.642 0 0 1 .46 1.1l-3.03 3.03v2.95c0 .18-.07.34-.19.46l-1.28 1.29c-.11.1-.27.17-.45.17-.35 0-.64-.29-.64-.64V4.13L11.19 1.1a.642.642 0 0 1 .45-1.1z"];
})), bB, xB = o((() => {
	bB = ["M7.427 3a7.5 7.5 0 0 0-.411 2.009H4.65l-2.67 5.996H5c.55 0 1 .45 1 .999v1h8V13c.165.01.332 0 .5 0a7.48 7.48 0 0 0 5.5-2.4V17c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1v-6.455L3.08 3.62l.01-.02c.15-.35.5-.6.91-.6zm5.715-.596a.133.133 0 0 1-.193 0l-.374-.374a.133.133 0 0 1 0-.193.133.133 0 0 1 .193 0l.373.374a.133.133 0 0 1 0 .193m1.743.033c-.05 0-.088-.006-.088-.055 0-.05.038-.056.088-.056h.165c.05 0 .088.006.088.055 0 .05-.038.056-.088.056zm.539.632c-.05 0-.104-.044-.104-.094v-.23c0-.05.054-.094.104-.094s.104.044.104.094v.23c0 .05-.055.094-.104.094m-3.575 2.305h.506l1.182 1.199c.006.005 0 .005 0 .01v.446c0 .187-.126.341-.319.341h-.098v.226c0 .192-.138.297-.33.297h.01v.792c0 .186-.181.335-.368.335s-.369-.149-.369-.335v-1.32h-.214c-.193 0-.308-.149-.308-.341V5.72c0-.192.115-.346.308-.346M14.5 0C17.536 0 20 2.464 20 5.5S17.536 11 14.5 11A5.5 5.5 0 0 1 9 5.5C9 2.464 11.464 0 14.5 0m0 9.9c2.431 0 4.4-1.969 4.4-4.4a3.5 3.5 0 0 0-.099-.864h-.236c-.187 0-.336-.104-.347-.313h-.319c.11.104.231.209.231.346v.705c0 .088-.055.17-.11.23h-.022l-.011.006-.022.011-.666.643v1.21c0 .193-.104.33-.296.33h-.54c-.192 0-.319-.137-.319-.33V6.222a.92.92 0 0 0-.533-.518h-.671c-.192 0-.368-.143-.368-.335v-.687c0-.193.176-.347.368-.347l.193-.005.319-.32a.34.34 0 0 1 .489 0l.319.32c.005 0 .005.005.005.005h.704c.16 0 .237-.16.341-.313v-.11l-.038.005h-.27a.16.16 0 0 1-.153-.16c0-.087.066-.159.154-.159h.269l.039.006V3.42s-.05-.038-.061-.038h-.302l-.067.076a.34.34 0 0 1-.489.011l-.066-.088h-.176l.248.259c.021.022.021.088 0 .11-.028.022-.067.028-.088.006l-.292-.276h-.127l-.363.325-.033-.006c-.038.11-.087.089-.143.089-.126 0-.225-.072-.225-.193 0-.127.099-.209.225-.209h.176v-.182c0-.088.061-.131.149-.131h.066v-.127c0-.143.149-.297.286-.297h.28c.16 0 .27-.115.27-.275V2.42c0-.016.055.017.055-.088h-.187l-.005.017-.308.33a.123.123 0 0 1-.177 0c-.049-.044-.049-.121 0-.171l.391-.385c.027-.022.06-.022.094-.022l.005.022h.869A4.38 4.38 0 0 0 14.5 1.1a4.4 4.4 0 0 0-2.816 1.018h.583c.094 0 .165.066.165.159s-.072.16-.165.16h-.478c0 .104-.039.06-.039.066v.351h.429l.226-.252c.132-.127.346-.155.473-.022a.33.33 0 0 1 0 .473l-1.183 1.182-.011.011c-.005.005-.011.005-.016.011a.1.1 0 0 0-.034.022c-.005.006-.01 0-.016.006a.3.3 0 0 1-.176.038h-.347c-.12.104-.187.148-.187.27v.088c0 .016-.027.027-.027.043l.561.589c.06.06.055.154 0 .209a.143.143 0 0 1-.209 0l-.578-.578a.4.4 0 0 1-.082.011c-.154 0-.292-.12-.292-.274v-.358h-.016c-.104.374-.165.77-.165 1.177 0 2.431 1.969 4.4 4.4 4.4m3.388-3.107c.077 0 .16.06.16.137v.424c0 .077-.083.137-.16.137s-.16-.06-.16-.137V6.93c0-.077.083-.137.16-.137m-3.113-4.879c0 .187-.154.314-.335.314h-.374v.104c0 .11-.05.198-.16.198s-.16-.088-.16-.198V1.98c-.104-.022-.033-.028-.033-.055 0-.187.127-.324.314-.324h.407c.187 0 .341.126.341.313"];
})), SB, CB = o((() => {
	SB = ["M7.136 3a6.3 6.3 0 0 0-.098 2.009H4.65l-2.67 5.996H5c.55 0 1 .45 1 .999v1h8v-1c0-.55.45-1 1-1h1.076l1.14 1.14a2.77 2.77 0 0 0 1.974.806q.424-.002.81-.12V17c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1v-6.455L3.08 3.62l.01-.02c.15-.35.5-.6.91-.6zm3.244 1.33c0 1.62 1.31 2.93 2.93 2.93s2.93-1.31 2.93-2.93-1.31-2.93-2.93-2.93-2.93 1.31-2.93 2.93m6.47 2.43 2.89 2.85c.13.15.22.35.23.56 0 .43-.35.78-.78.78-.23 0-.42-.08-.56-.22l-2.87-2.87c-.17.1-.33.2-.51.29-.03.01-.06.03-.09.04-.18.07-.35.15-.55.21-.19.06-.37.11-.57.14-.05.01-.1.02-.14.02-.2.03-.39.05-.6.05A4.3 4.3 0 0 1 9 4.31C9 1.93 10.93.01 13.3 0c2.37 0 4.3 1.93 4.3 4.3 0 .21-.02.4-.05.6-.01.05-.01.09-.02.14-.04.2-.08.38-.14.58-.05.19-.13.36-.21.54-.01.03-.03.06-.04.09-.08.18-.18.34-.29.51"];
})), wB, TB = o((() => {
	wB = ["M10.083 3a6 6 0 0 0 .001 2.009H4.65l-2.67 5.996H5c.55 0 1 .45 1 .999v1h8v-1c0-.55.45-1 1-1h3.02l-.53-1.19a6 6 0 0 0 1.824-.811L20 10.545v6.456c0 .55-.45.999-1 .999H1c-.55 0-1-.45-1-1v-6.455L3.08 3.62l.01-.02c.15-.35.5-.6.91-.6zM16 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8"];
})), EB, DB = o((() => {
	EB = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0M9 4h2v2H9zm4 12H7v-1h2V8H8V7h3v8h2z"];
})), OB, kB = o((() => {
	OB = ["M6 10c0 2.21 1.79 4 4 4h6.59l-2.29-2.29A.97.97 0 0 1 14 11a1.003 1.003 0 0 1 1.71-.71l4 4c.18.18.29.43.29.71s-.11.53-.29.71l-4 4a1.003 1.003 0 0 1-1.42-1.42l2.3-2.29H10c-3.31 0-6-2.69-6-6H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1zM2 2v6h6V2z"];
})), AB, jB = o((() => {
	AB = ["M1 9c.55 0 1 .45 1 1v4c0 1.1.9 2 2 2h2.59l-.3-.29a1.003 1.003 0 0 1 1.42-1.42l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2A1.003 1.003 0 0 1 6 19c0-.28.11-.53.3-.71l.29-.29H4c-2.21 0-4-1.79-4-4v-4c0-.55.45-1 1-1m6.996-9c.79 0 1.68.25 2.309.73a3.63 3.63 0 0 1 1.4 2.36c.11.6.17 1.52.17 2.15v.09c.22.09.42.32.47.82.03.39-.12.73-.2.87-.07.34-.27.71-.61.78-.04.16-.09.33-.15.48-.01.01-.02.05-.02.05-.27.71-.68 1.33-1.19 1.78 0 .08 0 .16.01.23.05.55-.15.95 1.33 1.6 1.469.66 3.698 1.35 4.178 2.39.45 1.05.27 1.67.27 1.67h-5.227a2 2 0 0 0-.319-.417l-2-2A2.003 2.003 0 0 0 5 15H4c-.548 0-1-.452-1-1v-1.462c.511-.213 1.023-.413 1.468-.608 1.479-.65 1.329-1.05 1.379-1.59l.01-.21c-.52-.45-.95-1.08-1.22-1.8l-.01-.01-.01-.03c-.07-.15-.12-.32-.16-.49-.34-.06-.54-.43-.62-.78-.08-.14-.24-.48-.2-.87.05-.51.26-.74.49-.83v-.08c0-.64.05-1.55.17-2.15a3.65 3.65 0 0 1 1.4-2.36C6.317.25 7.207 0 7.996 0m5.997 3c.59 0 1.26.19 1.73.55.46.35.8.85.97 1.4.04.13.07.25.08.38.08.45.13 1.14.13 1.61v.07c.16.07.31.24.35.62.02.29-.09.55-.15.65-.05.26-.2.53-.46.59-.03.12-.07.25-.11.36-.01.01-.01.04-.01.04-.2.53-.51 1-.89 1.34 0 .06 0 .12.01.17.04.41-.11.71 1 1.19 1.099.5 2.768 1.01 3.128 1.79.34.79.2 1.25.2 1.25h-3.039V15a5 5 0 0 0-.33-1.06c-.45-.97-1.37-1.52-3.238-2.3-.17-.07-.76-.31-.77-.32-.1-.04-.2-.08-.28-.12.05-.14.04-.29.06-.45l.01-.16c-.25-.21-.47-.48-.65-.79.22-.34.41-.71.56-1.12l.028-.078-.002.013-.006.035.06-.15c.36-.26.6-.67.72-1.13.18-.37.29-.82.25-1.3-.05-.5-.21-.92-.47-1.22-.02-.53-.06-1.11-.12-1.59.38-.17.83-.26 1.24-.26"];
})), MB, NB = o((() => {
	MB = ["M8.7 4.7C7.4 6 6.5 7.9 6.5 10s.8 4 2.2 5.3c-.8.5-1.7.7-2.7.7-3.3 0-6-2.7-6-6s2.7-6 6-6c1 0 1.9.2 2.7.7m-3.34 9.25c-.55-1.2-.86-2.54-.86-3.95s.31-2.75.86-3.95a4.001 4.001 0 0 0 0 7.9M14 4c3.3 0 6 2.7 6 6s-2.7 6-6 6c-1 0-1.9-.2-2.7-.7 1.3-1.3 2.2-3.2 2.2-5.3s-.8-3.9-2.2-5.3C12.1 4.2 13 4 14 4m.6 2.05c.55 1.2.86 2.54.86 3.95s-.31 2.75-.86 3.95c1.9-.31 3.36-1.96 3.36-3.95S16.5 6.36 14.6 6.05M10 5.5C8.8 6.7 8 8.2 8 10s.8 3.3 2 4.4c1.2-1.1 2-2.7 2-4.5s-.8-3.3-2-4.4"];
})), PB, FB = o((() => {
	PB = ["M20 10c0 5.51-4.49 10-10 10-1.17 0-2.32-.2-3.42-.6a1 1 0 0 1-.6-1.28c.19-.52.76-.79 1.28-.6.88.32 1.8.48 2.74.48 4.41 0 8-3.59 8-8s-3.59-8-8-8c-.94 0-1.86.16-2.74.48a1 1 0 0 1-1.28-.6A1 1 0 0 1 6.58.6C7.68.2 8.83 0 10 0c5.51 0 10 4.49 10 10m-4.29-.71-4-4a1.003 1.003 0 0 0-1.42 1.42L12.59 9H1a1 1 0 0 0 0 2h11.59l-2.29 2.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), IB, LB = o((() => {
	IB = ["M19 0H1C.4 0 0 .4 0 1v18c0 .5.4 1 1 1h18c.5 0 1-.5 1-1V1c0-.6-.5-1-1-1m-1 18H2V2h16zM5 11h4v4c0 .6.4 1 1 1s1-.4 1-1v-4h4c.6 0 1-.4 1-1s-.4-1-1-1h-4V5c0-.6-.4-1-1-1s-1 .4-1 1v4H5c-.6 0-1 .4-1 1s.4 1 1 1"];
})), RB, zB = o((() => {
	RB = ["M10 9c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.46-1-1-1m4.992.975v-.044a.4.4 0 0 0-.106-.225 7.7 7.7 0 0 0-1.087-1.125c-.831-.731-1.78-1.343-2.824-1.587a4.15 4.15 0 0 0-1.819-.025c-.562.112-1.093.337-1.593.619-.78.443-1.5 1.05-2.124 1.73a7 7 0 0 0-.331.395.46.46 0 0 0 0 .58c.318.42.7.788 1.087 1.126.83.731 1.78 1.343 2.824 1.587q.91.214 1.83.025c.557-.112 1.088-.337 1.594-.619.78-.443 1.5-1.05 2.118-1.73.113-.126.231-.257.337-.395a.44.44 0 0 0 .107-.225V10c-.013-.012-.013-.019-.013-.025M10 12c-1.107 0-2-.893-2-2s.893-2 2-2 2 .893 2 2-.893 2-2 2M7 1a1 1 0 0 0-1-1H1a1 1 0 0 0-1 1v5a1 1 0 0 0 2 0V2h4a1 1 0 0 0 1-1m6 0a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0V2h-4a1 1 0 0 1-1-1m0 18a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-5a1 1 0 1 0-2 0v4h-4a1 1 0 0 0-1 1m-6 0a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-5a1 1 0 1 1 2 0v4h4a1 1 0 0 1 1 1"];
})), BB, VB = o((() => {
	BB = ["M13 4c-1.31 0-2.51.43-3.5 1.14A5.98 5.98 0 0 0 6 4c-3.31 0-6 2.69-6 6s2.69 6 6 6c1.31 0 2.51-.43 3.5-1.14.99.71 2.19 1.14 3.5 1.14 3.31 0 6-2.69 6-6s-2.69-6-6-6m-4.93 9.41c-.61.37-1.31.59-2.07.59-2.21 0-4-1.79-4-4s1.79-4 4-4c.76 0 1.46.22 2.07.59C7.4 7.56 7 8.73 7 10s.4 2.44 1.07 3.41M13 14c-.76 0-1.46-.22-2.07-.59C11.6 12.44 12 11.27 12 10s-.4-2.44-1.07-3.41C11.54 6.22 12.24 6 13 6c2.21 0 4 1.79 4 4s-1.79 4-4 4"];
})), HB, UB = o((() => {
	HB = ["M6 3.66C6 5.69 10 11 10 11s4-5.31 4-7.34C13.99 1.64 12.21 0 10 0S6 1.64 6 3.66M8 4c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2m6 9.5V13h-4v1h3v2h-2v1h3zM3 12h14c.55 0 1 .45 1 1v6c0 .55-.45 1-1 1H3c-.55 0-1-.45-1-1v-6c0-.55.45-1 1-1m4 1v6h1v-6zm3 1v5h1v-5z"];
})), WB, GB = o((() => {
	WB = ["M10 20C4.477 20 0 15.523 0 10S4.477 0 10 0s10 4.477 10 10-4.477 10-10 10m0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16m1-2H9v-2h2zm0-3H9V4h2z"];
})), KB, qB = o((() => {
	KB = ["M15.364 5.9a1 1 0 0 1-.707-.293l-2.121-2.122a1 1 0 1 1 1.414-1.414l1.414 1.414L18.192.657a1 1 0 0 1 1.414 1.414l-3.535 3.536a1 1 0 0 1-.707.292M11.78.157a3 3 0 0 0-1.437 1.85 8 8 0 1 0 7.1 5.055l.042-.042 1.472-1.472A9.96 9.96 0 0 1 20 10c0 5.523-4.477 10-10 10S0 15.523 0 10 4.477 0 10 0q.913.001 1.78.158M11 16H9v-2h2zm0-3H9V4h2z"];
})), JB, YB = o((() => {
	JB = ["M13.167.512a3 3 0 0 0-.131.524 3 3 0 0 0-1.848 1.052 8 8 0 1 0 6.724 6.724 3 3 0 0 0 1.052-1.848 3 3 0 0 0 .524-.13A10 10 0 0 1 20 10c0 5.523-4.477 10-10 10S0 15.523 0 10 4.477 0 10 0a10 10 0 0 1 3.167.512M11 16H9v-2h2zm0-3H9V4h2zm6-10h1.5a1 1 0 0 1 0 2H17v1.5a1 1 0 0 1-2 0V5h-1.5a1 1 0 0 1 0-2H15V1.5a1 1 0 0 1 2 0z"];
})), XB, ZB = o((() => {
	XB = ["M11.7 4H14c.6 0 1-.4 1-1s-.4-1-1-1H7c-.6 0-1 .4-1 1s.4 1 1 1h2.2L7.3 15H5c-.6 0-1 .4-1 1s.4 1 1 1h7c.6 0 1-.4 1-1s-.4-1-1-1H9.8z"];
})), QB, $B = o((() => {
	QB = ["M19 6h-4V2c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h4v4c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1M6 12H2V9h4zm0-4H2V5h4zm7 9H7v-3h6zm0-4H7V9h6zm0-5H7V5h6zm5 9h-4v-3h4zm0-4h-4v-3h4z"];
})), eV, tV = o((() => {
	eV = ["M14 0c-3.31 0-6 2.69-6 6 0 1.11.32 2.14.85 3.03L.44 17.44a1.498 1.498 0 1 0 2.12 2.12l.79-.79.94.94c.18.18.43.29.71.29s.53-.11.71-.29l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-.94-.94 3.2-3.2A5.9 5.9 0 0 0 14 12c3.31 0 6-2.69 6-6s-2.69-6-6-6m0 9c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3"];
})), nV, rV = o((() => {
	nV = ["M19 3H7c-.28 0-.53.11-.71.29l-6 6C.11 9.47 0 9.72 0 10s.11.53.29.71l6 6c.18.18.43.29.71.29h12c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1m-2.29 9.29a1.003 1.003 0 0 1-1.42 1.42L13 11.41l-2.29 2.29c-.18.19-.43.3-.71.3a1.003 1.003 0 0 1-.71-1.71l2.3-2.29-2.3-2.29a1.003 1.003 0 0 1 1.42-1.42L13 8.59l2.29-2.29c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71L14.41 10z"];
})), iV, aV = o((() => {
	iV = ["M15.5 12H14V8h1.5C17.43 8 19 6.43 19 4.5S17.43 1 15.5 1 12 2.57 12 4.5V6H8V4.5C8 2.57 6.43 1 4.5 1S1 2.57 1 4.5 2.57 8 4.5 8H6v4H4.5C2.57 12 1 13.57 1 15.5S2.57 19 4.5 19 8 17.43 8 15.5V14h4v1.5c0 1.93 1.57 3.5 3.5 3.5s3.5-1.57 3.5-3.5-1.57-3.5-3.5-3.5m0-9c.83 0 1.5.67 1.5 1.5S16.33 6 15.5 6 14 5.33 14 4.5 14.67 3 15.5 3m-11 14c-.83 0-1.5-.67-1.5-1.5S3.67 14 4.5 14s1.5.67 1.5 1.5S5.33 17 4.5 17m0-11C3.67 6 3 5.33 3 4.5S3.67 3 4.5 3 6 3.67 6 4.5 5.33 6 4.5 6m7.5 6H8V8h4zm3.5 5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5"];
})), oV, sV = o((() => {
	oV = ["m16.71 7.29-6-6C10.53 1.11 10.28 1 10 1s-.53.11-.71.29l-6 6a1.003 1.003 0 0 0 1.42 1.42L10 3.41l5.29 5.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71"];
})), cV, lV = o((() => {
	cV = ["m19.71 9.29-6-6A1 1 0 0 0 13 3H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h12c.28 0 .53-.11.71-.29l6-6c.18-.18.29-.43.29-.71s-.11-.53-.29-.71m-9 3a1.003 1.003 0 0 1-1.42 1.42L7 11.41 4.71 13.7c-.18.19-.43.3-.71.3a1.003 1.003 0 0 1-.71-1.71L5.59 10l-2.3-2.29a1.003 1.003 0 0 1 1.42-1.42L7 8.59 9.29 6.3c.18-.19.43-.3.71-.3a1.003 1.003 0 0 1 .71 1.71L8.41 10z"];
})), uV, dV = o((() => {
	uV = ["M18 2c-.55 0-1 .45-1 1v5c0 2.21-1.79 4-4 4H4.41L6.7 9.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4c-.18.18-.29.43-.29.71s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L4.41 14H13c3.31 0 6-2.69 6-6V3c0-.55-.45-1-1-1"];
})), fV, pV = o((() => {
	fV = ["M2 8c.55 0 1-.45 1-1V4.41l6.29 6.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L4.41 3H7c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1v5c0 .55.45 1 1 1m9-6.94V3.1c3.39.49 6 3.38 6 6.9 0 3.87-3.13 7-7 7-3.52 0-6.41-2.61-6.9-6H1.06c.5 4.5 4.31 8 8.94 8a9 9 0 0 0 9-9c0-4.63-3.5-8.44-8-8.94"];
})), mV, hV = o((() => {
	mV = ["M13 4h6c.55 0 1-.45 1-1s-.45-1-1-1h-6c-.55 0-1 .45-1 1s.45 1 1 1m6 12h-4.42L6.87 2.5l-.02.01A.98.98 0 0 0 6 2H1c-.55 0-1 .45-1 1s.45 1 1 1h4.42l7.71 13.5.01-.01c.18.3.49.51.86.51h5c.55 0 1-.45 1-1s-.45-1-1-1"];
})), gV, _V = o((() => {
	gV = ["m17.74 10.35-6.99-8.01-.01.01C10.56 2.14 10.3 2 10 2s-.56.14-.74.35l-.01-.01-7 8 .01.01A.95.95 0 0 0 2 11c0 .55.45 1 1 1h3v5c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-5h3c.55 0 1-.45 1-1 0-.25-.1-.48-.26-.65"];
})), vV, yV = o((() => {
	vV = ["M19 13H4.41l2.29-2.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L2 12.59V10c0-.55-.45-1-1-1s-1 .45-1 1v8c0 .55.45 1 1 1s1-.45 1-1v-2.59l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L4.41 15H19c.55 0 1-.45 1-1s-.45-1-1-1m0-12c-.55 0-1 .45-1 1v2.59L14.71 1.3A.97.97 0 0 0 14 1a1.003 1.003 0 0 0-.71 1.71L15.59 5H1c-.55 0-1 .45-1 1s.45 1 1 1h14.59L13.3 9.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 7.41V10c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1"];
})), bV, xV = o((() => {
	bV = ["M19 4a1 1 0 0 0-.707.293L14 8.586l-2.293-2.293a1 1 0 0 0-1.414 1.414l3 3a.997.997 0 0 0 1.414 0l5-5A1 1 0 0 0 19 4m-2.048 7.291c.011.072.048.134.048.209a1.5 1.5 0 0 1-1.5 1.5c-.225 0-.433-.057-.624-.145-.279.085-.57.145-.876.145a3 3 0 0 1-2.121-.879l-3-3 .007-.007A3 3 0 0 1 8.184 8H4V7l1-3h10l.19.568 1.307-1.308c-.336-.356-.758-.658-1.165-.772 0 0-1.74-.488-5.332-.488s-5.332.488-5.332.488c-.67.188-1.424.864-1.674 1.502L2.99 4H3L2 7H1a1 1 0 0 0 0 2h.333l-.28.84L1 10v7.5a1.5 1.5 0 1 0 3 0V17h12v.5a1.5 1.5 0 0 0 3 0V10l-.19-.568zM4.5 13a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"];
})), SV, CV = o((() => {
	SV = ["M13 2a1 1 0 0 1 0 2v4l4 8v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-1l4-8V4a1 1 0 1 1 0-2zm-2 2H9v4l-2 4h6l-2-4z"];
})), wV, TV = o((() => {
	wV = ["M3 12h14v-1H3zm11-9H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V9zm4 12H2V5h11v3H3v1h10v1h5zm-4-6V5l4 4z"];
})), EV, DV = o((() => {
	EV = ["m19.5 9.1-9-5c-.2-.1-.3-.1-.5-.1s-.3 0-.5.1l-9 5c-.3.2-.5.5-.5.9s.2.7.5.9l9 5c.2.1.3.1.5.1s.3 0 .5-.1l9-5c.3-.2.5-.5.5-.9s-.2-.7-.5-.9"];
})), OV, kV = o((() => {
	OV = ["m9.514 4.126-9 5a1 1 0 0 0 0 1.748l9 5a1 1 0 0 0 .972 0l9-5a1 1 0 0 0 0-1.748l-9-5a1 1 0 0 0-.972 0M10 6.144l6.94 3.855L10 13.855 3.059 9.999z"];
})), AV, jV = o((() => {
	AV = ["m.5 6.9 9 5c.2.1.3.1.5.1s.3 0 .5-.1l9-5c.3-.2.5-.5.5-.9s-.2-.7-.5-.9l-9-5c-.2-.1-.3-.1-.5-.1s-.3 0-.5.1l-9 5c-.3.2-.5.5-.5.9s.2.7.5.9M19 9c-.2 0-.3 0-.5.1L10 13.9 1.5 9.1C1.3 9 1.2 9 1 9c-.6 0-1 .4-1 1 0 .4.2.7.5.9l9 5c.2.1.3.1.5.1s.3 0 .5-.1l9-5c.3-.2.5-.5.5-.9 0-.6-.4-1-1-1m0 4c-.2 0-.3 0-.5.1L10 17.9l-8.5-4.7c-.2-.2-.3-.2-.5-.2-.6 0-1 .4-1 1 0 .4.2.7.5.9l9 5c.2.1.3.1.5.1s.3 0 .5-.1l9-5c.3-.2.5-.5.5-.9 0-.6-.4-1-1-1"];
})), MV, NV = o((() => {
	MV = ["M18 6c-1.1 0-2 .9-2 2 0 .37.11.71.28 1.01l-2.27 2.27c-.3-.17-.64-.28-1.01-.28-.93 0-1.71.64-1.93 1.5H8.93c-.22-.86-1-1.5-1.93-1.5-.37 0-.71.11-1.01.28L3.72 9.01C3.89 8.71 4 8.37 4 8c0-.34-.09-.66-.24-.94l3.66-3.38c.31.2.68.32 1.08.32 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .34.09.66.24.94L3.08 6.32C2.77 6.12 2.4 6 2 6 .9 6 0 6.9 0 8s.9 2 2 2c.37 0 .71-.11 1.01-.28l2.27 2.27c-.17.3-.28.64-.28 1.01s.11.71.28 1.01l-2.27 2.27C2.71 16.11 2.37 16 2 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2c0-.37-.11-.71-.28-1.01l2.27-2.27c.3.17.64.28 1.01.28.93 0 1.71-.64 1.93-1.5h2.14c.22.86 1 1.5 1.93 1.5 1.1 0 2-.9 2-2 0-.37-.11-.71-.28-1.01l2.27-2.27c.3.17.64.28 1.01.28 1.1 0 2-.9 2-2s-.9-2-2-2"];
})), PV, FV = o((() => {
	PV = ["M18 13c-.53 0-1.01.21-1.37.55L11.9 10.6c.06-.19.1-.39.1-.6s-.04-.41-.1-.6l4.72-2.95c.37.34.85.55 1.38.55 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .21.04.41.1.6l-4.73 2.96c-.24-.23-.54-.4-.87-.48V3.93c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S8 .9 8 2c0 .93.64 1.71 1.5 1.93v4.14c-.33.09-.63.26-.87.48L3.9 5.6c.06-.19.1-.39.1-.6 0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.53 0 1.01-.21 1.37-.55L8.1 9.4c-.06.19-.1.39-.1.6s.04.41.1.6l-4.72 2.95C3.01 13.21 2.53 13 2 13c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2c0-.21-.04-.41-.1-.6l4.73-2.96c.24.23.54.4.87.48v4.14C8.64 16.29 8 17.07 8 18c0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93v-4.14c.33-.09.63-.26.87-.48l4.73 2.96c-.06.18-.1.38-.1.59 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2"];
})), IV, LV = o((() => {
	IV = ["M18 16c-.14 0-.28.02-.42.05l-1.73-3.45c.69-.45 1.14-1.22 1.14-2.1s-.46-1.65-1.14-2.1l1.73-3.45c.14.03.28.05.42.05 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .6.27 1.13.69 1.5l-1.77 3.54c-.14-.02-.28-.04-.42-.04a2.5 2.5 0 0 0-2.45 2h-4.1A2.5 2.5 0 0 0 5.5 8c-.14 0-.28.02-.42.04L3.31 4.5C3.73 4.13 4 3.6 4 3c0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.14 0 .28-.02.42-.05L4.14 8.4C3.46 8.85 3 9.62 3 10.5s.46 1.65 1.14 2.1l-1.73 3.45A2 2 0 0 0 2 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2c0-.6-.27-1.13-.69-1.5l1.77-3.54c.14.02.28.04.42.04a2.5 2.5 0 0 0 2.45-2h4.1a2.5 2.5 0 0 0 2.45 2c.14 0 .28-.02.42-.04l1.77 3.54c-.42.37-.69.9-.69 1.5 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2"];
})), RV, zV = o((() => {
	RV = ["M0 1a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 11a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm7 0a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1zm8 0a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-3a1 1 0 0 1-1-1z"];
})), BV, VV = o((() => {
	BV = ["M0 12a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm11 0a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), HV, UV = o((() => {
	HV = ["M18.3 8c-.2-.9-.6-1.7-1.1-2.5.2-.3.3-.7.3-1 0-1.1-.9-2-2-2-.4 0-.7.1-1 .3-.8-.5-1.6-.8-2.5-1.1-.1-1-1-1.7-2-1.7S8.2.8 8 1.7c-.9.3-1.7.6-2.5 1.1-.3-.2-.7-.3-1-.3-1.1 0-2 .9-2 2 0 .4.1.7.3 1-.5.8-.8 1.6-1.1 2.5C.8 8.2 0 9 0 10s.8 1.8 1.7 2c.2.9.6 1.7 1.1 2.5-.2.3-.3.7-.3 1 0 1.1.9 2 2 2 .4 0 .7-.1 1-.3.8.5 1.6.8 2.5 1.1.1 1 1 1.7 2 1.7s1.8-.8 2-1.7c.9-.2 1.7-.6 2.5-1.1.3.2.7.3 1 .3 1.1 0 2-.9 2-2 0-.4-.1-.7-.3-1 .5-.8.8-1.6 1.1-2.5 1-.1 1.7-1 1.7-2s-.8-1.8-1.7-2m-1.8 5.8c-.3-.2-.6-.3-1-.3-1.1 0-2 .9-2 2 0 .4.1.7.3 1-.6.3-1.2.6-1.9.8-.3-.7-1-1.3-1.9-1.3-.8 0-1.6.5-1.9 1.3-.7-.2-1.3-.4-1.9-.8.2-.3.3-.6.3-1 0-1.1-.9-2-2-2-.4 0-.7.1-1 .3-.3-.6-.6-1.2-.8-1.9.8-.3 1.3-1.1 1.3-1.9s-.5-1.6-1.2-1.8c.2-.7.4-1.3.8-1.9.3.2.6.3 1 .3 1.1 0 2-.9 2-2 0-.4-.1-.7-.3-1 .6-.3 1.2-.6 1.9-.8.2.7 1 1.2 1.8 1.2s1.6-.5 1.9-1.3c.7.2 1.3.4 1.9.8-.2.3-.3.6-.3 1 0 1.1.9 2 2 2 .4 0 .7-.1 1-.3.3.6.6 1.2.8 1.9-.8.3-1.3 1.1-1.3 1.9s.5 1.6 1.2 1.8c-.1.7-.4 1.4-.7 2"];
})), WV, GV = o((() => {
	WV = ["M2 16a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 8a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m8 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4"];
})), KV, qV = o((() => {
	KV = ["M18 16a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 14a2 2 0 1 1 0 4 2 2 0 0 1 0-4m11-2a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 8a2 2 0 1 1 0 4 2 2 0 0 1 0-4m16 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m-5-4a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4m16-2a2 2 0 1 1 0 4 2 2 0 0 1 0-4"];
})), JV, YV = o((() => {
	JV = ["M18.5 16.07v-4.14c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2-.93 0-1.71.64-1.93 1.5h-4.14c-.18-.7-.73-1.25-1.43-1.43V3.93c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S8 .9 8 2c0 .93.64 1.71 1.5 1.93v4.14c-.7.18-1.25.73-1.43 1.43H3.93C3.71 8.64 2.93 8 2 8c-1.1 0-2 .9-2 2 0 .93.64 1.71 1.5 1.93v4.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93v-4.14c.7-.18 1.25-.73 1.43-1.43h4.14c.18.7.73 1.25 1.43 1.43v4.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93v-4.14c.7-.18 1.25-.73 1.43-1.43h4.14c.18.7.73 1.25 1.43 1.43v4.14c-.86.22-1.5 1-1.5 1.93 0 1.1.9 2 2 2s2-.9 2-2c0-.93-.64-1.71-1.5-1.93"];
})), XV, ZV = o((() => {
	XV = ["M11 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 7a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 8a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), QV, $V = o((() => {
	QV = ["M0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 11a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zM11 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1z"];
})), eH, tH = o((() => {
	eH = ["M16.5 7a2.5 2.5 0 0 0-2.45 2h-2.1a2.5 2.5 0 0 0-4.9 0h-2.1a2.5 2.5 0 1 0 0 1h2.1a2.5 2.5 0 0 0 4.9 0h2.1a2.5 2.5 0 1 0 2.45-3"];
})), nH, rH = o((() => {
	nH = ["M0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm11 0a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zm0 7a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zm0 8a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1z"];
})), iH, aH = o((() => {
	iH = ["M11 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zm0 11a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), oH, sH = o((() => {
	oH = ["M2 16a2 2 0 1 1 0 4 2 2 0 0 1 0-4m16 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m-8-4a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 8a2 2 0 1 1 0 4 2 2 0 0 1 0-4m16 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m-8-4a2 2 0 1 1 0 4 2 2 0 0 1 0-4M2 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4m16 0a2 2 0 1 1 0 4 2 2 0 0 1 0-4"];
})), cH, lH = o((() => {
	cH = ["M2 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m16 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m-8 4c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), uH, dH = o((() => {
	uH = ["M0 1a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm7 0a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1zm8 0a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-3a1 1 0 0 1-1-1z"];
})), fH, pH = o((() => {
	fH = ["M0 1a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 7a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 8a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), mH, hH = o((() => {
	mH = ["M0 12a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zM0 1a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm7 0a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1zm8 0a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-3a1 1 0 0 1-1-1z"];
})), gH, _H = o((() => {
	gH = ["M0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm11 0a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1zM0 12a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), vH, yH = o((() => {
	vH = ["M0 1a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm11 0a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1z"];
})), bH, xH = o((() => {
	bH = ["M0 1a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm0 11a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"];
})), SH, CH = o((() => {
	SH = ["M10.551 1.127a1.26 1.26 0 0 0-1.102 0L.456 5.89c-.608.309-.608.913 0 1.222l8.993 4.762c.334.17.767.17 1.102 0l8.992-4.762c.61-.309.61-.913 0-1.222zM18 6.5l.016 4.514c.002.548.447.99.994.99a.99.99 0 0 0 .99-.99V6.5zM3.366 10.033l6.401 3.358a.5.5 0 0 0 .465 0l6.406-3.358a.25.25 0 0 1 .366.221v5.109a.25.25 0 0 1-.139.224l-6.64 3.302a.5.5 0 0 1-.446 0l-6.64-3.302A.25.25 0 0 1 3 15.363v-5.108a.25.25 0 0 1 .366-.222"];
})), wH, TH = o((() => {
	wH = ["M8.7 4.7C7.4 6 6.5 7.9 6.5 10s.8 4 2.2 5.3c-.8.5-1.7.7-2.7.7-3.3 0-6-2.7-6-6s2.7-6 6-6c1 0 1.9.2 2.7.7M14 4c3.3 0 6 2.7 6 6s-2.7 6-6 6c-1 0-1.9-.2-2.7-.7 1.3-1.3 2.2-3.2 2.2-5.3s-.8-3.9-2.2-5.3C12.1 4.2 13 4 14 4m.6 2.05c.55 1.2.86 2.54.86 3.95s-.31 2.75-.86 3.95c1.9-.31 3.36-1.96 3.36-3.95S16.5 6.36 14.6 6.05M10 5.5C8.8 6.7 8 8.2 8 10s.8 3.3 2 4.4c1.2-1.1 2-2.7 2-4.5s-.8-3.3-2-4.4"];
})), EH, DH = o((() => {
	EH = ["M.833 16h8.334c.458 0 .833-.45.833-1s-.375-1-.833-1H.833C.375 14 0 14.45 0 15s.375 1 .833 1M1 11h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m15 2c0 .28.11.53.29.71l.3.29H13c-.55 0-1 .45-1 1s.45 1 1 1h3.59l-.29.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l2-2c.18-.19.29-.44.29-.71 0-.28-.11-.53-.29-.71l-2-2A1 1 0 0 0 17 12a.99.99 0 0 0-1 1M1 6h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1"];
})), OH, kH = o((() => {
	OH = ["m7.162 10 9.154 3.052a1 1 0 0 1-.632 1.897l-12-4c-.912-.304-.912-1.594 0-1.897l12-4a1 1 0 0 1 .632 1.897z"];
})), AH, jH = o((() => {
	AH = ["M16.316 11.051 7.162 8l9.154-3.051a1 1 0 1 0-.632-1.898l-12 4c-.912.304-.912 1.594 0 1.898l12 4a1 1 0 1 0 .632-1.898M16 15H4a1 1 0 1 0 0 2h12a1 1 0 1 0 0-2"];
})), MH, NH = o((() => {
	MH = ["M8.143 14.644 7.028 17.43c.919.368 1.922.57 2.972.57s2.053-.202 2.972-.57l-1.115-2.786A5 5 0 0 1 10 15a5 5 0 0 1-1.857-.356m-2.787-2.787A5 5 0 0 1 5 10c0-.656.126-1.283.356-1.857L2.57 7.028A8 8 0 0 0 2 10c0 1.05.202 2.053.57 2.972zm2.787-6.5A5 5 0 0 1 10 5c.656 0 1.283.126 1.857.356l1.115-2.786A8 8 0 0 0 10 2c-1.05 0-2.053.202-2.972.57zm6.5 2.786c.23.574.357 1.2.357 1.857 0 .656-.126 1.283-.356 1.857l2.786 1.115c.368-.919.57-1.922.57-2.972s-.202-2.053-.57-2.972zM10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6m0 7C4.477 20 0 15.523 0 10S4.477 0 10 0s10 4.477 10 10-4.477 10-10 10"];
})), PH, FH = o((() => {
	PH = ["M6.33 13.39c0 .34.27.61.6.61h6.13c.33 0 .6-.27.6-.61C14.03 9.78 16 9.4 16 6.09 16 2.72 13.31 0 10 0S4 2.72 4 6.09c0 3.31 1.97 3.69 2.33 7.3M13 15H7c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1m-1 3H8c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1"];
})), IH, LH = o((() => {
	IH = ["M9 11H6a1 1 0 0 1-1-1L5.91.9a1 1 0 0 1 .995-.9h6.257a.84.84 0 0 1 .778 1.15L11.2 8h2.978a.822.822 0 0 1 .748 1.162l-4.764 10.481A.608.608 0 0 1 9 19.392z"];
})), RH, zH = o((() => {
	RH = ["m10.85 11.98-4.44 4.44-1 1c-.36.36-.86.58-1.41.58-1.1 0-2-.9-2-2 0-.55.22-1.05.59-1.41l5.44-5.44C7.69 9.06 7.36 9 7 9c-1.11 0-2.09.46-2.82 1.18l-.01-.01-3 3 .01.01C.46 13.91 0 14.89 0 16c0 2.21 1.79 4 4 4 1.11 0 2.09-.46 2.82-1.18l.01.01 3-3-.01-.01C10.54 15.09 11 14.11 11 13c0-.36-.06-.69-.15-1.02M20 4c0-2.21-1.79-4-4-4-1.11 0-2.09.46-2.82 1.18l-.01-.01-3 3 .01.01C9.46 4.91 9 5.89 9 7c0 .36.06.69.15 1.02l4.44-4.44 1-1c.36-.36.86-.58 1.41-.58 1.1 0 2 .9 2 2 0 .55-.22 1.05-.59 1.41l-5.44 5.44c.34.09.67.15 1.03.15 1.11 0 2.09-.46 2.82-1.18l.01.01 3-3-.01-.01C19.54 6.09 20 5.11 20 4M5 14a1.003 1.003 0 0 0 1.71.71l8-8a1.003 1.003 0 0 0-1.42-1.42l-2 2-2 2-2 2-2 2c-.18.18-.29.43-.29.71"];
})), BH, VH = o((() => {
	BH = ["M1.1 1A1.1 1.1 0 0 0 0 2.1v10.8A1.1 1.1 0 0 0 1.1 14H3a1 1 0 1 0 0-2H2V3h11v9H9a1 1 0 1 0 0 2h4.9a1.1 1.1 0 0 0 1.1-1.1V2.1A1.1 1.1 0 0 0 13.9 1zm5 18A1.1 1.1 0 0 1 5 17.9V7.1A1.1 1.1 0 0 1 6.1 6H11a1 1 0 1 1 0 2H7v9h11V8h-1a1 1 0 1 1 0-2h1.9A1.1 1.1 0 0 1 20 7.1v10.8a1.1 1.1 0 0 1-1.1 1.1z"];
})), HH, UH = o((() => {
	HH = ["M1.03 1C.46 1 0 1.46 0 2.03v.95C0 3.54.46 4 1.03 4h17.95C19.54 4 20 3.54 20 2.97v-.94C20 1.46 19.54 1 18.97 1zM0 17.97C0 18.54.46 19 1.03 19h17.95c.56 0 1.03-.46 1.03-1.03v-.95c0-.56-.46-1.03-1.03-1.03H1.03C.46 16 0 16.46 0 17.03zm0-5C0 13.54.46 14 1.03 14h17.95c.56 0 1.03-.46 1.03-1.03v-.95c0-.56-.46-1.03-1.03-1.03H1.03C.46 11 0 11.46 0 12.03zm0-5C0 8.54.46 9 1.03 9h17.95C19.54 9 20 8.54 20 7.97v-.94C20 6.46 19.54 6 18.97 6H1.03C.46 6 0 6.46 0 7.03z"];
})), WH, GH = o((() => {
	WH = ["M0 2.973v-.936C0 1.468.46 1.01 1.029 1H7.97C8.541 1 9 1.468 9 2.027v.946C9 3.542 8.53 4 7.971 4H1.03C.459 4 0 3.542 0 2.973m0 5v-.936C0 6.468.46 6.01 1.029 6H7.97C8.541 6 9 6.468 9 7.027v.946C9 8.542 8.53 9 7.971 9H1.03C.459 9 0 8.542 0 7.973m0 5v-.936C0 11.468.46 11.01 1.029 11H7.97c.571 0 1.03.468 1.03 1.027v.946C9 13.542 8.53 14 7.971 14H1.03C.459 14 0 13.542 0 12.973m0 5v-.936C0 16.468.46 16.01 1.029 16H7.97c.571 0 1.03.468 1.03 1.027v.946C9 18.542 8.53 19 7.971 19H1.03C.459 19 0 18.542 0 17.973m11-15v-.936c0-.569.46-1.027 1.029-1.037h6.942C19.541 1 20 1.468 20 2.027v.946C20 3.542 19.53 4 18.971 4H12.03C11.459 4 11 3.542 11 2.973m0 5v-.936c0-.569.46-1.027 1.029-1.037h6.942C19.541 6 20 6.468 20 7.027v.946C20 8.542 19.53 9 18.971 9H12.03C11.459 9 11 8.542 11 7.973m0 5v-.936c0-.569.46-1.027 1.029-1.037h6.942c.57 0 1.029.468 1.029 1.027v.946c0 .569-.47 1.027-1.029 1.027H12.03c-.57 0-1.029-.458-1.029-1.027m0 5v-.936c0-.569.46-1.027 1.029-1.037h6.942c.57 0 1.029.468 1.029 1.027v.946c0 .569-.47 1.027-1.029 1.027H12.03c-.57 0-1.029-.458-1.029-1.027"];
})), KH, qH = o((() => {
	KH = ["M8 6H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1m0 5H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m0 5H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1M8 1H1c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1m11 0h-7c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1"];
})), JH, YH = o((() => {
	JH = ["M10 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m9 1h-1.07c-.45-3.61-3.32-6.45-6.93-6.91V1c0-.55-.45-1-1-1S9 .45 9 1v1.09C5.39 2.55 2.52 5.39 2.07 9H1c-.55 0-1 .45-1 1s.45 1 1 1h1.07c.45 3.61 3.32 6.45 6.93 6.91V19c0 .55.45 1 1 1s1-.45 1-1v-1.09c3.61-.46 6.48-3.29 6.93-6.91H19c.55 0 1-.45 1-1s-.45-1-1-1m-4 2h.9a5.98 5.98 0 0 1-4.9 4.91V15c0-.55-.45-1-1-1s-1 .45-1 1v.91A5.98 5.98 0 0 1 4.1 11H5c.55 0 1-.45 1-1s-.45-1-1-1h-.9A5.98 5.98 0 0 1 9 4.09V5c0 .55.45 1 1 1s1-.45 1-1v-.91A5.98 5.98 0 0 1 15.9 9H15c-.55 0-1 .45-1 1s.45 1 1 1"];
})), XH, ZH = o((() => {
	XH = ["M15.93 9H14V4.99c0-2.21-1.79-4-4-4s-4 1.79-4 4V9H3.93c-.55 0-.93.44-.93.99v8c0 .55.38 1.01.93 1.01h12c.55 0 1.07-.46 1.07-1.01v-8c0-.55-.52-.99-1.07-.99M8 9V4.99c0-1.1.9-2 2-2s2 .9 2 2V9z"];
})), QH, $H = o((() => {
	QH = ["M9.988 2a1 1 0 0 1 .999 1v4h3.995V5l-1.145-1.146A.5.5 0 0 1 14.19 3h3.581a.5.5 0 0 1 .353.854L16.979 5v2c2.996 1.333 4.494 4 .999 7l1.145 1.146a.5.5 0 0 1-.353.854h-2.496a.53.53 0 0 1-.444-.252c-.925-1.433-3.111-3.084-5.687.058a.52.52 0 0 1-.399.194h-.488a.53.53 0 0 1-.42-.218c-1.061-1.429-3.359-3.043-5.684.008a.52.52 0 0 1-.412.21H1V3a1 1 0 0 1 .998-1zm-6.99 2-.001 5h2.996V4zM8.99 4H6.992v5H8.99zM5.993 19a2 2 0 0 1-1.997-2 1.999 1.999 0 1 1 3.995 0 2 2 0 0 1-1.998 2m0-1a1.001 1.001 0 1 0 .063-2.001A1.001 1.001 0 0 0 5.993 18m6.991 1a2 2 0 0 1-1.997-2 1.999 1.999 0 1 1 3.995 0 2 2 0 0 1-1.998 2m0-1a1.001 1.001 0 0 0 .392-1.932 1.001 1.001 0 0 0-1.079 1.628 1 1 0 0 0 .687.304"];
})), eU, tU = o((() => {
	eU = ["M19 0h-8c-.55 0-1 .45-1 1s.45 1 1 1h7v16h-7c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-4 10c0-.28-.11-.53-.29-.71l-5-5a1.003 1.003 0 0 0-1.42 1.42L11.59 9H1c-.55 0-1 .45-1 1s.45 1 1 1h10.59L8.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l5-5c.18-.18.29-.43.29-.71"];
})), nU, rU = o((() => {
	nU = ["m19.71 9.29-5-5a1.003 1.003 0 0 0-1.42 1.42L16.59 9H6c-.55 0-1 .45-1 1s.45 1 1 1h10.59l-3.29 3.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l5-5c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M9 18H2V2h7c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1"];
})), iU, aU = o((() => {
	iU = ["M10 0a1 1 0 0 0-1 1v2H5V2a1 1 0 0 0-2 0v1H2a1 1 0 0 0 0 2h1v2H2a1 1 0 0 0 0 2h4a1 1 0 0 0 0-2H5V5h4v14a1 1 0 1 0 2 0V5h4v2h-1a1 1 0 1 0 0 2h4a1 1 0 1 0 0-2h-1V5h1a1 1 0 1 0 0-2h-1V2a1 1 0 1 0-2 0v1h-4V1a1 1 0 0 0-1-1"];
})), oU, sU = o((() => {
	oU = ["M20 1.1a.976.976 0 0 0-.83-.88C15.15-.43 12.07.34 10 2.5 7.93.34 4.85-.43.84.22.37.3.03.67 0 1.1v15.01c0 .07 0 .14.01.21.09.52.61.88 1.15.79 3.85-.62 6.4.16 8 2.46.02.02.03.04.05.07.02.02.04.04.06.07l.01.01a1 1 0 0 0 .28.19c.01 0 .01.01.02.01.03.01.07.03.1.04.01 0 .02.01.04.01.03.01.07.02.1.02.01 0 .02 0 .04.01H10c.04 0 .09 0 .13-.01.01 0 .03 0 .04-.01.03-.01.06-.01.1-.02.01 0 .03-.01.04-.01.03-.01.07-.02.1-.04.01 0 .02-.01.03-.01.07-.03.13-.07.19-.11.01 0 .01-.01.02-.01.02-.02.04-.03.06-.05.01-.01.02-.02.03-.02l.05-.05c.01-.01.02-.02.02-.03.01-.02.02-.03.04-.05 1.61-2.3 4.15-3.09 8-2.46.54.09 1.06-.26 1.15-.79-.01-.05 0-.09 0-.13zM9 16.63c-1.78-1.31-4.12-1.83-7-1.55V2c3.26-.37 5.51.39 7 2.35zm9-1.56c-2.88-.28-5.22.24-7 1.55V4.34c1.49-1.96 3.74-2.71 7-2.35z"];
})), cU, lU = o((() => {
	cU = ["M1 12h4.34l2-2H1c-.55 0-1 .45-1 1s.45 1 1 1m16.77-3.94 1.65-1.65c.36-.36.58-.86.58-1.41 0-1.1-.9-2-2-2-.55 0-1.05.22-1.41.59l-1.65 1.65zM1 4h12.34l2-2H1c-.55 0-1 .45-1 1s.45 1 1 1M0 15c0 .55.45 1 1 1h.34l2-2H1c-.55 0-1 .45-1 1m1-7h8.34l2-2H1c-.55 0-1 .45-1 1s.45 1 1 1m18 2h-.34l-2 2H19c.55 0 1-.45 1-1s-.45-1-1-1m0 4h-4.34l-2 2H19c.55 0 1-.45 1-1s-.45-1-1-1M4 19l4.41-1.59-2.81-2.79zM14.23 5.94l-7.65 7.65 2.83 2.83 7.65-7.65z"];
})), uU, dU = o((() => {
	uU = ["M17 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2m0 2a3 3 0 0 1-2.73-1.754 4 4 0 0 0-.617.264c-.884.465-1.92 1.418-2.605 3.49.685 2.072 1.721 3.025 2.605 3.49q.315.164.617.264a3 3 0 1 1-.165 2.034 6.3 6.3 0 0 1-1.383-.528c-.983-.518-1.948-1.364-2.722-2.705-.774 1.34-1.739 2.187-2.722 2.705a6.3 6.3 0 0 1-1.383.528A3 3 0 0 1 0 15a3 3 0 0 1 5.73-1.246q.302-.1.617-.264c.884-.465 1.92-1.418 2.605-3.49-.685-2.072-1.721-3.025-2.605-3.49a4 4 0 0 0-.617-.264 3 3 0 1 1 .165-2.034c.433.11.904.276 1.383.528.983.518 1.948 1.364 2.722 2.705.774-1.34 1.739-2.187 2.722-2.705a6.3 6.3 0 0 1 1.383-.528A3 3 0 0 1 20 5a3 3 0 0 1-3 3M4 5a1 1 0 1 0-2 0 1 1 0 0 0 2 0m12 10a1 1 0 1 0 2 0 1 1 0 0 0-2 0M3 14a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), fU, pU = o((() => {
	fU = ["M3 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2m0 4a3 3 0 1 1 2.838-3.976c.633.042 1.491.158 2.347.476 1.402.523 2.868 1.625 3.296 3.807.259 1.318 1.085 1.966 2.032 2.318q.353.132.722.21a3 3 0 1 1 0 2.33c-.238.052-.482.12-.722.21-.947.352-1.773 1-2.032 2.318-.429 2.182-1.894 3.284-3.296 3.807-.856.318-1.714.434-2.347.476a3.001 3.001 0 1 1-.019-2.004 6.2 6.2 0 0 0 1.668-.347c.947-.352 1.773-1 2.032-2.318.323-1.644 1.234-2.675 2.264-3.307-1.03-.632-1.941-1.663-2.264-3.307-.259-1.318-1.085-1.966-2.032-2.318a6.2 6.2 0 0 0-1.667-.347A3 3 0 0 1 3 6m13 4a1 1 0 1 0 2 0 1 1 0 0 0-2 0M2 17a1 1 0 1 0 2 0 1 1 0 0 0-2 0"];
})), mU, hU = o((() => {
	mU = ["m19.54 4.18.01-.02-6-4-.01.02C13.39.08 13.21 0 13 0s-.39.08-.54.18l-.01-.02L7 3.8 1.55.17l-.01.01A.97.97 0 0 0 1 0C.45 0 0 .45 0 1v14c0 .35.19.64.46.82l-.01.02 6 4 .01-.02c.15.1.33.18.54.18s.39-.08.54-.18l.01.02L13 16.2l5.45 3.63.01-.02c.15.11.33.19.54.19.55 0 1-.45 1-1V5c0-.35-.19-.64-.46-.82M6 17.13l-4-2.67V2.87l4 2.67zm6-2.67-4 2.67V5.54l4-2.67zm6 2.67-4-2.67V2.87l4 2.67z"];
})), gU, _U = o((() => {
	gU = ["M18 9.22v7.91l-4-2.67V9.22c-.61-.55-1-1.33-1-2.22-.35 0-.69-.07-1-.18v7.65l-4 2.67V5.54l2.02-1.35c0-.06-.02-.13-.02-.19 0-1.66 1.34-3 3-3 0-.34.07-.66.17-.97C13.12.02 13.06 0 13 0c-.21 0-.39.08-.54.18l-.01-.02L7 3.8 1.55.17l-.01.01A.97.97 0 0 0 1 0C.45 0 0 .45 0 1v14c0 .35.19.64.46.82l-.01.02 6 4 .01-.02c.15.1.33.18.54.18s.39-.08.54-.18l.01.02L13 16.2l5.45 3.63.01-.02c.15.11.33.19.54.19.55 0 1-.45 1-1V6.82c-.31.11-.65.18-1 .18 0 .89-.39 1.67-1 2.22M6 17.13l-4-2.67V2.87l4 2.67zM12 4c0 .55.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V5h2c.55 0 1-.45 1-1s-.45-1-1-1h-2V1c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1"];
})), vU, yU = o((() => {
	vU = ["M10 0C6.13 0 3 2.98 3 6.67 3 10.35 10 20 10 20s7-9.65 7-13.33S13.86 0 10 0m0 10c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3"];
})), bU, xU = o((() => {
	bU = ["M18 2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm-8 4.818c0-1.043-1.303-1.484-1.943-.707l-.06.08L6.5 8.34 5.003 6.19l-.06-.079C4.303 5.334 3 5.775 3 6.818V13a1 1 0 1 0 2 0V9.687l.269.386.12.15a1.5 1.5 0 0 0 2.342-.15L8 9.687V13a1 1 0 1 0 2 0zM14 6a1 1 0 0 0-1 1v3.236l-.731-.877-.07-.075a1.001 1.001 0 0 0-1.53 1.275l.062.082 2.347 2.815.084.089a1 1 0 0 0 1.671.007q.045-.045.089-.096l2.347-2.815.061-.082a1.001 1.001 0 0 0-1.53-1.275l-.069.075-.731.877V7a1 1 0 0 0-1-1"];
})), SU, CU = o((() => {
	SU = ["M19 0h-5c-.55 0-1 .45-1 1s.45 1 1 1h2.59L11.3 7.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L18 3.41V6c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1M8 11c-.28 0-.53.11-.71.29L2 16.59V14c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1H3.41l5.29-5.29c.19-.18.3-.43.3-.71 0-.55-.45-1-1-1"];
})), wU, TU = o((() => {
	wU = ["M15 9c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m4-7H1c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1m-1 13-6-5-2 2-4-5-4 8V4h16z"];
})), EU, DU = o((() => {
	EU = ["M1 6h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m18 3H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0 5H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), OU, kU = o((() => {
	OU = ["M8 6h11c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1M4 6c-.28 0-.53.11-.71.29l-3 3C.11 9.47 0 9.72 0 10s.11.53.29.71l3 3A1.003 1.003 0 0 0 5 13V7c0-.55-.45-1-1-1m15 8H8c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m0-5H8c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1"];
})), AU, jU = o((() => {
	AU = ["M12 9H1c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m0 5H1c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m0-10H1c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m7.71 5.29-3-3A1.003 1.003 0 0 0 15 7v6a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), MU, NU = o((() => {
	MU = ["M6.71 6.29a1.003 1.003 0 0 0-1.42 1.42L6.59 9H2V2h5v2.18c.42.15.8.39 1.11.7l.01-.01.88.89V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-4.76l-.88.88-.01-.01c-.31.31-.69.56-1.11.71V18H2v-7h4.59L5.3 12.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71zM19 0h-7c-.55 0-1 .45-1 1v4.76l.88-.88.01.01c.31-.31.69-.55 1.11-.7V2h5v7h-4.59l1.29-1.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3c-.18.18-.29.43-.29.71s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L13.41 11H18v7h-5v-2.18c-.42-.15-.8-.39-1.11-.7l-.01.01-.88-.89V19c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), PU, FU = o((() => {
	PU = ["M10 13c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m8-5c-.93 0-1.71.64-1.93 1.5H14V4c0-2.21-1.79-4-4-4S6 1.79 6 4v5.5H3.93C3.71 8.64 2.93 8 2 8c-1.1 0-2 .9-2 2s.9 2 2 2c.93 0 1.71-.64 1.93-1.5H6V16c0 2.21 1.79 4 4 4s4-1.79 4-4v-5.5h2.07c.22.86 1 1.5 1.93 1.5 1.1 0 2-.9 2-2s-.9-2-2-2m-5 8c0 1.66-1.34 3-3 3s-3-1.34-3-3V4c0-1.66 1.34-3 3-3s3 1.34 3 3zM10 3c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), IU, LU = o((() => {
	IU = ["M10 0a4 4 0 0 0-4 4v5a4 4 0 0 0 8 0V4a4 4 0 0 0-4-4M4 7a1 1 0 0 1 1 1v1a5 5 0 0 0 10 0V8a1 1 0 1 1 2 0v1a7 7 0 0 1-6 6.93V18h1a1 1 0 1 1 0 2H8a1 1 0 1 1 0-2h1v-2.07A7 7 0 0 1 3 9V8a1 1 0 0 1 1-1"];
})), RU, zU = o((() => {
	RU = ["M8 11H3c-.55 0-1 .45-1 1s.45 1 1 1h2.59L.3 18.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L7 14.41V17c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1M20 1a1.003 1.003 0 0 0-1.71-.71L13 5.59V3c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1h-2.59l5.29-5.29c.19-.18.3-.43.3-.71"];
})), BU, VU = o((() => {
	BU = ["M16 9H4c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1"];
})), HU, UU = o((() => {
	HU = ["M15 0H5c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-5 19c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m4-3H6V3h8z"];
})), WU, GU = o((() => {
	WU = ["M19 5c-.28 0-.53.11-.71.29L15 8.59V5c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h13c.55 0 1-.45 1-1v-3.59l3.29 3.29c.18.19.43.3.71.3.55 0 1-.45 1-1V6c0-.55-.45-1-1-1"];
})), KU, qU = o((() => {
	KU = ["M19 1a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm-1 4H2v12h16zm-3-3h-2v2h2zm3 0h-2v2h2z"];
})), JU, YU = o((() => {
	JU = ["M20 5v13a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V5zm-3-4h2a1 1 0 0 1 1 1v1h-3zm-2 2H0V2a1 1 0 0 1 1-1h14z"];
})), XU, ZU = o((() => {
	XU = ["M18.746 17H1.254A1.25 1.25 0 0 1 0 15.707c.07-1.927.278-5.273.894-8.196.325-1.544.76-2.947 1.333-3.957Q3.108 2.001 4.249 2c.88 0 1.541.357 2.081.92.547.571.961 1.345 1.327 2.151.103.226.21.477.317.726l.003.006c.245.57.482 1.12.706 1.524.338.609.785 1.173 1.471 1.173 1.046 0 1.653-.667 2.147-1.245l.003-.003.135-.157c.283-.32.566-.616.925-.835.35-.213.785-.36 1.383-.36.628 0 1.239.358 1.832 1.042.587.676 1.114 1.623 1.576 2.688.853 1.967 1.458 4.272 1.814 5.848A1.25 1.25 0 0 1 18.746 17"];
})), QU, $U = o((() => {
	QU = ["M19 14.15A9.94 9.94 0 0 1 9.94 20C4.45 20 0 15.55 0 10.06 0 6.03 2.4 2.56 5.85 1a9.8 9.8 0 0 0-.88 4.09c0 5.49 4.45 9.94 9.94 9.94 1.46 0 2.84-.31 4.09-.88"];
})), eW, tW = o((() => {
	eW = ["M3.5 8a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5m7 0a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5m7 0a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5"];
})), nW, rW = o((() => {
	nW = ["M20 16H4l7-11h1l2 2h1zm-4-5-1.5-3h-1l-1-1-1-1L8 11.5l3-1.5 1 1 1-1zM8.055 8 2.79 16H0l7-8z"];
})), iW, aW = o((() => {
	iW = ["m19.71 9.29-3-3a1.003 1.003 0 0 0-1.42 1.42L16.59 9H11V3.41l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-3-3C10.53.11 10.28 0 10 0s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L9 3.41V9H3.41L4.7 7.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 9.47 0 9.72 0 10s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L3.41 11H9v5.59L7.71 15.3A.97.97 0 0 0 7 15a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3a1.003 1.003 0 0 0-1.42-1.42L11 16.59V11h5.59l-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), oW, sW = o((() => {
	oW = ["M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18h-.07c-.05-.2-.12-.42-.22-.67-.46-1.05-2.68-1.75-4.16-2.4s-1.28-1.05-1.33-1.59c-.01-.07-.01-.15-.01-.23.51-.45.92-1.07 1.19-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.34-.07.54-.44.61-.78.08-.14.23-.48.2-.87-.05-.5-.25-.73-.47-.82v-.09c0-.63-.06-1.55-.17-2.15-.02-.17-.06-.33-.11-.5a3.67 3.67 0 0 0-1.29-1.86C11.7 3.25 10.81 3 10.02 3s-1.68.25-2.31.73c-.61.47-1.07 1.13-1.29 1.86-.05.16-.09.33-.11.5-.12.6-.17 1.51-.17 2.14v.08c-.24.09-.44.32-.49.83-.04.39.12.73.2.87.08.35.28.72.63.78q.06.255.15.48c0 .01.01.02.01.03l.01.01c.27.72.7 1.35 1.22 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.38 1.59s-3.7 1.35-4.16 2.4c-.12.27-.18.49-.23.69H2V2h16z"];
})), cW, lW = o((() => {
	cW = ["M19 3H7c-.55 0-1 .45-1 1v1h12v6h1c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1m-6 6H1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-6c0-.55-.45-1-1-1m-1 6H2v-4h10zm4-9H4c-.55 0-1 .45-1 1v1h12v6h1c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1"];
})), uW, dW = o((() => {
	uW = ["M19 0c-.08 0-.16.03-.24.05V.03l-12 3v.02C6.33 3.16 6 3.53 6 4v11.35c-.59-.22-1.27-.35-2-.35-2.21 0-4 1.12-4 2.5S1.79 20 4 20c1.94 0 3.55-.86 3.92-2H8V7.78l10-2.5v7.07c-.59-.22-1.27-.35-2-.35-2.21 0-4 1.12-4 2.5s1.79 2.5 4 2.5c1.94 0 3.55-.86 3.92-2H20V1c0-.55-.45-1-1-1"];
})), fW, pW = o((() => {
	fW = ["M2 2c.55 0 1 .45 1 1v5c0 2.21 1.79 4 4 4h8.59L13.3 9.71A.97.97 0 0 1 13 9a1.003 1.003 0 0 1 1.71-.71l4 4c.18.18.29.43.29.71s-.11.53-.29.71l-4 4a1.003 1.003 0 0 1-1.42-1.42l2.3-2.29H7c-3.31 0-6-2.69-6-6V3c0-.55.45-1 1-1"];
})), mW, hW = o((() => {
	mW = ["M13 5c-.6 0-1-.4-1-1 0-.5.4-1 1-1h2V1c0-.6.4-1 1-1 .5 0 1 .4 1 1v2h2c.5 0 1 .4 1 1s-.5 1-1 1h-2v2c0 .6-.5 1-1 1-.6 0-1-.4-1-1V5zm-2.14 1.14C10.26 5.538 10 4.754 10 4c0-1.472 1.168-3 3-3H1c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3v4a1.003 1.003 0 0 0 1.71.71l4.7-4.71H19c.55 0 1-.45 1-1V6.823A3 3 0 0 1 19 7c0 1.832-1.528 3-3 3-.755 0-1.539-.26-2.14-.86C13.26 8.538 13 7.753 13 7c-.755 0-1.539-.26-2.14-.86"];
})), gW, _W = o((() => {
	gW = ["M18.7 13.7c.5 0 1 .4 1 1 0 .257-.073.44-.22.614l-.08.086-4 4c-.2.2-.4.3-.7.3-.6 0-1-.5-1-1 0-.257.073-.44.22-.614L14 18l4-4c.2-.2.4-.3.7-.3M1.8 0l8.378 2.982A3.003 3.003 0 0 0 13 7a3.003 3.003 0 0 0 3.877 2.87l.723 2.53.049.06a.4.4 0 0 1 .051.24c0 .167-.07.403-.208.593l-.092.107-4 4c-.2.2-.4.3-.7.3-.075 0-.15-.056-.225-.084L12.4 17.6l-7-2-.112-.042c-.223-.094-.431-.244-.542-.45L4.7 15 0 1.8l.5-.6L7 7.7c-.2.3-.3.6-.3 1 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2a1.7 1.7 0 0 0-.871.22L7.7 7 1.2.5zM16 0c.55 0 1 .45 1 1v2h2c.55 0 1 .45 1 1s-.45 1-1 1h-2v2c0 .432-.278.803-.664.941l-.01.004A1 1 0 0 1 16 8c-.55 0-1-.45-1-1V5h-2c-.55 0-1-.45-1-1l.007-.116C12.065 3.388 12.489 3 13 3h2V1c0-.55.45-1 1-1"];
})), vW, yW = o((() => {
	vW = ["M8 0H1C.45 0 0 .45 0 1v7c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m0 11H1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h7c.55 0 1-.45 1-1v-7c0-.55-.45-1-1-1m6 7h-1v-1c0-.55-.45-1-1-1s-1 .45-1 1v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1s-.45-1-1-1m5-7h-2c-.55 0-1 .45-1 1s.45 1 1 1h1v1c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1m0-11h-7c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-5 11h-2c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1s1-.45 1-1v-1h1c.55 0 1-.45 1-1s-.45-1-1-1m5 5c-.55 0-1 .45-1 1v1h-1c-.55 0-1 .45-1 1s.45 1 1 1h2c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1"];
})), bW, xW = o((() => {
	bW = ["M11.513 5.663A2 2 0 0 0 13 9h1v1a2 2 0 1 0 4 0v-.733l1.5.833c.3.2.5.5.5.9s-.2.7-.5.9l-9 5c-.2.1-.3.1-.5.1s-.3 0-.5-.1l-9-5c-.3-.2-.5-.5-.5-.9s.2-.7.5-.9l9-5c.2-.1.3-.1.5-.1s.3 0 .5.1zM17 6h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V8h-2a1 1 0 1 1 0-2h2V4a1 1 0 1 1 2 0z"];
})), SW, CW = o((() => {
	SW = ["M17 3h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V5h-2a1 1 0 1 1 0-2h2V1a1 1 0 1 1 2 0zm-1.252 5.984L10.5 11.9c-.2.1-.3.1-.5.1s-.3 0-.5-.1l-9-5C.2 6.7 0 6.4 0 6s.2-.7.5-.9l9-5c.2-.1.3-.1.5-.1s.3 0 .5.1L13.92 2H13a2 2 0 1 0 0 4h1v1a2 2 0 0 0 1.748 1.984m2.07-1.15C17.935 7.58 18 7.298 18 7V6h1c.353 0 .684-.091.972-.251q.027.117.028.251c0 .4-.2.7-.5.9zM19 9c.6 0 1 .4 1 1 0 .4-.2.7-.5.9l-9 5c-.2.1-.3.1-.5.1s-.3 0-.5-.1l-9-5c-.3-.2-.5-.5-.5-.9 0-.6.4-1 1-1 .2 0 .3 0 .5.1l8.5 4.8 8.5-4.8c.2-.1.3-.1.5-.1m0 4c.6 0 1 .4 1 1 0 .4-.2.7-.5.9l-9 5c-.2.1-.3.1-.5.1s-.3 0-.5-.1l-9-5c-.3-.2-.5-.5-.5-.9 0-.6.4-1 1-1 .2 0 .3 0 .5.2l8.5 4.7 8.5-4.8c.2-.1.3-.1.5-.1"];
})), wW, TW = o((() => {
	wW = ["M14.5 12a2.5 2.5 0 0 0-2.45 2h-7.1a2.5 2.5 0 1 0 0 1h7.1a2.5 2.5 0 1 0 2.45-3M19 5h-2V3c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V7h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), EW, DW = o((() => {
	EW = ["M12 4c0 .6.4 1 1 1h2v2c0 .6.4 1 1 1 .5 0 1-.4 1-1V5h2c.5 0 1-.4 1-1s-.5-1-1-1h-2V1c0-.6-.5-1-1-1-.6 0-1 .4-1 1v2h-2c-.6 0-1 .5-1 1m7 3c0 1.7-1.3 3-3 3s-3-1.3-3-3c-1.7 0-3-1.3-3-3s1.3-3 3-3c0-.2 0-.4.1-.5-1-.3-2-.5-3.1-.5C4.5 0 0 4.5 0 10s4.5 10 10 10 10-4.5 10-10c0-1.1-.2-2.1-.5-3z"];
})), OW, kW = o((() => {
	OW = ["M11.41 15.92c-1.46-.65-1.26-1.05-1.31-1.59-.01-.07-.01-.15-.01-.23.5-.45.91-1.07 1.18-1.78 0 0 .01-.04.02-.05.06-.15.11-.32.15-.48.33-.07.53-.44.6-.78.08-.14.23-.48.2-.87-.05-.5-.24-.73-.47-.82v-.09c0-.63-.06-1.55-.17-2.15-.02-.17-.06-.33-.11-.5-.22-.73-.67-1.4-1.27-1.86C9.58 4.25 8.7 4 7.92 4s-1.66.25-2.28.73c-.61.47-1.06 1.13-1.27 1.86-.05.16-.08.33-.11.5-.12.6-.18 1.51-.18 2.14v.08c-.23.09-.43.32-.48.83-.04.39.12.73.2.87.08.35.28.72.62.78q.06.255.15.48c0 .01.01.02.01.03l.01.01c.27.72.69 1.35 1.21 1.8 0 .07-.01.14-.01.21-.05.54.1.94-1.36 1.59S.77 17.26.32 18.31C-.14 19.38.04 20 .04 20h15.75s.18-.62-.27-1.67c-.45-1.06-2.65-1.75-4.11-2.41M18.87 3h-2V1c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V5h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), AW, jW = o((() => {
	AW = ["M11.95 10.23c.16-.18.22-.22.46-.22h1.48c.25 0 .47.08.59.33.1.2.09.41-.05.66l-2.71 3.58L14.88 19c.13.21.16.46.03.69-.12.21-.34.31-.57.31H12.7c-.31 0-.56-.17-.7-.44l-1.9-2.67-1.93 2.68c-.15.27-.42.43-.73.43H5.98c-.25 0-.47-.08-.59-.33-.1-.2-.09-.41.05-.66l3.09-4.35L4.26 9H3v4.32c0 .41-.3.69-.7.69H.7c-.41 0-.7-.28-.7-.69V.69C0 .28.3 0 .7 0h4.42c.71 0 1.36.1 1.94.3.59.2 1.11.49 1.54.87.44.38.78.84 1.02 1.39.25.54.37 1.13.37 1.77 0 1.01-.28 1.88-.84 2.6-.43.54-1.35 1.29-2 1.59l3.09 3.94zM4.71 6.04c.71 0 1.45-.16 1.81-.46.33-.28.5-.69.5-1.25s-.17-.97-.5-1.25c-.35-.3-1.1-.46-1.81-.46h-1.7v3.42zM19 3c.55 0 1 .45 1 1s-.45 1-1 1h-2v2c0 .55-.45 1-1 1s-1-.45-1-1V5h-2c-.55 0-1-.45-1-1s.45-1 1-1h2V1c0-.55.45-1 1-1s1 .45 1 1v2z"];
})), MW, NW = o((() => {
	MW = ["M12 4c0 .6.4 1 1 1h2v2c0 .6.4 1 1 1 .5 0 1-.4 1-1V5h2c.5 0 1-.4 1-1s-.5-1-1-1h-2V1c0-.6-.5-1-1-1-.6 0-1 .4-1 1v2h-2c-.6 0-1 .5-1 1m3.796 5.994c-1.05 2.868-2.974 5.313-5.796 7.374V0Q4 4.286 1 4.286q0 10 9 15.714 6.95-4.413 8.534-11.383a3.07 3.07 0 0 1-2.738 1.377"];
})), PW, FW = o((() => {
	PW = ["M19 3h-2V1c0-.55-.45-1-1-1s-1 .45-1 1v2h-2c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V5h2c.55 0 1-.45 1-1s-.45-1-1-1M5 7.5v1c0 .28.22.5.5.5s.5-.22.5-.5V8h2v7h-.5c-.28 0-.5.22-.5.5s.22.5.5.5h2c.28 0 .5-.22.5-.5s-.22-.5-.5-.5H9V8h2v.5c0 .28.22.5.5.5s.5-.22.5-.5v-1c0-.28-.22-.5-.5-.5h-6c-.28 0-.5.22-.5.5M16 9c-.55 0-1 .45-1 1v8H2V5h8c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1v15c0 .55.45 1 1 1h15c.55 0 1-.45 1-1v-9c0-.55-.45-1-1-1"];
})), IW, LW = o((() => {
	IW = ["M20 6s-2.98 2.43-6.12 2.19C13.52 5.31 12.05 0 6 0c0 0 2.41 2.99 2.16 6.12C5.27 6.49 0 7.97 0 14c0 0 2.98-2.43 6.11-2.19C6.47 14.69 7.94 20 14 20c0 0-2.42-2.99-2.16-6.13C14.73 13.51 20 12.02 20 6m-10 6c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2"];
})), RW, zW = o((() => {
	RW = ["m9.487 7 .532-3.196a1 1 0 0 1 1.962.392L11.513 7H16a1 1 0 0 1 0 2h-4.82l-.333 2H16a1 1 0 0 1 0 2h-5.487l-.532 3.196a1 1 0 0 1-1.962-.392L8.487 13H4a1 1 0 0 1 0-2h4.82l.333-2H4a1 1 0 1 1 0-2z"];
})), BW, VW = o((() => {
	BW = ["M10 20c1.1 0 2-.9 2-2H8c0 1.1.9 2 2 2m7-5c-.55 0-1-.45-1-1V8c0-2.61-1.67-4.81-4-5.63V2c0-1.1-.9-2-2-2S8 .9 8 2v.37C5.67 3.19 4 5.39 4 8v6c0 .55-.45 1-1 1s-1 .45-1 1 .45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1"];
})), HW, UW = o((() => {
	HW = ["M12.003 2.371 12 2.5a3 3 0 1 0 0 6 3 3 0 0 0 4 2.83V14c0 .55.45 1 1 1s1 .45 1 1-.45 1-1 1H3c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V8c0-2.61 1.67-4.81 4-5.63V2c0-1.1.9-2 2-2s2 .9 2 2v.37zM12 18c0 1.1-.9 2-2 2s-2-.9-2-2zm2-15.5a1 1 0 1 1 2 0v2h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0v-2h-2a1 1 0 1 1 0-2h2z"];
})), WW, GW = o((() => {
	WW = ["M12 18c0 1.1-.9 2-2 2s-2-.9-2-2zM10 0c.476 0 .914.168 1.258.448Q10.133 1.093 10 2.5q-.2 2.1 1.6 2.9Q10 7.2 10 8v1.2a2.8 2.8 0 0 0 2.8 2.8H16v2c0 .51.388.935.884.993L17 15c.55 0 1 .45 1 1s-.45 1-1 1H3c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V8c0-2.61 1.67-4.81 4-5.63V2c0-1.1.9-2 2-2m8 9.25v-.395a.75.75 0 0 0-.75-.75h-2.812L17.834 3.9A.75.75 0 0 0 18 3.43v-.68a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0-.75.75v.184c0 .414.336.75.75.75h2.813L12.22 7.831a1 1 0 0 0-.221.627v.792c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75"];
})), KW, qW = o((() => {
	KW = ["M10 20c1.1 0 2-.9 2-2H8c0 1.1.9 2 2 2m2-17.834A2.994 2.994 0 0 0 8 4.99c0 .808.319 1.557.876 2.114l2.97 2.99a2.99 2.99 0 0 0 4.154.072V14c0 .55.45 1 1 1s1 .45 1 1-.45 1-1 1H3c-.55 0-1-.45-1-1s.45-1 1-1 1-.45 1-1V8c0-2.61 1.67-4.81 4-5.63V2c0-1.1.9-2 2-2s2 .9 2 2zm1.26 6.514-2.97-2.99a.97.97 0 0 1-.29-.7c0-.55.44-1 .99-1 .27 0 .52.11.7.29l2.28 2.28 4.27-4.27a1 1 0 0 1 .7-.29c.55 0 1 .45 1 1 0 .28-.11.53-.3.7l-4.98 4.98a.99.99 0 0 1-1.4 0"];
})), JW, YW = o((() => {
	JW = ["M1.74 9.01h1.27V1h-.95c-.04.24-.12.45-.26.62-.13.17-.29.3-.47.41-.19.11-.4.18-.63.23-.23.04-.46.07-.71.07v1.03h1.75zm.43 7.93c.18-.14.37-.28.58-.43q.315-.21.63-.45c.21-.16.41-.33.61-.5.2-.18.37-.38.52-.59s.28-.45.37-.7.14-.54.14-.85c0-.25-.04-.52-.12-.8q-.12-.42-.39-.78c-.19-.24-.43-.44-.73-.59-.3-.17-.68-.25-1.12-.25-.41 0-.77.08-1.08.23-.32.16-.58.37-.8.64s-.38.59-.49.96-.16.77-.16 1.21h1.19c.01-.28.03-.53.08-.77s.12-.45.21-.62c.09-.18.22-.31.38-.42.16-.1.35-.15.59-.15.26 0 .47.05.63.14s.29.21.38.35q.135.21.18.45c.03.16.05.31.05.45-.01.31-.08.58-.22.81-.14.24-.32.45-.53.66-.22.2-.45.39-.71.57s-.51.36-.74.54c-.5.36-.89.78-1.17 1.27-.3.47-.45 1.04-.46 1.69H5v-1.14H1.43c.05-.17.14-.33.27-.49.13-.15.29-.3.47-.44M18 4.02H8c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-1c0-.56-.45-1-1-1m0 9H8c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-1c0-.56-.45-1-1-1"];
})), XW, ZW = o((() => {
	XW = ["M2.39 5.75c-.17.21-.38.39-.63.52s-.52.23-.83.29c-.3.05-.61.08-.93.08v1.24h2.49V15h1.49V4.98H2.73c-.05.31-.17.57-.34.77m17.2 4.71c-.27-.44-.65-.71-1.14-.82v-.02c.42-.16.72-.43.92-.79s.29-.79.29-1.27c0-.42-.08-.8-.23-1.12-.15-.33-.36-.59-.62-.8q-.39-.315-.87-.48c-.32-.11-.65-.16-.98-.16-.43 0-.82.08-1.16.25q-.51.24-.87.69c-.24.29-.43.64-.57 1.04s-.22.83-.23 1.3h1.39c-.01-.25.02-.49.07-.72.06-.23.14-.44.26-.63q.18-.285.45-.45c.18-.11.39-.17.63-.17.39 0 .71.12.96.37s.37.58.37.99c0 .29-.05.54-.16.74s-.25.36-.43.47-.38.19-.61.24-.46.06-.68.05v1.17q.42-.015.81.03c.26.03.5.1.71.21s.38.28.51.5.2.52.2.89c0 .55-.16.97-.47 1.27q-.465.45-1.17.45c-.55 0-.95-.19-1.23-.58-.27-.39-.4-.88-.38-1.46h-1.39q.015.75.21 1.38c.13.41.32.77.57 1.06s.56.52.93.68.8.24 1.3.24c.41 0 .79-.07 1.16-.21s.69-.33.96-.58c.28-.25.5-.56.66-.92a3 3 0 0 0 .24-1.23c0-.64-.14-1.17-.41-1.61M8.58 12.41c.21-.18.45-.36.7-.53.25-.18.5-.36.75-.56s.49-.41.73-.63c.23-.22.44-.47.63-.74.18-.27.33-.56.44-.88s.16-.67.16-1.07c0-.32-.05-.65-.14-1s-.25-.68-.47-.97c-.22-.3-.51-.55-.87-.74-.36-.2-.81-.29-1.35-.29-.49 0-.93.1-1.3.29-.37.18-.69.44-.95.78-.26.33-.45.73-.58 1.2-.13.46-.2.96-.2 1.5h1.43c.01-.35.04-.67.09-.97s.14-.56.25-.78.26-.39.45-.52.43-.19.71-.19q.465 0 .75.18c.19.12.34.26.45.43s.18.36.22.56q.06.3.06.57c-.01.38-.1.72-.26 1.02-.15.3-.37.57-.63.83-.26.25-.54.49-.85.71s-.61.45-.89.68c-.6.45-1.06.98-1.41 1.58-.35.61-.52 1.32-.53 2.13h6.01v-1.43H7.69c.06-.21.17-.42.33-.61s.34-.38.56-.55"];
})), QW, $W = o((() => {
	QW = ["M5 0H1a1 1 0 0 0-1 1v4h2V2h3zm13 15v3h-3v2h4a1 1 0 0 0 1-1v-4zM0 15h2v3h3v2H1a1 1 0 0 1-1-1zM15 0h4a1 1 0 0 1 1 1v4h-2V2h-3zM9.55 2.125 3.742 5.252 10 9l6.259-3.748L10.5 2.125a.96.96 0 0 0-.95 0M9.5 10 3.106 5.996A.9.9 0 0 0 3 6.421V12.7c0 .34.192.655.504.824l5.889 3.426q.052.028.107.05zm7.394-4.004a.9.9 0 0 1 .106.425V12.7c0 .34-.192.655-.504.824l-5.889 3.426q-.052.028-.107.05v-7z"];
})), eG, tG = o((() => {
	eG = ["M19 6h-5V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h4v-6h4v6h10c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1M6 12H2V8h4zm0-6H2V2h4zm6 6H8V8h4zm0-6H8V2h4zm6 11h-4v-3h4zm0-5h-4V8h4z"];
})), nG, rG = o((() => {
	nG = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0M7 18l2-7H5l8-9-2 7h4z"];
})), iG, aG = o((() => {
	iG = ["M19 17.99h-1.36l-4.35-9.57 2.91-.86 1.66 4.1c.11.27.43.4.72.31.12-.04.22-.11.28-.2.06-.11 1.47-2.08 1.05-5.6C19.79 5.12 19.3 0 16.01 0 14.89.01 13.99.83 14 1.84c0 .19.04.38.1.56l1.34 3.31L.72 10.03v.02c-.41.12-.72.49-.72.94 0 .55.45 1 1 1 .1 0 .19-.03.28-.06v.02l2-.59 1.47 6.63H3c-.55 0-1 .45-1 1s.45 1 1 1h16c.55 0 1-.45 1-1s-.45-1-1-1M5.2 10.8l3.95-1.16-2.83 6.22zm2.35 7.19 3.95-8.68 3.95 8.68z"];
})), oG, sG = o((() => {
	oG = ["M14.94 0h-4c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-8 6c-.28 0-.53.11-.71.29l-3 3c-.18.18-.29.43-.29.71s.11.53.29.71l3 3A1.003 1.003 0 0 0 7.94 13V7c0-.55-.45-1-1-1"];
})), cG, lG = o((() => {
	cG = ["M18 3a1 1 0 1 0-2 0 1 1 0 0 0 2 0m-3.82 1.028a6.2 6.2 0 0 0-1.667.347c-.947.352-1.773 1-2.032 2.318C10.158 8.337 9.247 9.368 8.217 10c1.03.632 1.941 1.663 2.264 3.307.259 1.318 1.085 1.966 2.032 2.318.581.217 1.18.308 1.668.347a3.001 3.001 0 1 1-.019 2.004c-.633-.042-1.491-.158-2.347-.476-1.402-.523-2.868-1.625-3.296-3.807-.259-1.318-1.085-1.966-2.032-2.318a5 5 0 0 0-.722-.21 3 3 0 1 1 0-2.33q.36-.075.722-.21c.947-.352 1.773-1 2.032-2.318.428-2.182 1.894-3.284 3.296-3.807.856-.318 1.714-.434 2.347-.476a3.001 3.001 0 1 1 .018 2.004M4 10a1 1 0 1 0 0 .002zm13 8a1 1 0 1 0 0-2 1 1 0 0 0 0 2"];
})), uG, dG = o((() => {
	uG = ["M2 10a1 1 0 1 0 2 0 1 1 0 0 0-2 0m3.83-1h8.34a3.001 3.001 0 1 1 0 2H5.83a3.001 3.001 0 1 1 0-2M17 9a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), fG, pG = o((() => {
	fG = ["M4 1h14c.55 0 1 .45 1 1v13c0 .55-.45 1-1 1h-8v-2h7V4H5v6H3V2c0-.55.45-1 1-1m2.5 5h7c.28 0 .5-.22.5-.5s-.22-.5-.5-.5h-7c-.28 0-.5.22-.5.5s.22.5.5.5m0 2h3c.28 0 .5-.22.5-.5S9.78 7 9.5 7h-3c-.28 0-.5.22-.5.5s.22.5.5.5m5 2h-5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5h5c.28 0 .5.22.5.5s-.22.5-.5.5M7 17c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1s.45 1 1 1h2.59L.3 18.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L7 14.41z"];
})), mG, hG = o((() => {
	mG = ["M10 0c5.52 0 10 4.48 10 10s-4.48 10-10 10S0 15.52 0 10c0-.55.45-1 1-1s1 .45 1 1c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8C7.47 2 5.22 3.17 3.76 5H5c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1s1 .45 1 1v2.05C3.82 1.6 6.71 0 10 0m1 16H9v-2h2zm0-3H9V4h2z"];
})), gG, _G = o((() => {
	gG = ["M6 10c0 2.162.858 4.124 2.251 5.563a6 6 0 1 1 0-11.127A7.97 7.97 0 0 0 6 10m6 0a6 6 0 0 1-2 4.472A6 6 0 0 1 8 10c0-1.777.773-3.374 2-4.472q.23.205.438.435A5.98 5.98 0 0 1 12 10m-.251 5.563a6 6 0 1 0 0-11.127A7.97 7.97 0 0 1 14 10a7.97 7.97 0 0 1-2.251 5.563m-1.833-8.45A5 5 0 0 0 9 10c0 1.011.301 1.973.844 2.781l.156.22c.593-.79.943-1.739.994-2.748L11 10c0-1.01-.3-1.972-.844-2.781L10.001 7z"];
})), vG, yG = o((() => {
	vG = ["M0 10c0 5.51 4.49 10 10 10 1.17 0 2.32-.2 3.42-.6.52-.19.79-.76.6-1.28a1 1 0 0 0-1.28-.6c-.88.32-1.8.48-2.74.48-4.41 0-8-3.59-8-8s3.59-8 8-8c.94 0 1.86.16 2.74.48a1 1 0 0 0 1.28-.6 1 1 0 0 0-.6-1.28C12.32.2 11.17 0 10 0 4.49 0 0 4.49 0 10m19.71-.71-4-4a1.003 1.003 0 0 0-1.42 1.42L16.59 9H5a1 1 0 0 0 0 2h11.59l-2.29 2.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71"];
})), bG, xG = o((() => {
	bG = ["m11.849.306 7.045 3.523A2 2 0 0 1 20 5.618v8.705a2 2 0 0 1-1.257 1.857l-8.955 3.582a2 2 0 0 1-1.637-.068L1.106 16.17A2 2 0 0 1 0 14.38V5.678A2 2 0 0 1 1.257 3.82L10.212.238a2 2 0 0 1 1.637.068M10 9.677v7.846l8-3.2V6.477l-3 1.2v5.159l-2 .793V8.477z"];
})), SG, CG = o((() => {
	SG = ["M0 11V9h2a1 1 0 0 1 0 2zm20-2v2h-3a1 1 0 1 1 0-2zM5 9a1 1 0 0 0 0 2h3a1 1 0 1 0 0-2zm5 1a1 1 0 0 1 1-1h3a1 1 0 1 1 0 2h-3a1 1 0 0 1-1-1m7-10h-2v4H4V0H2v5c0 .55.45 1 1 1h13c.55 0 1-.45 1-1zM2 20h2v-4h11v4h2v-5c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1z"];
})), wG, TG = o((() => {
	wG = ["M19 1H1c-.55 0-1 .45-1 1v16c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1M7 17H2V8h5zm11 0H8V8h10zm0-10H2V3h16z"];
})), EG, DG = o((() => {
	EG = ["M11 17h6V3h-6zM1 20h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1M2 2h16v16H2z"];
})), OG, kG = o((() => {
	OG = ["M1 1h18a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1m1 2v13h16V3zm9 0h1v13h-1zm2 7h3.952v1H13zm0 2h3.952v1H13zm0 2h3.952v1H13zm0-6h3.952v1H13zm0-2h3.952v1H13zm0-2h3.952v1H13z"];
})), AG, jG = o((() => {
	AG = ["M19 1H1c-.6 0-1 .4-1 1v15c0 .6.4 1 1 1h18c.6 0 1-.4 1-1V2c0-.6-.4-1-1-1m-9 11H7V9h3zm0-4H7V5h3zm-8 8V3h4v13zm5 0v-3h3v3zm11 0h-7v-3h7zm0-4h-7V9h7zm0-4h-7V5h7z"];
})), MG, NG = o((() => {
	MG = ["M18.35 2.67A5.66 5.66 0 0 0 14.33 1c-1.44 0-2.89.56-3.99 1.67l-9.16 9.27C.4 12.73 0 13.78 0 14.83s.39 2.1 1.18 2.9c.78.79 1.82 1.18 2.85 1.18 1.04 0 2.07-.39 2.87-1.2l9.14-9.27c.96-.96.96-2.5.02-3.45s-2.49-.96-3.44 0l-7.59 7.69c-.31.32-.3.83.01 1.14s.81.31 1.13.02l7.59-7.69c.31-.31.84-.31 1.13-.02.31.31.31.85 0 1.16l-9.14 9.27c-.93.95-2.54.93-3.45.02-.94-.95-.92-2.55.02-3.49l9.16-9.25c1.55-1.56 4.18-1.59 5.72-.03 1.56 1.57 1.55 4.26 0 5.82l-8.89 9.02c-.3.31-.3.81.01 1.11.3.3.79.31 1.1.01v.01l8.91-9.02A5.65 5.65 0 0 0 20 6.73c0-1.48-.55-2.94-1.65-4.06"];
})), PG, FG = o((() => {
	PG = ["M16.5 1H7C4.2 1 2 3.2 2 6s2.2 5 5 5v6.5c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5V4h2v13.5c0 .8.7 1.5 1.5 1.5s1.5-.7 1.5-1.5V4h1.5c.8 0 1.5-.7 1.5-1.5S17.3 1 16.5 1"];
})), IG, LG = o((() => {
	IG = ["M12 1c.55 0 1 .45 1 1v2H6V2c0-.55.45-1 1-1h.78a1.98 1.98 0 0 1 3.44 0zm2 1h2c.55 0 1 .45 1 1v16c0 .55-.45 1-1 1H3c-.55 0-1-.45-1-1V3c0-.55.45-1 1-1h2v3h9zm-.069 12.492c-.387.531-.68.856-.857.983a.8.8 0 0 1-.44.118c-.199 0-.398-.118-.596-.364-.325-.412-.765-1.563-1.32-3.442.492-.836.9-1.387 1.246-1.643a1.25 1.25 0 0 1 .774-.285c.105 0 .293.039.555.108.272.069.502.108.712.108a.98.98 0 0 0 .711-.285q.283-.28.283-.738c0-.324-.094-.57-.283-.757s-.46-.285-.816-.285c-.314 0-.617.068-.9.216s-.638.463-1.068.954c-.324.364-.806 1.004-1.434 1.909A9.2 9.2 0 0 0 9.2 8l-3.389.58-.063.354a3.4 3.4 0 0 1 .638-.068 1.01 1.01 0 0 1 .838.423c.345.442.837 1.77 1.454 4.002-.492.63-.816 1.043-1.004 1.24-.293.315-.545.522-.733.61a1.05 1.05 0 0 1-.502.108c-.147 0-.377-.078-.702-.226a1.5 1.5 0 0 0-.596-.148 1.15 1.15 0 0 0-.817.315 1.04 1.04 0 0 0-.324.787.98.98 0 0 0 .293.738c.199.187.461.285.796.285a2.2 2.2 0 0 0 .91-.197c.283-.128.638-.413 1.067-.846.43-.432 1.026-1.111 1.78-2.045.293.885.543 1.534.753 1.937s.461.698.733.876q.41.265 1.036.265.597.001 1.225-.422c.565-.355 1.12-.984 1.685-1.88l-.346-.196"];
})), RG, zG = o((() => {
	RG = ["M18 0H2C.9 0 0 .9 0 2s.9 2 2 2h7v4H4c-1.1 0-2 .9-2 2s.9 2 2 2h5v4H6c-1.1 0-2 .9-2 2s.9 2 2 2h8c1.1 0 2-.9 2-2s-.9-2-2-2h-3v-4h5c1.1 0 2-.9 2-2s-.9-2-2-2h-5V4h7c1.1 0 2-.9 2-2s-.9-2-2-2"];
})), BG, VG = o((() => {
	BG = ["M4 7c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m15 11.69-5-2.5v-3.63c-.32.11-.66.22-1 .29v3.32l-6 2.57v-7.25c-.36-.27-.69-.57-1-.9v8.1l-5-2.5V10c.55 0 1-.45 1-1s-.45-1-1-1V1.31l3.43 1.71c.11-.31.24-.62.39-.92L.72.05A.6.6 0 0 0 .5 0C.22 0 0 .22 0 .5v16c0 .2.12.36.28.44l6 3c.07.04.14.06.22.06.07 0 .14-.01.2-.04l6.79-2.91 5.79 2.9c.07.03.14.05.22.05.28 0 .5-.22.5-.5v-4.21c-.31.13-.64.21-1 .21zM10 5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m3-1c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1m6.72-.94-1.43-.72c.2.43.36.89.48 1.36l.23.11V5.5c-.55 0-1 .45-1 1s.45 1 1 1v1.96l1 1V3.5c0-.2-.12-.36-.28-.44m-3.69 5.56c.14-.21.27-.42.38-.65.02-.04.04-.07.05-.11.11-.22.2-.45.28-.69v-.01c.07-.24.13-.48.17-.73l.03-.17c.04-.25.06-.5.06-.76C17 2.46 14.54 0 11.5 0S6 2.46 6 5.5 8.46 11 11.5 11c.26 0 .51-.02.76-.06l.17-.03c.25-.04.49-.1.73-.17h.01c.24-.08.47-.17.69-.28.04-.02.07-.03.11-.05.23-.11.44-.24.65-.38l.18.18 3.5 3.5c.17.18.42.29.7.29a1.003 1.003 0 0 0 .71-1.71zm-4.53.88c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4"];
})), HG, UG = o((() => {
	HG = ["M7 3H4c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1m9 0h-3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h3c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), WG, GG = o((() => {
	WG = ["M16.94 17a5 5 0 0 0-.33-1.06c-.45-.97-1.37-1.52-3.24-2.3-.17-.07-.76-.31-.77-.32-.1-.04-.2-.08-.28-.12.05-.14.04-.29.06-.45 0-.05.01-.11.01-.16-.25-.21-.47-.48-.65-.79.22-.34.41-.71.56-1.12l.04-.11c-.01.02-.01.02-.02.08l.06-.15c.36-.26.6-.67.72-1.13.18-.37.29-.82.25-1.3-.05-.5-.21-.92-.47-1.22-.02-.53-.06-1.11-.12-1.59.38-.17.83-.26 1.24-.26.59 0 1.26.19 1.73.55.46.35.8.85.97 1.4.04.13.07.25.08.38.08.45.13 1.14.13 1.61v.07c.16.07.31.24.35.62.02.29-.09.55-.15.65-.05.26-.2.53-.46.59-.03.12-.07.25-.11.36-.01.01-.01.04-.01.04-.2.53-.51 1-.89 1.34 0 .06 0 .12.01.17.04.41-.11.71 1 1.19 1.1.5 2.77 1.01 3.13 1.79.34.79.2 1.25.2 1.25h-3.04zm-5.42-3.06c1.47.66 3.7 1.35 4.18 2.39.45 1.05.27 1.67.27 1.67H.04s-.19-.62.27-1.67 2.68-1.75 4.16-2.4 1.33-1.05 1.38-1.59c0-.07.01-.14.01-.21-.52-.45-.95-1.08-1.22-1.8l-.01-.01c0-.01-.01-.02-.01-.03-.07-.15-.12-.32-.16-.49-.34-.06-.54-.43-.62-.78-.08-.14-.24-.48-.2-.87.05-.51.26-.74.49-.83v-.08c0-.64.05-1.55.17-2.15a3.65 3.65 0 0 1 1.4-2.36C6.32 2.25 7.21 2 8 2s1.68.25 2.31.73a3.63 3.63 0 0 1 1.4 2.36c.11.6.17 1.52.17 2.15v.09c.22.09.42.32.47.82.03.39-.12.73-.2.87-.07.34-.27.71-.61.78-.04.16-.09.33-.15.48-.01.01-.02.05-.02.05-.27.71-.68 1.33-1.19 1.78 0 .08 0 .16.01.23.05.55-.15.95 1.33 1.6"];
})), KG, qG = o((() => {
	KG = ["M15 10c-1.66 0-3 1.34-3 3v2c0 1.66 1.34 3 3 3s3-1.34 3-3v-2c0-1.66-1.34-3-3-3m1 5c0 .55-.45 1-1 1s-1-.45-1-1v-2c0-.55.45-1 1-1s1 .45 1 1zM8 7V5c0-1.66-1.34-3-3-3S2 3.34 2 5v2c0 1.66 1.34 3 3 3s3-1.34 3-3M4 7V5c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1s-1-.45-1-1m11-4a1.003 1.003 0 0 0-1.88-.48L5.14 16.49a1.003 1.003 0 1 0 1.74.99l7.99-13.97c.08-.15.13-.32.13-.51"];
})), JG, YG = o((() => {
	JG = ["M19.61 17.91c-.57-1.32-3.35-2.19-5.19-3.01-1.85-.82-1.59-1.31-1.66-1.99-.01-.09-.01-.19-.02-.29.63-.56 1.15-1.33 1.49-2.22 0 0 .02-.05.02-.06.07-.19.13-.39.19-.6.42-.09.67-.55.76-.98.1-.17.29-.6.25-1.08-.06-.62-.31-.91-.59-1.03v-.11c0-.79-.07-1.93-.22-2.68A4.55 4.55 0 0 0 12.9.92C12.11.32 11 0 10.01 0s-2.1.32-2.89.92a4.55 4.55 0 0 0-1.74 2.94c-.14.75-.22 1.89-.22 2.68v.1c-.29.11-.55.4-.61 1.04-.04.48.15.91.25 1.08.1.44.35.91.79.98.05.21.12.41.19.6 0 .01.01.03.01.04l.01.02c.34.91.87 1.69 1.52 2.25 0 .09-.01.18-.02.26-.07.68.13 1.17-1.72 1.99S.96 16.59.39 17.91.05 20 .05 20h19.9s.23-.77-.34-2.09"];
})), XG, ZG = o((() => {
	XG = ["M19.91 15.51c-.08-.08-4.21-2.5-4.35-2.57a.9.9 0 0 0-.4-.1c-.19 0-.42.13-.71.4-.28.27-1.17 1.49-1.43 1.76s-.48.4-.65.4c-.08 0-.19-.02-.32-.07s-1.45-.73-4.2-3.15-3.11-4-3.13-4.44c0-.17.13-.39.4-.65.28-.25.57-.51.89-.74.32-.24.61-.5.88-.78s.4-.52.4-.71c0-.13-.03-.27-.1-.4C7.12 4.32 4.62.19 4.53.1c-.19-.18-.92-.1-1.29.1C.25 1.82 0 4 .05 4.86c.05.89.61 5.58 5.2 9.93 5.7 5.41 9.66 5.2 9.92 5.2.87 0 3.52-.48 4.65-3.19.16-.38.31-1.07.09-1.29"];
})), QG, $G = o((() => {
	QG = ["M19.845 15.51c-.08-.08-4.206-2.5-4.346-2.57a.9.9 0 0 0-.4-.1c-.189 0-.419.13-.709.4-.28.27-1.168 1.49-1.428 1.76s-.48.4-.65.4c-.08 0-.19-.02-.319-.07-.13-.05-1.449-.73-4.196-3.15s-3.107-4-3.127-4.44c0-.17.13-.39.4-.65.28-.25.57-.51.89-.74q.476-.36.878-.78c.27-.28.4-.52.4-.71 0-.13-.03-.27-.1-.4C7.068 4.32 4.57.19 4.48.1c-.19-.18-.92-.1-1.289.1C.205 1.82-.045 4 .005 4.86c.05.89.61 5.58 5.195 9.93 5.694 5.41 9.65 5.2 9.91 5.2.869 0 3.516-.48 4.645-3.19.16-.38.31-1.07.09-1.29M11 2c-.6 0-1-.4-1-1s.4-1 1-1c5 0 9 4 9 9 0 .6-.4 1-1 1s-1-.4-1-1c0-3.9-3.1-7-7-7m0 4c-.6 0-1-.4-1-1s.4-1 1-1c2.8 0 5 2.2 5 5 0 .6-.4 1-1 1s-1-.4-1-1c0-1.7-1.3-3-3-3"];
})), eK, tK = o((() => {
	eK = ["M19.845 15.51c-.08-.08-4.206-2.5-4.346-2.57a.9.9 0 0 0-.4-.1c-.189 0-.419.13-.709.4-.28.27-1.168 1.49-1.428 1.76s-.48.4-.65.4c-.08 0-.19-.02-.319-.07-.13-.05-1.449-.73-4.196-3.15s-3.107-4-3.127-4.44c0-.17.13-.39.4-.65.28-.25.57-.51.89-.74q.476-.36.878-.78c.27-.28.4-.52.4-.71 0-.13-.03-.27-.1-.4C7.068 4.32 4.57.19 4.48.1c-.19-.18-.92-.1-1.289.1C.205 1.82-.045 4 .005 4.86c.05.89.61 5.58 5.195 9.93 5.694 5.41 9.65 5.2 9.91 5.2.869 0 3.516-.48 4.645-3.19.16-.38.31-1.07.09-1.29M11 7h5.58l-1.29 1.29a1 1 0 0 0-.3.71 1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L16.58 5H11c-.55 0-1 .45-1 1s.45 1 1 1"];
})), nK, rK = o((() => {
	nK = ["M14 0H4c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-4.342A6 6 0 0 1 13 15v1H5V3h8c.701 0 1.375.12 2 .341V1c0-.55-.45-1-1-1M9 19c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m4-15c.711 0 1.387.148 2 .416A4.99 4.99 0 0 1 18 9a5 5 0 0 1-.828 2.757l2.534 2.534a1 1 0 1 1-1.415 1.415l-2.534-2.534A5 5 0 0 1 13 14a5 5 0 0 1-5-5c.021-2.724 2.259-5 5-5m0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6"];
})), iK, aK = o((() => {
	iK = ["M9 .98c-4.5.5-8 4.31-8 8.94 0 4.97 4.03 9.04 9 9.04 4.63 0 8.44-3.96 8.94-7.96H9zm1-1.06V10h10C20 4 15.52-.08 10-.08"];
})), oK, sK = o((() => {
	oK = ["M5 5h5a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H5A5 5 0 0 1 5 5m7 .727c0-.401.326-.727.727-.727H15a5 5 0 0 1 0 10h-2.273a.727.727 0 0 1-.727-.727zM15 13a3 3 0 1 0 0-6h-1v6z"];
})), cK, lK = o((() => {
	cK = ["M11.77 1.16c-.81.81-.74 2.28.02 3.76L6.1 8.71c-2.17-1.46-4.12-2-4.94-1.18l4.95 4.95-4.95 6.36 6.36-4.95 4.95 4.95c.82-.82.27-2.77-1.19-4.94l3.8-5.69c1.47.76 2.94.84 3.76.02z"];
})), uK, dK = o((() => {
	uK = ["M3.096 9.522c.344.687-.328 1.881-1.098 3.25-.792 1.408-1.688 3-1.688 4.413 0 .225.238.426.436.553.165.106.362.144.558.144h3.594a.985.985 0 0 0 .985-.985c0-.262.104-.512.288-.697l.162-.162a.84.84 0 0 0 .246-.594.84.84 0 0 1 .247-.595l.102-.102a1.2 1.2 0 0 0 .348-.84v-.205c0-.385.312-.697.697-.697h3.483c.77 0 1.393-.623 1.393-1.393V10.22c0-.77.624-1.393 1.394-1.393h4.179c.77 0 1.394-.624 1.394-1.394V6.315c0-.083.033-.162.092-.219A.3.3 0 0 0 20 5.878v-.493a.44.44 0 0 0-.092-.271.44.44 0 0 1-.092-.271v-.197a.697.697 0 0 0-.697-.697h-.348a.35.35 0 0 1-.349-.348.35.35 0 0 0-.348-.349h-.144a.5.5 0 0 0-.349.145l-.203.204a1.2 1.2 0 0 1-.841.348H3.385a.7.7 0 0 1-.493-.204.697.697 0 0 0-.985 0 .7.7 0 0 1-.493.204h-.408a.697.697 0 0 0-.696.697v2.457c0 .217-.053.429-.132.63-.161.41-.356 1.093.132 1.093.112 0 .248-.008.398-.016.786-.041 1.98-.104 2.388.712m4.571 2.787a.305.305 0 0 1-.296-.38l.3-1.203c.045-.175.302-.143.302.037 0 .084.068.152.153.152h.438q.106 0 .193.059l.553.369c.317.21.694-.167.483-.483l-.368-.553a.35.35 0 0 1-.059-.194V9.87c0-.192.156-.348.348-.348h1.598a.35.35 0 0 1 .246.102l.187.187c.26.261.408.615.408.985v.672a.35.35 0 0 1-.102.246l-.187.187a1.4 1.4 0 0 1-.985.408zM2.264 6.25h16.124c.25 0 .398.278.26.486l-.209.312a.31.31 0 0 1-.26.14H2.055a.312.312 0 0 1-.26-.486l.209-.313a.31.31 0 0 1 .26-.139"];
})), fK, pK = o((() => {
	fK = ["M5.83 9.75.29 15.29a1.003 1.003 0 0 0 1.42 1.42l5.54-5.54c-.57-.37-1.05-.85-1.42-1.42M19 11c-.55 0-1 .45-1 1v1.59l-3.83-3.83c-.37.56-.85 1.04-1.41 1.41L16.59 15H15c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1m-5-4c0-2.21-1.79-4-4-4S6 4.79 6 7s1.79 4 4 4 4-1.79 4-4m-4 2c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2"];
})), mK, hK = o((() => {
	mK = ["M3 5H1c-.55 0-1 .45-1 1v13c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m0-5H1C.45 0 0 .45 0 1v2c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m13.71 5.29C16.53 5.11 16.28 5 16 5s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L15 8.41V11c0 2.21-1.79 4-4 4H8.41l1.29-1.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3c-.18.18-.29.43-.29.71s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L8.41 17H11c3.31 0 6-2.69 6-6V8.41l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zM19 0H6c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), gK, _K = o((() => {
	gK = ["M16 10c0-.36-.2-.67-.49-.84l.01-.01-10-6-.01.01A1 1 0 0 0 5 3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1 .19 0 .36-.07.51-.16l.01.01 10-6-.01-.01c.29-.17.49-.48.49-.84"];
})), vK, yK = o((() => {
	vK = ["M1.707.293A1 1 0 0 0 .293 1.707L2.086 3.5.293 5.293a1 1 0 0 0 1.414 1.414L3.5 4.914l1.793 1.793a1 1 0 0 0 1.414-1.414L4.914 3.5l1.793-1.793A1 1 0 0 0 5.293.293L3.5 2.086zM16 20a4 4 0 1 0 0-8 4 4 0 0 0 0 8m0-2a2 2 0 1 0 0-4 2 2 0 0 0 0 4m2.29-12.3L16 3.41V8a3 3 0 0 1-3 3H4a1 1 0 0 0-1 1v7a1 1 0 1 1-2 0v-7a3 3 0 0 1 3-3h9a1 1 0 0 0 1-1V3.41l-2.29 2.3a1.003 1.003 0 0 1-1.42-1.42l4-4c.18-.18.43-.29.71-.29s.53.11.71.29l4 4A1.003 1.003 0 0 1 19 6c-.28 0-.53-.11-.71-.3"];
})), bK, xK = o((() => {
	bK = ["M16 9h-5V4c0-.55-.45-1-1-1s-1 .45-1 1v5H4c-.55 0-1 .45-1 1s.45 1 1 1h5v5c0 .55.45 1 1 1s1-.45 1-1v-5h5c.55 0 1-.45 1-1s-.45-1-1-1"];
})), SK, CK = o((() => {
	SK = ["M18 7q-.405 0-.75.15l-6.28-4.88c.01-.09.03-.18.03-.27 0-1.1-.9-2-2-2S7 .9 7 2c0 .06.01.12.02.19l-4.19 3C2.57 5.07 2.29 5 2 5 .9 5 0 5.9 0 7c0 .74.4 1.38 1 1.72v7.55c-.6.35-1 .99-1 1.73 0 1.1.9 2 2 2 .74 0 1.38-.4 1.72-1h7.55c.35.6.98 1 1.72 1 1.1 0 2-.9 2-2 0-.37-.11-.72-.29-1.02L18.03 11A2 2 0 0 0 18 7m-5.03 9c-.72.01-1.35.41-1.69 1H3.72c-.17-.3-.42-.55-.72-.72V8.72c.6-.34 1-.98 1-1.72 0-.06-.01-.12-.02-.19l4.19-3c.26.12.54.19.83.19q.405 0 .75-.15l6.28 4.88c-.01.09-.03.18-.03.27 0 .37.11.72.29 1.02z"];
})), wK, TK = o((() => {
	wK = ["M6 10c0-2.21 1.79-4 4-4h6.59L14.3 8.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-4-4a1.003 1.003 0 0 0-1.42 1.42L16.59 4H10c-3.31 0-6 2.69-6 6H1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1zm-4 8v-6h6v6z"];
})), EK, DK = o((() => {
	EK = ["M10 10c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1S9 .45 9 1v8c0 .55.45 1 1 1m3-7.45v2.16c2.36 1.12 4 3.5 4 6.29 0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.79 1.64-5.17 4-6.29V2.55C3.51 3.79 1 7.09 1 11a9 9 0 0 0 18 0c0-3.91-2.51-7.21-6-8.45"];
})), OK, kK = o((() => {
	OK = ["M20 8.01c0-1.26-.61-2.43-1.61-3.12C17.86 2.5 15.8.79 13.4.79c-.58 0-1.14.1-1.69.29A3.53 3.53 0 0 0 9.17 0C8.05 0 7 .55 6.32 1.45q-.225-.03-.45-.03c-1.63 0-3.03 1.12-3.46 2.71C.97 4.65 0 6.05 0 7.66c0 .48.09.95.26 1.4-.17.44-.26.91-.26 1.39 0 1.38.72 2.64 1.89 3.29.67.7 1.59 1.09 2.54 1.09.61 0 1.19-.15 1.71-.45.68.82 1.68 1.3 2.73 1.3.66 0 1.28-.18 1.83-.52.61.49 1.34.81 2.11.91 1.3 1.43 2.3 3.28 2.31 3.3 0 0 .35.61.33.61.96-.01 1.77-.2 1.64-1.3.01.02-.92-2.89-.92-2.89.52-.26.94-.69 1.21-1.23 1.12-.66 1.84-1.91 1.84-3.26 0-.3-.03-.6-.1-.89.57-.64.88-1.51.88-2.4m-1.54 1.28-.18-.2-.77-.84c-.33-.37-.67-1.17-.73-1.73 0 0-.13-1.25-.13-1.26-.06-.74-1.17-.73-1.13.14 0 .02.13 1.26.13 1.26.04.36.15.77.3 1.17-.08-.01-.15-.02-.22-.02 0 0-2.57-.12-2.57-.13-.73-.03-.89 1.22-.05 1.25l2.57.13c.53.03 1.29.37 1.61.72l.61.67.02.06c.1.27.14.55.14.83 0 .93-.51 1.77-1.34 2.18l-.2.1-.09.23c-.19.48-.6.82-1.1.93l-.67.14.87 2.75c-.48-.76-1.19-1.79-2.02-2.67l-.15-.16-.21-.02c-.51-.04-.99-.21-1.42-.48l1.7-1.48c.44-.39 1.04-.55 1.24-.49 0 0 .78.22.78.23.78.2 1.03-.92.29-1.21l-.78-.23c-.69-.2-1.67.22-2.24.72l-1.91 1.66-.39.32c-.44.36-.93.55-1.5.55-.8 0-1.54-.41-1.97-1.07v-1.88c0-.5.21-.98.34-1.07 0 0 .65-.43.64-.43.87-.69.21-1.57-.64-1.14 0-.01-.65.43-.65.43-.31.2-.54.56-.7.97-.13-.13-.28-.25-.43-.35 0 0-1.91-1.26-1.91-1.28-.81-.56-1.5.63-.61 1.11 0-.02 1.89 1.28 1.89 1.28.46.31.77.97.77 1.36v.84c-.43.24-.78.36-1.24.36-.67 0-1.31-.29-1.77-.79l-.07-.08-.09-.05a2.42 2.42 0 0 1-1.31-2.16c0-.38.09-.74.25-1.08l.15-.31-.14-.33c-.17-.34-.25-.7-.25-1.08 0-1.13.76-2.1 1.85-2.37l.39-.09.07-.43a2.41 2.41 0 0 1 2.39-2.05c.19 0 .39.02.58.07l.4.1.22-.38A2.41 2.41 0 0 1 9.17 1.3c.55 0 1.08.19 1.5.53l-.44.45-.01-.01-.31.31c-.41.35-.92.53-1.11.5 0 0-.84-.13-.84-.14-.83-.15-1.09 1.08-.18 1.29.01 0 .84.14.84.14.03 0 .06 0 .09.01-.14.46-.18.96-.12 1.4 0 0 .21 1.24.19 1.23.13.65 1.32.44 1.16-.22 0-.01-.19-1.23-.19-1.23-.07-.48.15-1.19.45-1.5l.48-.5c.07-.06.13-.12.19-.18l.93-.95c.5-.23 1.04-.34 1.59-.34 1.93 0 3.57 1.4 3.89 3.34l.05.31.26.15a2.445 2.445 0 0 1 .87 3.4"];
})), AK, jK = o((() => {
	AK = ["M13.95 10.23c.16-.18.22-.22.46-.22h1.48c.25 0 .47.08.59.33.1.2.09.41-.05.66l-2.71 3.58L16.88 19c.13.21.16.46.03.69-.12.21-.34.31-.57.31H14.7c-.31 0-.56-.17-.7-.44l-1.9-2.67-1.93 2.68c-.15.27-.42.43-.73.43H7.98c-.25 0-.47-.08-.59-.33-.1-.2-.09-.41.05-.66l3.09-4.35L6.26 9H5v4.32c0 .41-.3.69-.7.69H2.7c-.41 0-.7-.28-.7-.69V.69c0-.41.3-.69.7-.69h4.42c.71 0 1.36.1 1.94.3.59.2 1.11.49 1.54.87.44.38.78.84 1.02 1.39.24.54.36 1.14.36 1.78 0 1.01-.28 1.88-.84 2.6-.43.54-1.35 1.29-2 1.59l3.09 3.94zM6.71 6.04c.71 0 1.45-.16 1.81-.46.33-.28.5-.69.5-1.25s-.17-.97-.5-1.25c-.35-.3-1.1-.46-1.81-.46h-1.7v3.42z"];
})), MK, NK = o((() => {
	MK = ["M19 1h-8c0-.55-.45-1-1-1S9 .45 9 1H1c-.55 0-1 .45-1 1s.45 1 1 1h1v11c0 .55.45 1 1 1h4.59L4.3 18.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L9 16.41V19c0 .55.45 1 1 1s1-.45 1-1v-2.59l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L12.41 15H17c.55 0 1-.45 1-1V3h1c.55 0 1-.45 1-1s-.45-1-1-1m-3 12H4V3h12z"];
})), PK, FK = o((() => {
	PK = ["M14 16H6v-4H4v5c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-5h-2zm2-13c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v1h12zm3 2H1c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h2v-3h14v3h2c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-1 4h-2V7h2z"];
})), IK, LK = o((() => {
	IK = ["M18 4c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v2h16zm-2-3c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v1h12zm3 6H1c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-5 7c0 .55-.45 1-1 1H7c-.55 0-1-.45-1-1v-2h1v2h6v-2h1z"];
})), RK, zK = o((() => {
	RK = ["M2 15c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0-7c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m5-4h12c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1M2 1C.9 1 0 1.9 0 3s.9 2 2 2 2-.9 2-2-.9-2-2-2m17 8H7c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1m0 7H7c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1"];
})), BK, VK = o((() => {
	BK = ["M3 5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m5-1h11c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1M3 15c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m16 1H8c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m-1-8H9c-1.1 0-2 .9-2 2s.9 2 2 2h9c1.1 0 2-.9 2-2s-.9-2-2-2M3 7c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3"];
})), HK, UK = o((() => {
	HK = ["M7.01 10.11c.35-.64.72-1.68 1.09-3.11l.8-3.03h.96l.24-.77h-.99c.28-1.11.66-1.92 1.12-2.43.28-.32.56-.48.83-.48.05 0 .1.02.13.05s.05.07.05.12c0 .04-.04.13-.11.25-.08.12-.11.24-.11.35q0 .225.18.39c.12.11.27.16.45.16.2 0 .36-.07.49-.2s.2-.31.2-.54q0-.39-.3-.63T11.08 0c-.68 0-1.3.19-1.86.58-.55.38-1.08 1.02-1.58 1.91-.17.3-.34.5-.49.59-.15.08-.4.13-.74.12l-.23.77h.95L5.74 9.21c-.23.86-.39 1.39-.47 1.59q-.18.435-.54.75c-.1.08-.21.12-.35.12-.04 0-.07-.01-.1-.03l-.03-.04c0-.02.03-.07.1-.13.07-.07.1-.17.1-.31 0-.15-.05-.28-.16-.38s-.27-.15-.47-.15c-.25 0-.44.07-.59.2-.15.12-.23.28-.23.46 0 .19.09.36.27.5.19.14.47.21.86.21.61 0 1.16-.15 1.63-.46.48-.31.89-.79 1.25-1.43m3.7 1.18c-.18-.18-.43-.29-.71-.29s-.53.11-.71.29l-3 3a1.003 1.003 0 0 0 1.42 1.42L9 14.41V19c0 .55.45 1 1 1s1-.45 1-1v-4.59l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71zm4.15-6.78c.17-.13.36-.2.55-.2.07 0 .2.03.39.08s.36.08.5.08c.2 0 .37-.07.5-.2.13-.14.2-.31.2-.52 0-.22-.07-.4-.2-.53s-.33-.2-.58-.2q-.33 0-.63.15c-.2.1-.45.32-.75.67-.23.25-.56.7-1.01 1.33a6.5 6.5 0 0 0-.91-2.15l-2.38.39-.05.25c.18-.03.33-.05.45-.05.24 0 .43.1.59.3q.375.465 1.02 2.79c-.34.44-.58.73-.7.87-.21.22-.38.36-.52.43-.1.05-.22.08-.35.08-.1 0-.26-.05-.49-.16a1 1 0 0 0-.42-.11c-.23 0-.42.07-.57.22-.17.14-.24.32-.24.55q0 .315.21.51c.14.13.33.2.56.2s.44-.05.64-.14.45-.29.75-.59.72-.78 1.25-1.43c.2.62.38 1.07.53 1.35s.32.49.52.61c.19.12.44.19.73.19.28 0 .57-.1.86-.3.38-.25.77-.69 1.17-1.31l-.25-.14c-.27.37-.48.6-.61.69-.09.06-.19.09-.31.09-.14 0-.28-.09-.42-.26q-.345-.435-.93-2.4c.37-.58.66-.96.9-1.14"];
})), WK, GK = o((() => {
	WK = ["M19 10h-2.38L14.9 6.55h-.01c-.17-.32-.5-.55-.89-.55-.43 0-.79.28-.93.66h-.01l-2.75 7.57L7.98 1.82h-.02A.98.98 0 0 0 7 1c-.44 0-.8.29-.94.69h-.01L3.28 10H1c-.55 0-1 .45-1 1s.45 1 1 1h3c.44 0 .8-.29.94-.69h.01l1.78-5.34 2.29 12.21h.02c.08.46.47.82.96.82.43 0 .79-.28.93-.66h.01l3.21-8.82.96 1.92h.01c.16.33.49.56.88.56h3c.55 0 1-.45 1-1s-.45-1-1-1"];
})), KK, qK = o((() => {
	KK = ["M4 10a3 3 0 1 1 1.065-5.806A5.001 5.001 0 0 1 14.63 3.11q.418-.108.87-.109a3.5 3.5 0 1 1 0 7zm0 2a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0v-5a1 1 0 0 1 1-1m9 1a1 1 0 1 0-2 0v6a1 1 0 1 0 2 0zm3-1a1 1 0 0 1 1 1v3a1 1 0 1 1-2 0v-3a1 1 0 0 1 1-1m-7 1a1 1 0 1 0-2 0v3a1 1 0 1 0 2 0z"];
})), JK, YK = o((() => {
	JK = ["M14.47 5h2.12L15.3 6.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L16.59 3H14c-.31 0-.57.15-.76.37l-.01-.01-2.93 3.52 1.3 1.56zm2.24 7.29a1.003 1.003 0 0 0-1.42 1.42l1.3 1.29h-2.12L4.77 3.36l-.01.01A1 1 0 0 0 4 3H1c-.55 0-1 .45-1 1s.45 1 1 1h2.53l9.7 11.64.01-.01c.19.22.45.37.76.37h2.59l-1.29 1.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71zM3.53 15H1c-.55 0-1 .45-1 1s.45 1 1 1h3c.31 0 .57-.15.76-.37l.01.01 2.93-3.52-1.3-1.56z"];
})), XK, ZK = o((() => {
	XK = ["M10 0q-.663 0-1.305.084a1 1 0 0 0 .259 1.984 8 8 0 0 1 2.092 0 1 1 0 0 0 .259-1.984A10 10 0 0 0 10 0M5.13 3.652a1 1 0 1 0-1.218-1.586 10 10 0 0 0-1.846 1.846A1 1 0 1 0 3.652 5.13 8 8 0 0 1 5.13 3.652m10.958-1.586a1 1 0 0 0-1.218 1.586 8 8 0 0 1 1.478 1.478 1 1 0 1 0 1.585-1.218 10 10 0 0 0-1.845-1.846M2.068 8.954a1 1 0 1 0-1.984-.259 10 10 0 0 0 0 2.61 1 1 0 1 0 1.984-.259 8 8 0 0 1 0-2.092m17.848-.259a1 1 0 1 0-1.984.259 8 8 0 0 1 0 2.092 1 1 0 0 0 1.984.259 10 10 0 0 0 0-2.61M3.652 14.87a1 1 0 0 0-1.586 1.218 10 10 0 0 0 1.846 1.845 1 1 0 0 0 1.218-1.585 8 8 0 0 1-1.478-1.478m14.281 1.218a1 1 0 0 0-1.585-1.218 8 8 0 0 1-1.478 1.478 1 1 0 1 0 1.218 1.585 10 10 0 0 0 1.845-1.845m-8.98 1.844a1 1 0 0 0-.258 1.984 10 10 0 0 0 2.61 0 1 1 0 1 0-.259-1.984 8 8 0 0 1-2.092 0M10 7a3 3 0 1 1 0 6 3 3 0 0 1 0-6m5 3a5 5 0 1 0-10 0 5 5 0 0 0 10 0"];
})), QK, $K = o((() => {
	QK = ["M10 3a7 7 0 1 1 0 14 7 7 0 0 1 0-14"];
})), eq, tq = o((() => {
	eq = ["M4 18h12V2H4zM2 1a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1zm4.293 11.705a.999.999 0 1 1 1.412-1.412L10 13.587l2.295-2.294a.999.999 0 0 1 1.412 1.412l-2.962 2.963a1 1 0 0 1-1.49 0zm0-3.998a1 1 0 0 1 0-1.412l2.962-2.963a1 1 0 0 1 1.49 0l2.962 2.963a.999.999 0 0 1-1.412 1.412L10 6.413 7.705 8.707a1 1 0 0 1-1.412 0"];
})), nq, rq = o((() => {
	nq = ["M18 16V4H2v12zM1 18a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1zM7.295 6.293a.999.999 0 1 1 1.412 1.412L6.413 10l2.294 2.295a.999.999 0 1 1-1.412 1.412l-2.963-2.962a1 1 0 0 1 0-1.49zm3.998 0a1 1 0 0 1 1.412 0l2.963 2.962.04.038a1 1 0 0 1-.04 1.452l-2.963 2.962a.999.999 0 0 1-1.412-1.412L13.587 10l-2.294-2.295a1 1 0 0 1 0-1.412"];
})), iq, aq = o((() => {
	iq = ["M1 4h18c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V5c0-.55.45-1 1-1m1 2v8h16V6z"];
})), oq, sq = o((() => {
	oq = ["m19.71 5.29-4-4a1.003 1.003 0 0 0-1.42 1.42L16.59 5H6c-3.31 0-6 2.69-6 6s2.69 6 6 6h5v-2H6c-2.21 0-4-1.79-4-4s1.79-4 4-4h10.59L14.3 9.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M15 14c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), cq, lq = o((() => {
	cq = ["M3.636 3.636A9 9 0 0 1 10 1c2.439 0 5.182.717 7 2.471V2a1 1 0 1 1 2 0v4a1 1 0 0 1-1 1h-4a1 1 0 1 1 0-2h1.7c-1.304-1.32-3.483-2-5.7-2a7 7 0 0 0-7 7 1 1 0 1 1-2 0 9 9 0 0 1 2.636-6.364m12.728 12.728A9 9 0 0 1 10 19c-2.439 0-5.182-.717-7-2.471V18a1 1 0 1 1-2 0v-4a1 1 0 0 1 1-1h4a1 1 0 1 1 0 2H4.3c1.304 1.32 3.483 2 5.7 2a7 7 0 0 0 7-7 1 1 0 1 1 2 0 9 9 0 0 1-2.636 6.364"];
})), uq, dq = o((() => {
	uq = ["M6 13a1 1 0 1 1 0 2H4.3c1.303 1.32 3.483 2 5.7 2a7 7 0 0 0 3.331-.845l1.46 1.46A9 9 0 0 1 10 19c-2.439 0-5.182-.717-7-2.472V18a1 1 0 1 1-2 0v-4a1 1 0 0 1 1-1zm12-4a1 1 0 0 1 1 1 9 9 0 0 1-1.38 4.785l-1.462-1.46A7 7 0 0 0 17 10a1 1 0 0 1 1-1M3.844 6.668A7 7 0 0 0 3 10a1 1 0 1 1-2 0c0-1.71.488-3.368 1.384-4.792zM18 1a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-4a1 1 0 1 1 0-2h1.7c-1.303-1.32-3.483-2-5.7-2a7 7 0 0 0-3.33.843L5.21 2.382A9 9 0 0 1 10 1c2.439 0 5.182.717 7 2.472V2a1 1 0 0 1 1-1M2 1c.28 0 .53.11.71.3l16 15.99A1.003 1.003 0 0 1 18 19c-.28 0-.53-.11-.71-.3l-16-15.99A1.003 1.003 0 0 1 2 1"];
})), fq, pq = o((() => {
	fq = ["M0 17.5a2.5 2.5 0 1 1 5 0 2.5 2.5 0 0 1-5 0M14 0a1 1 0 0 0-1 1v3.768L9.737 2.884a1 1 0 1 0-1 1.732L12 6.5 8.737 8.384a1 1 0 0 0 1 1.732L13 8.232V12a1 1 0 1 0 2 0V8.232l3.263 1.884a1 1 0 0 0 1-1.732L16 6.5l3.263-1.884a1 1 0 1 0-1-1.732L15 4.768V1a1 1 0 0 0-1-1"];
})), mq, hq = o((() => {
	mq = ["M19 16H3.1L19.31 3.39l-.61-.79L2 15.59V3c0-.55-.45-1-1-1s-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m-9-9c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m-5 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m10-2c0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2-2 .9-2 2m-5 4c0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2-2 .9-2 2"];
})), gq, _q = o((() => {
	gq = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8m5-9H5c-.55 0-1 .45-1 1s.45 1 1 1h10c.55 0 1-.45 1-1s-.45-1-1-1"];
})), vq, yq = o((() => {
	vq = ["M19 0H5c-.55 0-1 .45-1 1v4h2V2h5v16H6v-3H4v4c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18h-5V2h5zM6.29 13.71a1.003 1.003 0 0 0 1.42-1.42L5.41 10 7.7 7.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L4 8.59l-2.29-2.3A1.003 1.003 0 0 0 .29 7.71L2.59 10 .3 12.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L4 11.41z"];
})), bq, xq = o((() => {
	bq = ["M4 11h6c.55 0 1-.45 1-1s-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-7 18H2V2h10zm6 0h-5V2h5z"];
})), Sq, Cq = o((() => {
	Sq = ["M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1M7 18H2V2h5zm11 0H8V2h10zm-8-7h6c.55 0 1-.45 1-1s-.45-1-1-1h-6c-.55 0-1 .45-1 1s.45 1 1 1"];
})), wq, Tq = o((() => {
	wq = ["M7 14h6c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2V8h16zm0-11H2V2h16z"];
})), Eq, Dq = o((() => {
	Eq = ["M7 8h6c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1m12-8H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2v-5h16zm0-6H2V2h16z"];
})), Oq, kq = o((() => {
	Oq = ["M14 6c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1v2.05C16.18 1.6 13.29 0 10 0 4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10c0-.55-.45-1-1-1s-1 .45-1 1c0 4.42-3.58 8-8 8s-8-3.58-8-8 3.58-8 8-8c2.53 0 4.77 1.17 6.24 3H15c-.55 0-1 .45-1 1"];
})), Aq, jq = o((() => {
	Aq = ["M6 6c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1s1 .45 1 1v2.05C3.82 1.6 6.71 0 10 0c5.52 0 10 4.48 10 10s-4.48 10-10 10S0 15.52 0 10c0-.55.45-1 1-1s1 .45 1 1c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8C7.47 2 5.23 3.17 3.76 5H5c.55 0 1 .45 1 1"];
})), Mq, Nq = o((() => {
	Mq = ["M8.7 4.7C7.9 4.2 7 4 6 4c-3.3 0-6 2.7-6 6s2.7 6 6 6c1 0 1.9-.2 2.7-.7C7.3 14 6.5 12.1 6.5 10s.9-4 2.2-5.3M14 4c-1 0-1.9.2-2.7.7 1.4 1.4 2.2 3.2 2.2 5.3s-.9 4-2.2 5.3c.8.5 1.7.7 2.7.7 3.3 0 6-2.7 6-6s-2.7-6-6-6m-4 1.5C8.8 6.7 8 8.2 8 10s.8 3.3 2 4.4c1.2-1.1 2-2.7 2-4.5s-.8-3.3-2-4.4"];
})), Pq, Fq = o((() => {
	Pq = ["M7 4.2C7 5.75 8.34 7 10 7s3-1.46 3-2.8C13 1.45 10.94 0 10 0H6c0 2.74 3.76 1.96 1 4.2m11.71 14.09L13 12.59V9.01c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v3.58l-5.71 5.7a1.003 1.003 0 0 0 1.42 1.42L7 15.42V19c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-3.58l4.29 4.29a1.003 1.003 0 0 0 1.42-1.42M10.21 8c.01 0 .01.01 0 0 .01.01.01 0 0 0"];
})), Iq, Lq = o((() => {
	Iq = ["M8.7 4.7C7.4 6 6.5 7.9 6.5 10s.8 4 2.2 5.3c-.8.5-1.7.7-2.7.7-3.3 0-6-2.7-6-6s2.7-6 6-6c1 0 1.9.2 2.7.7m-3.34 9.25c-.55-1.2-.86-2.54-.86-3.95s.31-2.75.86-3.95a4.001 4.001 0 0 0 0 7.9M14 4c3.3 0 6 2.7 6 6s-2.7 6-6 6c-1 0-1.9-.2-2.7-.7 1.3-1.3 2.2-3.2 2.2-5.3s-.8-3.9-2.2-5.3C12.1 4.2 13 4 14 4m-4 1.5C8.8 6.7 8 8.2 8 10s.8 3.3 2 4.4c1.2-1.1 2-2.7 2-4.5s-.8-3.3-2-4.4"];
})), Rq, zq = o((() => {
	Rq = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5"];
})), Bq, Vq = o((() => {
	Bq = ["M7 7.5c0-3 1.857-6.25 3-7.5 1.143 1.25 3 4.5 3 7.5s-.714 6.25-1 7.5H8c-.286-1.25-1-4.5-1-7.5m6.84 2.5c-.139 1.62-.47 3.405-.84 5.01l4 .99-1-4zm-4.832 6q-.01.21-.008.429C9 17.143 9 17.5 10 20c1-2.5 1-2.857 1-3.571q.002-.219-.008-.429zM7 15.011c-.37-1.605-.701-3.39-.84-5.011L4 12l-1 4zM10 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2"];
})), Hq, Uq = o((() => {
	Hq = ["M10 5c2.121-2.121 6.308-2.924 8-3-.076 1.692-.879 5.879-3 8-1.192 1.192-2.543 1.823-3.748 2.384-.442.207-.865.404-1.252.616-.203.111-.597.302-.986.49-.444.215-.88.426-1.014.51l-2-2c.158-.252 1-2 1-2s1.37-3.37 3-5m5 1a1 1 0 1 0-2 0 1 1 0 0 0 2 0M3 17s0-2 2-4l2 2c-2 2-4 2-4 2m11-2-4 4-1.298-4.233a50 50 0 0 1 2.643-1.322c1.275-.604 2.307-1.092 3.554-2.015zM1 10l4-4 3.557-.899c-.923 1.247-1.412 2.28-2.015 3.554-.36.762-.762 1.61-1.322 2.643z"];
})), Wq, Gq = o((() => {
	Wq = ["M3 1v7H1a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-4h4a1 1 0 0 0 1-1V3c0-.55-.45-1-1-1h-7.58L9.71.3A.97.97 0 0 0 9 0H4c-.55 0-1 .45-1 1m7.596 3H18v9h-3V9a1 1 0 0 0-1-1H5V2h3.584zM9 10h2l-5 8H4z"];
})), Kq, qq = o((() => {
	Kq = ["M18.293 9.59a.76.76 0 0 1-.038 1.035l-4.326 4.326a.76.76 0 1 0 1.076 1.076l4.326-4.326c.846-.846.896-2.2.114-3.106l-3.315-3.84h1.38a.76.76 0 1 0 0-1.521h-3.043a.76.76 0 0 0-.76.76v3.044a.76.76 0 0 0 1.521 0V6.04zm-5.427-.474a1.25 1.25 0 0 1 0 1.768l-5.303 5.303a1.25 1.25 0 0 1-1.768 0L.492 10.884a1.25 1.25 0 0 1 0-1.768l5.303-5.303a1.25 1.25 0 0 1 1.768 0z"];
})), Jq, Yq = o((() => {
	Jq = ["M1.707 9.59a.76.76 0 0 0 .038 1.035l4.326 4.326a.76.76 0 0 1-1.076 1.076L.669 11.701a2.283 2.283 0 0 1-.114-3.106l3.315-3.84H2.49a.76.76 0 1 1 0-1.521h3.043c.42 0 .76.34.76.76v3.044a.76.76 0 1 1-1.521 0V6.04zm17.409-.474a1.25 1.25 0 0 1 0 1.768l-5.303 5.303a1.25 1.25 0 0 1-1.768 0l-5.303-5.303a1.25 1.25 0 0 1 0-1.768l5.303-5.303a1.25 1.25 0 0 1 1.768 0z"];
})), Xq, Zq = o((() => {
	Xq = ["M8.71 6.29A1 1 0 0 0 8 6H3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-8c0-.28-.11-.53-.29-.71zM11 18H4V8h3v3c0 .55.45 1 1 1h3zm3-16h-1.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C9.11 2.47 9 2.72 9 3s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H14c1.1 0 2 .9 2 2v3c0 .55.45 1 1 1s1-.45 1-1V6c0-2.21-1.79-4-4-4"];
})), Qq, $q = o((() => {
	Qq = ["M14 2h-1.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2C9.11 2.47 9 2.72 9 3s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42l-.3-.29H14c1.1 0 2 .9 2 2v3c0 .55.45 1 1 1s1-.45 1-1V6c0-2.21-1.79-4-4-4m-2 5H3c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m-1 11H4V9h7z"];
})), eJ, tJ = o((() => {
	eJ = ["M14.028 6.016c.146.275.31.57.485.872.304.524.628 1.047.952 1.545l.118.178-.208-.006-.577-.005c-2.093.004-2.841.303-2.841.895 0 .069.271.248 1.245.567l1.008.313c2.671.831 3.99 1.827 3.99 4.167 0 2.76-1.928 4.059-4.832 4.376-.782.085-1.52.098-2.452.066l-1.15-.046H6.221l.535-.811a68 68 0 0 0 1.122-1.787h2.04l.686.03c1.028.046 1.77.043 2.523-.039 1.832-.2 2.673-.767 2.673-1.789 0-.69-.483-1.09-1.992-1.585l-.83-.257c-1.192-.364-2.037-.7-2.59-1.165.399-1 .612-1.844.612-2.538a6 6 0 0 0-.382-2.098c.745-.573 1.884-.822 3.41-.883M5 4.2c2.648 0 4.791 2.151 4.8 4.797C9.8 11.652 5 18.6 5 18.6l-.5-.744C3.273 15.993.2 11.121.2 8.997A4.8 4.8 0 0 1 5 4.2m0 2.4a2.4 2.4 0 1 0 .002 4.802A2.4 2.4 0 0 0 5 6.6M17 .333a2.67 2.67 0 0 1 2.667 2.665C19.667 4.473 17 8.333 17 8.333l-.391-.587c-.741-1.137-2.276-3.629-2.276-4.748A2.67 2.67 0 0 1 17 .333"];
})), nJ, rJ = o((() => {
	nJ = ["M10 2a8 8 0 1 0 6.245 13H15a1 1 0 1 1 0-2h4a1 1 0 0 1 1 1v4a1 1 0 1 1-2 0v-1.999A9.99 9.99 0 0 1 10 20C4.477 20 0 15.523 0 10S4.477 0 10 0zm10.001 8-2 .003a8 8 0 0 0-.273-2.077l1.932-.515a10 10 0 0 1 .341 2.59M18.663 5l-1.732 1a8 8 0 0 0-1.273-1.655l1.414-1.415A10 10 0 0 1 18.662 5M15 1.339l-1 1.732a8 8 0 0 0-1.929-.801L12.59.338A10 10 0 0 1 15 1.34M7.507 6.13a1 1 0 0 1 1.008.014l5 3a1 1 0 0 1 0 1.714l-5 3A1 1 0 0 1 7 13V7a1 1 0 0 1 .507-.87"];
})), iJ, aJ = o((() => {
	iJ = ["M9 18c.6 0 1 .4 1 1s-.4 1-1 1c-5 0-9-4-9-9 0-.6.4-1 1-1s1 .4 1 1c0 3.9 3.1 7 7 7m0-4c.6 0 1 .4 1 1s-.4 1-1 1c-2.8 0-5-2.2-5-5 0-.6.4-1 1-1s1 .4 1 1c0 1.7 1.3 3 3 3m5.7-3.7c.4-.4 1-.4 1.4 0l3.6 3.6c.4.4.4 1 0 1.4l-1.4 1.4c-.4.4-1 .4-1.4 0l-3.6-3.6c-.4-.4-.4-1 0-1.4zM4.7.3c.4-.4 1-.4 1.4 0l3.6 3.6c.4.4.4 1 0 1.4L8.3 6.7c-.4.4-1 .4-1.4 0L3.3 3.1c-.4-.4-.4-1 0-1.4zm11.1 1c.4-.4 1-.4 1.4 0l1.6 1.6c.4.4.4 1 0 1.4l-6.5 6.5c-.4.4-1 .4-1.4 0L9.3 9.2c-.4-.4-.4-1 0-1.4zM9 12c-.6 0-1-.4-1-1s.4-1 1-1 1 .4 1 1-.4 1-1 1"];
})), oJ, sJ = o((() => {
	oJ = ["M12 0H4c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h13c.55 0 1-.45 1-1V6zm4 18H5V2h6v5h5zm-8.29-6.71a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29.32 0 .59-.16.77-.38l.01.01 4-5-.01-.01c.14-.18.23-.38.23-.62 0-.55-.45-1-1-1-.32 0-.59.16-.77.38l-.01-.01-3.3 4.13z"];
})), cJ, lJ = o((() => {
	cJ = ["M9 9c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m5 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m4-5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2m1 10H2V3c0-.55-.45-1-1-1s-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M5 15c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2"];
})), uJ, dJ = o((() => {
	uJ = ["m19.56 17.44-4.94-4.94A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8S0 3.58 0 8s3.58 8 8 8c1.67 0 3.21-.51 4.5-1.38l4.94 4.94a1.498 1.498 0 1 0 2.12-2.12M8 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), fJ, pJ = o((() => {
	fJ = ["M17 0c1.7 0 3 1.3 3 3s-1.3 3-3 3a3.03 3.03 0 0 1-1.752-.542l-2.824 2.824a2.985 2.985 0 0 1-.08 3.354l2.905 2.905A3.03 3.03 0 0 1 17 14c1.7 0 3 1.3 3 3s-1.3 3-3 3-3-1.3-3-3c0-.663.199-1.264.541-1.752l-2.905-2.905a2.98 2.98 0 0 1-3.354.08l-2.824 2.825A3.03 3.03 0 0 1 6 17c0 1.7-1.3 3-3 3s-3-1.3-3-3 1.3-3 3-3c.663 0 1.263.2 1.751.541l2.79-2.79c-.4-.51-.64-1.152-.64-1.85 0-.648.206-1.248.555-1.738L4.751 5.458A3.03 3.03 0 0 1 3 6C1.3 6 0 4.7 0 3s1.3-3 3-3 3 1.3 3 3c0 .663-.2 1.263-.542 1.751l2.705 2.705A2.98 2.98 0 0 1 9.9 6.9c.699 0 1.34.24 1.85.641l2.791-2.791A3.03 3.03 0 0 1 14 3c0-1.7 1.3-3 3-3M3 15c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m14 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M3 1c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m14 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2"];
})), mJ, hJ = o((() => {
	mJ = ["M13 8H5c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m0 3H5c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m0-6H5c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m6.56 12.44-3.23-3.23A8.94 8.94 0 0 0 18 9a9 9 0 1 0-9 9c1.94 0 3.74-.62 5.21-1.67l3.23 3.23a1.498 1.498 0 1 0 2.12-2.12M9 16c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7"];
})), gJ, _J = o((() => {
	gJ = ["m19.56 17.44-3.23-3.23A8.94 8.94 0 0 0 18 9a9 9 0 1 0-9 9c1.94 0 3.74-.62 5.21-1.67l3.23 3.23a1.498 1.498 0 1 0 2.12-2.12M9 16c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7m3.5-11h-7c-.28 0-.5.22-.5.5v2c0 .28.22.5.5.5s.5-.22.5-.5V7h2v6h-.5c-.28 0-.5.22-.5.5s.22.5.5.5h3c.28 0 .5-.22.5-.5s-.22-.5-.5-.5H10V7h2v.5c0 .28.22.5.5.5s.5-.22.5-.5v-2c0-.28-.22-.5-.5-.5"];
})), vJ, yJ = o((() => {
	vJ = ["M19 5H1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-1 8h-8V7h8z"];
})), bJ, xJ = o((() => {
	bJ = ["m19.71 18.29-4.25-4.25L20 12.91 9.93 9.33c.04-.1.07-.21.07-.33V3c0-.55-.45-1-1-1H4V1c0-.55-.45-1-1-1S2 .45 2 1v1H1c-.55 0-1 .45-1 1s.45 1 1 1h1v5c0 .55.45 1 1 1h6c.12 0 .23-.03.34-.07L12.91 20l1.14-4.54 4.25 4.25c.17.18.42.29.7.29a1.003 1.003 0 0 0 .71-1.71M8 8H4V4h4z"];
})), SJ, CJ = o((() => {
	SJ = ["M10 0c5.52 0 10 4.48 10 10s-4.48 10-10 10S0 15.52 0 10 4.48 0 10 0m0 2c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8m0 4a4 4 0 1 1 0 8 4 4 0 0 1 0-8"];
})), wJ, TJ = o((() => {
	wJ = ["M5 0H1a1 1 0 0 0-1 1v4h2V2h3zm13 15v3h-3v2h4a1 1 0 0 0 1-1v-4zM0 18v-3h2v3h3v2H1a1 1 0 0 1-1-1zM15 0h4a1 1 0 0 1 1 1v4h-2V2h-3zM8 0h4v2H8zm10 8v4h2V8zM0 12V8h2v4zm12 6H8v2h4z"];
})), EJ, DJ = o((() => {
	EJ = ["M2 0h3v2H2v3H0V1a1 1 0 0 1 1-1zm16 18v-3h2v4a1 1 0 0 1-1 1h-4v-2zM0 15v4a1 1 0 0 0 1 1h4v-2H2v-3zM18 0h-3v2h3v3h2V1a1 1 0 0 0-1-1zm-6 0H8v2h4zM0 8v4h2V8zm9-2a1 1 0 0 1 2 0v3h3a1 1 0 1 1 0 2h-3v3a1 1 0 1 1-2 0v-3H6a1 1 0 1 1 0-2h3zm11 6h-2V8h2zM8 20v-2h4v2z"];
})), OJ, kJ = o((() => {
	OJ = ["M5 0H1a1 1 0 0 0-1 1v4h2V2h3zm13 15v3h-3v2h4a1 1 0 0 0 1-1v-4zM0 18v-3h2v3h3v2H1a1 1 0 0 1-1-1zM8 0h4v2H8zm10 8v4h2V8zM0 12V8h2v4zm12 6H8v2h4zM19.548.452a1.543 1.543 0 0 0-2.182 0l-1.091 1.091 2.182 2.182 1.091-1.09a1.543 1.543 0 0 0 0-2.183m-4 1.818 2.181 2.183-8.001 8.001-2.182-2.182zM6.817 11 9 13.182 5 15z"];
})), AJ, jJ = o((() => {
	AJ = ["M5 0v2H2v3H0V1a1 1 0 0 1 1-1zm13 18v-3h2v4a1 1 0 0 1-1 1h-4v-2zM0 15v4a1 1 0 0 0 1 1h4v-2H2v-3zM15 0v2h3v3h2V1a1 1 0 0 0-1-1zm-3 0H8v2h4zM0 8v4h2V8zm20 4h-2V8h2zM8 20v-2h4v2zm-1.999-8.993a1 1 0 1 1 0-2h8a1 1 0 0 1 0 2z"];
})), MJ, NJ = o((() => {
	MJ = ["M10.707 19.707a1 1 0 0 1-1.414 0l-4-4a1 1 0 1 1 1.414-1.414L9 16.586V11H1a1 1 0 1 1 0-2h8V6H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-8v3h8a1 1 0 1 1 0 2h-8v5.586l2.293-2.293a1 1 0 0 1 1.414 1.414z"];
})), PJ, FJ = o((() => {
	PJ = ["M1.754.135 19.393 9.06c.57.288.775.943.458 1.462-.107.176-.266.32-.458.418l-17.64 8.925c-.57.288-1.288.1-1.604-.418C.05 19.287 0 19.183 0 19v-7l11-2L0 8V1.075C0 .481.529 0 1.18 0c.201 0 .399.047.574.135"];
})), IJ, LJ = o((() => {
	IJ = ["M19 0h-5c-.6 0-1 .4-1 1s.4 1 1 1h2.6l-4.3 4.3c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3L18 3.4V6c0 .5.5 1 1 1s1-.5 1-1V1c0-.6-.5-1-1-1m0 9c-1 0-1.9-.5-2.5-1.3l-1.4 1.4c-.5.6-1.3.9-2.1.9-1.7 0-3-1.3-3-3 0-.8.3-1.6.9-2.1l1.4-1.4C11.5 2.9 11 2 11 1c0-.3.1-.6.2-.9-.4-.1-.8-.1-1.2-.1C4.5 0 0 4.5 0 10s4.5 10 10 10 10-4.5 10-10c0-.4 0-.8-.1-1.2-.3.1-.6.2-.9.2"];
})), RJ, zJ = o((() => {
	RJ = ["M8 11H3c-.55 0-1 .45-1 1s.45 1 1 1h2.59L.3 18.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L7 14.41V17c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1m10 2c-.53 0-1.01.21-1.37.55L11.9 10.6c.06-.19.1-.39.1-.6s-.04-.41-.1-.6l4.72-2.95c.37.34.85.55 1.38.55 1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .21.04.41.1.6l-4.73 2.96c-.24-.23-.54-.4-.87-.48V3.93c.86-.22 1.5-1 1.5-1.93 0-1.1-.9-2-2-2S8 .9 8 2c0 .93.64 1.71 1.5 1.93v4.14c-.33.09-.63.26-.87.48L7.6 7.91 5.42 6.55 3.9 5.6c.06-.19.1-.39.1-.6 0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2c.53 0 1.01-.21 1.37-.55L9 9.96V10h.06L12 11.84l.4.25 1.51.94 2.19 1.37c-.06.19-.1.39-.1.6 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2m-7-2.96-.06-.04H11z"];
})), BJ, VJ = o((() => {
	BJ = ["M8 11H3c-.55 0-1 .45-1 1s.45 1 1 1h2.59L.3 18.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L7 14.41V17c0 .55.45 1 1 1s1-.45 1-1v-5c0-.55-.45-1-1-1m11.54-6.82.01-.02-6-4-.01.02C13.39.08 13.21 0 13 0s-.39.08-.54.18l-.01-.02L7 3.8 1.55.17l-.01.01A.97.97 0 0 0 1 0C.45 0 0 .45 0 1v9c0-.55.45-1 1-1h1V2.87l4 2.67V9h2V5.54l4-2.67v11.6l-1 .67v2.4l2-1.33 5.45 3.63.01-.02c.15.1.33.18.54.18.55 0 1-.45 1-1V5c0-.35-.19-.64-.46-.82M18 17.13l-4-2.67V2.87l4 2.67z"];
})), HJ, UJ = o((() => {
	HJ = ["M13.238 14c.234 0 .46.082.64.232L16 16h2v2H2v-2h2l2.122-1.768a1 1 0 0 1 .64-.231zM10 11a1 1 0 1 1 0 2 1 1 0 0 1 0-2M6.269 8.64c1.949-2.09 5.298-2.279 7.457-.01a1 1 0 0 1-.04 1.41c-.4.38-1.03.36-1.42-.03-1.33-1.4-3.349-1.29-4.538-.01a.997.997 0 1 1-1.459-1.36m3.733-5.636c2.699 0 5.298 1.3 6.797 3.4.1.2.2.4.2.6 0 .3-.1.6-.4.8-.5.399-1.1.299-1.4-.201-1.1-1.6-3.198-2.6-5.197-2.6-2.1 0-3.899.9-5.198 2.6-.3.5-1 .5-1.4.2-.5-.3-.499-1-.199-1.4 1.7-2.199 3.998-3.489 6.797-3.399"];
})), WJ, GJ = o((() => {
	WJ = ["M13.29 9.29c.3.62.8 1.12 1.42 1.42l-3 3c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L7 10.41l-5 5V17h17c.55 0 1 .45 1 1s-.45 1-1 1H1a1 1 0 0 1-1-1V4c0-.55.45-1 1-1s1 .45 1 1v8.59l4.29-4.3C6.47 8.11 6.72 8 7 8s.53.11.71.29l3.29 3.3zM12 5c0-.5.4-1 1-1h2V2c0-.6.4-1 1-1 .5 0 1 .4 1 1v2h2c.5 0 1 .4 1 1s-.5 1-1 1h-2v2c0 .6-.5 1-1 1-.6 0-1-.4-1-1V6h-2c-.6 0-1-.4-1-1"];
})), KJ, qJ = o((() => {
	KJ = ["M11.91 10.67c.52.45 1.13.8 1.8 1.03l-2.01 2.01c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L7 10.41l-5 5V17h16.99c.55 0 1 .45 1 1s-.45 1-1 1H1a1 1 0 0 1-1-1V4c0-.55.45-1 1-1s1 .45 1 1v8.59l4.29-4.3C6.47 8.11 6.72 8 7 8s.53.11.71.29l3.29 3.3zM18.5 4.6h1.04c.25 0 .45.2.46.44v.9c0 .25-.2.45-.45.45h-1.04c-.07.22-.16.42-.27.62l.73.73c.17.17.17.44 0 .61l-.61.61c-.17.17-.44.17-.61 0l-.73-.73c-.2.11-.4.2-.62.26v1.05c0 .25-.2.45-.45.45h-.9c-.25 0-.45-.2-.45-.45V8.51c-.21-.06-.4-.15-.58-.25l-.76.77c-.17.17-.46.17-.64 0l-.64-.64a.465.465 0 0 1 0-.64l.76-.77c-.1-.19-.19-.38-.25-.59h-1.04c-.25 0-.45-.2-.45-.45v-.9c0-.25.2-.45.45-.45h1.04c.07-.22.16-.42.27-.61l-.73-.73a.43.43 0 0 1 0-.61l.61-.61c.17-.17.44-.17.61 0l.73.73c.2-.11.4-.2.62-.26V1.45a.44.44 0 0 1 .44-.45h.9c.25 0 .45.2.45.45V2.5c.21.06.4.15.58.25l.76-.77c.17-.17.46-.17.64 0l.64.64c.17.17.17.46 0 .64l-.76.77c.1.17.19.36.25.57m-4.69.9c0 .93.75 1.69 1.69 1.69.93 0 1.69-.75 1.69-1.69s-.75-1.69-1.69-1.69-1.69.76-1.69 1.69"];
})), JJ, YJ = o((() => {
	JJ = ["M18.82 6.58c-.03.05-.07.09-.11.13 0 0 0-.01-.01-.01l-2 2c-.2.2-.4.3-.7.3-.6 0-1-.4-1-1 0-.3.1-.5.3-.7L16.6 6H11c-.6 0-1-.4-1-1s.4-1 1-1h5.6l-1.3-1.3c-.2-.2-.3-.4-.3-.7 0-.6.4-1 1-1 .3 0 .5.1.7.3l3 3c.2.2.3.4.3.7s-.1.5-.3.7zm-5.53 2.71c.3.62.8 1.12 1.42 1.42l-3 3c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L7 10.41l-5 5V17h17c.55 0 1 .45 1 1s-.45 1-1 1H1a1 1 0 0 1-1-1V4c0-.55.45-1 1-1s1 .45 1 1v8.59l4.29-4.3C6.47 8.11 6.72 8 7 8s.53.11.71.29l3.29 3.3z"];
})), XJ, ZJ = o((() => {
	XJ = ["M12.14 10.45c.21.67.65 1.23 1.22 1.61l-1.65 1.65c-.18.18-.43.29-.71.29s-.53-.11-.71-.3L7 10.41l-5 5V17h17c.55 0 1 .45 1 1s-.45 1-1 1H1a1 1 0 0 1-1-1V4c0-.55.45-1 1-1s1 .45 1 1v8.59l4.29-4.3C6.47 8.11 6.72 8 7 8s.53.11.71.29l3.29 3.3zM19.35 1a.642.642 0 0 1 .46 1.1l-3.03 3.03v2.95c0 .18-.07.34-.19.46l-1.28 1.29c-.11.1-.27.17-.45.17-.35 0-.64-.29-.64-.64V5.13L11.19 2.1a.642.642 0 0 1 .45-1.1z"];
})), QJ, $J = o((() => {
	QJ = ["m11.28 11.31-.28.28-3.29-3.3C7.53 8.11 7.28 8 7 8s-.53.11-.71.29L2 12.59V4c0-.55-.45-1-1-1s-1 .45-1 1v14a1 1 0 0 0 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1H2v-1.59l5-5 3.29 3.29c.18.19.43.3.71.3s.53-.11.71-.29l2.09-2.09c-.17.02-.34.02-.51.02-.7 0-1.38-.12-2.01-.33m-.93-6c0-1.62 1.31-2.93 2.93-2.93s2.93 1.31 2.93 2.93-1.31 2.93-2.93 2.93-2.93-1.31-2.93-2.93m6.47 2.43c.11-.17.21-.33.29-.51.01-.03.03-.06.04-.09.08-.18.16-.35.21-.54.06-.2.1-.38.14-.58.01-.05.01-.09.02-.14.03-.2.05-.39.05-.6 0-2.37-1.93-4.3-4.3-4.3-2.37.01-4.3 1.93-4.3 4.31s1.93 4.3 4.3 4.3c.21 0 .4-.02.6-.05.04 0 .09-.01.14-.02.2-.03.38-.08.57-.14.2-.06.37-.14.55-.21.03-.01.06-.03.09-.04.18-.09.34-.19.51-.29l2.87 2.87c.14.14.33.22.56.22.43 0 .78-.35.78-.78a.94.94 0 0 0-.23-.56z"];
})), eY, tY = o((() => {
	eY = ["M13.75 0C14.44 0 15 .56 15 1.25v12.5c0 .69-.56 1.25-1.25 1.25h-7.5C5.56 15 5 14.44 5 13.75V1.25C5 .56 5.56 0 6.25 0zM11.5 2a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5zM11 6.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5m.5 3.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5zm-7.5.726v3.024A2.25 2.25 0 0 0 6.25 16h7.5A2.25 2.25 0 0 0 16 13.75v-3.024l3.607 2.618a.97.97 0 0 1 .131 1.443l-4.5 4.875a1.07 1.07 0 0 1-.786.338H5.548c-.3 0-.586-.123-.785-.338L.262 14.787a.97.97 0 0 1 .13-1.443z"];
})), nY, rY = o((() => {
	nY = ["M17.29 4.295a1.002 1.002 0 0 1 1.42 1.419l-3 2.997a1.015 1.015 0 0 1-1.42 0l-3-2.997a1.002 1.002 0 0 1 1.42-1.419L14 5.584V1a1 1 0 0 1 2 0v4.584zM13.267 0A2 2 0 0 0 13 1v2.27a2.002 2.002 0 0 0-2.417 3.152l3.01 3.006.01.01c.359.34.85.563 1.397.563v3.749c0 .69-.56 1.25-1.25 1.25h-7.5C5.56 15 5 14.44 5 13.75V1.25C5 .56 5.56 0 6.25 0zM4 10.726.393 13.344a.97.97 0 0 0-.131 1.443l4.5 4.875c.2.215.485.338.786.338h8.904c.3 0 .586-.123.785-.338l4.501-4.875a.97.97 0 0 0-.13-1.443L16 10.726v3.024A2.25 2.25 0 0 1 13.75 16h-7.5A2.25 2.25 0 0 1 4 13.75z"];
})), iY, aY = o((() => {
	iY = ["M4 1c0-.55-.45-1-1-1S2 .45 2 1v5h2zM2 19c0 .55.45 1 1 1s1-.45 1-1v-6H2zm9-18c0-.55-.45-1-1-1S9 .45 9 1v8h2zm7 0c0-.55-.45-1-1-1s-1 .45-1 1v3h2zM9 19c0 .55.45 1 1 1s1-.45 1-1v-3H9zm9-14h-2c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1m-2 14c0 .55.45 1 1 1s1-.45 1-1v-8h-2zM4 7H2c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m7 3H9c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1"];
})), oY, sY = o((() => {
	oY = ["M7.88 11.12a.96.96 0 0 1 1.277.33l3.719 6.207c.081.136.124.29.124.447 0 .495-.419.896-.936.896H4.936a1 1 0 0 1-.436-.103.88.88 0 0 1-.392-1.21l3.409-6.208a.9.9 0 0 1 .362-.36M15 5a4 4 0 1 1 0 8 4 4 0 0 1 0-8M8 1a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"];
})), cY, lY = o((() => {
	cY = ["M15 18H2V5h8.76l2-2H1c-.55 0-1 .45-1 1v15c0 .55.45 1 1 1h15c.55 0 1-.45 1-1V7.24l-2 2zm4-18h-7c-.55 0-1 .45-1 1s.45 1 1 1h4.59l-7.3 7.29a1.003 1.003 0 0 0 1.42 1.42L18 3.41V8c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1"];
})), uY, dY = o((() => {
	uY = ["M13.917 17.209c1.01.454 2.543.928 2.873 1.643.31.722.186 1.148.186 1.148H6.026s-.13-.426.186-1.148 1.842-1.203 2.86-1.65.914-.722.948-1.093c0-.048.007-.097.007-.145a3.1 3.1 0 0 1-.839-1.237l-.007-.007c0-.007-.006-.014-.006-.02a2 2 0 0 1-.11-.337c-.234-.042-.372-.296-.426-.537a1.05 1.05 0 0 1-.138-.598c.034-.35.179-.509.337-.57v-.056c0-.44.034-1.065.117-1.478q.021-.177.075-.343a2.5 2.5 0 0 1 .887-1.28c.426-.33 1.038-.501 1.58-.501.544 0 1.155.172 1.588.502a2.5 2.5 0 0 1 .963 1.622c.075.413.117 1.045.117 1.478v.062c.15.062.288.22.323.564.02.268-.083.502-.138.598-.048.234-.185.488-.42.537a3 3 0 0 1-.116.364 3.1 3.1 0 0 1-.818 1.224q-.002.084.007.158c.034.378-.103.653.914 1.1m1.059-.639c-.24-.099-.455-.186-.65-.273l-.007-.004a4 4 0 0 1-.194-.091c.224-.288.41-.609.554-.946l.001-.002.013-.033q.028-.065.052-.13l.011-.027.016-.04c.105-.092.19-.19.256-.284a1.9 1.9 0 0 0 .265-.562c.105-.227.225-.593.192-1.027l-.001-.011-.002-.011a1.85 1.85 0 0 0-.325-.91 10 10 0 0 0-.12-1.246 3 3 0 0 0-.106-.475l-.001-.006a3.54 3.54 0 0 0-.763-1.353c.27-.092.56-.139.83-.139.495 0 1.05.156 1.444.456a2.27 2.27 0 0 1 .875 1.475c.069.375.106.95.106 1.344v.056c.138.056.263.2.294.513a1 1 0 0 1-.125.543c-.044.213-.169.444-.381.488-.025.1-.056.206-.094.3a2.8 2.8 0 0 1-.756 1.144q-.002.076.006.144.006.065.007.127c.01.283.018.518.824.872.192.087.404.173.623.263.83.34 1.752.717 1.99 1.231.28.657.168 1.044.168 1.044h-2.081a4 4 0 0 0-.188-.542l-.005-.013-.006-.012c-.183-.397-.491-.681-.76-.88a5.6 5.6 0 0 0-.896-.522 17 17 0 0 0-.916-.4zM14 1c.55 0 1 .45 1 1 0 .28-.11.53-.29.7L10 7.41v.897a3.2 3.2 0 0 0-.69.4 3.5 3.5 0 0 0-1.343 2.259c-.07.37-.107.836-.122 1.237a1.84 1.84 0 0 0-.339.926c-.046.458.09.84.195 1.06.053.178.138.376.27.56q.083.121.21.242v.143l.053.052L6.71 16.71A1.003 1.003 0 0 1 5 16V7.41L.29 2.71A1.003 1.003 0 0 1 1 1zM9.059 14.361c-.23-.044-.366-.296-.42-.535a1.05 1.05 0 0 1-.138-.598c.034-.35.179-.509.337-.57v-.056c0-.44.034-1.065.117-1.478q.021-.177.075-.343A2.5 2.5 0 0 1 10 9.44V13c0 .28-.11.53-.29.71z"];
})), fY, pY = o((() => {
	fY = ["M10 20q9-5.715 9-15.714-3 0-9-4.286-6 4.286-9 4.286Q1 14.285 10 20m0-17.348c2.577 1.734 4.776 2.88 6.667 3.419-.44 4.627-2.636 8.353-6.667 11.297z"];
})), mY, hY = o((() => {
	mY = ["M6.84.804 6.5 2.5h-3a1 1 0 0 0-1 1v4.893l-1.58.451a.99.99 0 0 0-.691 1.192c.46 1.82 1.163 4.356 1.701 5.571q-.327.018-.68.018a.625.625 0 0 0 0 1.25c2.583 0 4.268-.68 5.202-1.146.687.466 1.88 1.146 3.548 1.146 1.65 0 2.837-.666 3.528-1.132l.005.003c.244.131.6.3 1.07.468.938.335 2.321.661 4.147.661a.624.624 0 1 0 0-1.25q-.484 0-.922-.031a1 1 0 0 0 .184-.334l1.67-5.168a1 1 0 0 0-.677-1.27l-1.505-.43V3.5a1 1 0 0 0-1-1h-3L13.16.804A1 1 0 0 0 12.18 0H7.82a1 1 0 0 0-.98.804M5 7.679V5h3.75v1.607zm6.25-1.072V5H15v2.68zM6.205 16.95a.63.63 0 0 1 .658.042c.569.407 1.597 1.134 3.137 1.134s2.568-.727 3.137-1.134a.625.625 0 0 1 .724-.001l.007.005.045.029q.066.042.21.12a6.6 6.6 0 0 0 .9.392c.811.29 2.053.589 3.727.589a.624.624 0 1 1 0 1.25c-1.826 0-3.21-.326-4.148-.661a8 8 0 0 1-1.069-.468l-.005-.003c-.691.466-1.878 1.132-3.528 1.132-1.667 0-2.861-.68-3.548-1.146-.934.467-2.619 1.146-5.202 1.146a.625.625 0 1 1 0-1.25c2.66 0 4.23-.787 4.955-1.176"];
})), gY, _Y = o((() => {
	gY = ["M17.94 3.63c-.01-.02-.01-.03-.02-.04l-.03-.09h-.01c-.18-.3-.49-.5-.86-.5h-14c-.42 0-.77.25-.92.61L0 8.5h.02a2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0zM3.02 2h14c.55 0 1-.45 1-1s-.45-1-1-1h-14c-.55 0-1 .45-1 1s.44 1 1 1m13 14h-12v-4h-2v7c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-7h-2z"];
})), vY, yY = o((() => {
	vY = ["M18 14H8.72l-.67-2H17c.44 0 .8-.29.94-.69h.01l2-6h-.01c.03-.1.06-.2.06-.31 0-.55-.45-1-1-1H5.39l-.44-1.32h-.01C4.8 2.29 4.44 2 4 2H1c-.55 0-1 .45-1 1s.45 1 1 1h2.28l3.33 10H5c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2h9c0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2M6.05 6h11.56l-1.33 4H7.39z"];
})), bY, xY = o((() => {
	bY = ["M.833 13h8.334c.458 0 .833-.45.833-1s-.375-1-.833-1H.833C.375 11 0 11.45 0 12s.375 1 .833 1M1 8h18c.55 0 1-.45 1-1s-.45-1-1-1H1c-.55 0-1 .45-1 1s.45 1 1 1m15 6c0-.28-.11-.53-.29-.71l-.3-.29H19c.55 0 1-.45 1-1s-.45-1-1-1h-3.59l.29-.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-2 2c-.18.19-.29.44-.29.71 0 .28.11.53.29.71l2 2c.18.18.43.29.71.29.55.01 1-.44 1-1"];
})), SY, CY = o((() => {
	SY = ["M7.15 10.33c.888.8 1.999 1.36 3.228 1.574l2.326 6.98a.846.846 0 0 1-.535 1.07.844.844 0 0 1-1.072-.535l-1.225-3.671H7.125L5.9 19.419a.85.85 0 0 1-1.072.536.85.85 0 0 1-.536-1.071zm1.353 1.305-.808 2.413h1.607zM5 5.5c0 .76.13 1.49.37 2.17-.496 1.056-.313 2.356.704 3.29.385.353.404.94.038 1.311a.98.98 0 0 1-1.356.038c-2.183-2.01-2-5.125.01-6.94a1 1 0 0 1 .24-.156A6 6 0 0 0 5 5.5m-1.126 7.685c-1.346-.918-2.187-2.67-2.187-4.34 0-1.752.757-3.254 2.187-4.339.42-.25.42-.834.168-1.168-.252-.418-.84-.418-1.177-.167C1.014 4.59-.08 6.509.005 8.846c.084 2.253 1.177 4.423 2.86 5.675.168.083.336.166.504.166.253 0 .505-.083.673-.333.337-.418.253-.918-.168-1.169m8.372-.876a.98.98 0 0 1-1.354-.037.9.9 0 0 1-.206-.324q.4.052.814.052.586 0 1.145-.1a5 5 0 0 1-.399.409m2.385-.833 1.228 1.229a6.6 6.6 0 0 1-1.723 1.816c-.169.083-.337.166-.505.166-.253 0-.505-.083-.673-.333-.337-.418-.253-.918.168-1.169.62-.422 1.133-1.022 1.505-1.709M11.5 0C14.54 0 17 2.46 17 5.5q0 .39-.06.75l-.03.17c-.04.25-.1.49-.17.73v.01c-.08.24-.17.47-.28.69-.01.04-.03.07-.05.11-.11.23-.24.44-.38.65l3.68 3.68A1.003 1.003 0 0 1 19 14c-.28 0-.53-.11-.7-.29l-3.68-3.68c-.21.14-.42.27-.65.38-.04.01-.07.03-.11.05-.22.11-.45.2-.69.28h-.01c-.24.07-.48.13-.73.17l-.17.03c-.25.04-.5.06-.76.06C8.46 11 6 8.54 6 5.5S8.46 0 11.5 0m0 1.5c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4"];
})), wY, TY = o((() => {
	wY = ["m16.71 5.29-5-5A1 1 0 0 0 11 0H4c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V6c0-.28-.11-.53-.29-.71M9 7h2v3H9zM6 7h2v3H6zm2 11H6v-3h2zm3 0H9v-3h2zm3 0h-2v-3h2zm0-4H6v-3h8zm0-4h-2V7h2z"];
})), EY, DY = o((() => {
	EY = ["M12 2c-.46 0-.85.32-.97.74L7.04 16.7c-.02.1-.04.2-.04.3 0 .55.45 1 1 1 .46 0 .85-.32.97-.74L12.96 3.3c.02-.1.04-.2.04-.3 0-.55-.45-1-1-1"];
})), OY, kY = o((() => {
	OY = ["m11.41 10 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L10 8.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42L8.59 10 5.3 13.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3.29-3.3 3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"];
})), AY, jY = o((() => {
	AY = ["M17 10a7.001 7.001 0 0 1-11.95 4.95A7 7 0 1 1 17 10m-6-5H9v2h2zm0 3H8v1h1v5H8v1h4v-1h-1z"];
})), MY, NY = o((() => {
	MY = ["M14 9H6c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1"];
})), PY, FY = o((() => {
	PY = ["M14 9h-3V6c0-.55-.45-1-1-1s-1 .45-1 1v3H6c-.55 0-1 .45-1 1s.45 1 1 1h3v3c0 .55.45 1 1 1s1-.45 1-1v-3h3c.55 0 1-.45 1-1s-.45-1-1-1"];
})), IY, LY = o((() => {
	IY = ["M5 5v10h10V5zM4 3h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1"];
})), RY, zY = o((() => {
	RY = ["M15 5c-.28 0-.53.11-.71.29L8 11.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l7-7A1.003 1.003 0 0 0 15 5"];
})), BY, VY = o((() => {
	BY = ["M11 11.776v2.81l2.31 2.242a.987.987 0 0 1 0 1.415c-.399.39-1.044.39-1.442 0L11 17.414V19a.99.99 0 0 1-.996 1A.996.996 0 0 1 9 19v-1.636l-.912.879c-.398.39-1.043.39-1.441 0a.987.987 0 0 1 0-1.415L9 14.536v-2.79l-2.548 1.435-.837 3.063c-.146.534-.705.85-1.248.707a1 1 0 0 1-.721-1.224l.309-1.132-1.4.793a1.03 1.03 0 0 1-1.393-.366.99.99 0 0 1 .373-1.366l1.445-.818-1.224-.322a1 1 0 0 1-.72-1.225 1.02 1.02 0 0 1 1.248-.707l3.193.84 2.462-1.395-2.532-1.434-3.123.82a1.02 1.02 0 0 1-1.249-.706 1 1 0 0 1 .721-1.225L2.91 7.18l-1.4-.793a.99.99 0 0 1-.373-1.366 1.03 1.03 0 0 1 1.392-.366l1.445.818-.328-1.2a1 1 0 0 1 .72-1.225 1.02 1.02 0 0 1 1.25.707l.855 3.132L9 8.311V5.414L6.647 3.121a.987.987 0 0 1 0-1.414 1.033 1.033 0 0 1 1.441 0L9 2.586V1c0-.552.44-1 1.004-1A.99.99 0 0 1 11 1l-.007 1.536.875-.829a1.033 1.033 0 0 1 1.441 0 .987.987 0 0 1 0 1.414L11 5.364v2.918l2.53-1.42.855-3.131c.146-.534.705-.85 1.249-.707a1 1 0 0 1 .72 1.224l-.327 1.2 1.4-.792a1.03 1.03 0 0 1 1.392.366.99.99 0 0 1-.373 1.366l-1.355.768 1.153.303a1 1 0 0 1 .721 1.225c-.146.533-.705.85-1.249.707l-3.123-.821-2.576 1.459 2.506 1.42 3.193-.84a1.02 1.02 0 0 1 1.249.707 1 1 0 0 1-.72 1.225l-1.224.322 1.4.793a.99.99 0 0 1 .373 1.366 1.03 1.03 0 0 1-1.393.366l-1.356-.768.31 1.132a1 1 0 0 1-.721 1.224 1.02 1.02 0 0 1-1.249-.707l-.837-3.063z"];
})), HY, UY = o((() => {
	HY = ["M9.5 19a9.5 9.5 0 1 0 0-19 9.5 9.5 0 0 0 0 19m0-2a7.5 7.5 0 0 1-2.313-.363l-.665-2.048 1.152-1.585h3.824l1.152 1.585-.644 1.982A7.5 7.5 0 0 1 9.5 17m-6-2.999A7.47 7.47 0 0 1 2 9.5v-.05l1.557-1.132 2.337.76 1.038 3.246L5.712 14zM17 9.5a7.47 7.47 0 0 1-1.5 4.501h-2.04l-1.339-1.842.976-3.05 2.432-.79 1.47 1.068zM3.225 5.391a7.53 7.53 0 0 1 3.539-2.876l2.232 1.622v1.885L6.163 8.113l-2.296-.746zM15.22 7.367l-2.357.766-2.867-2.117v-1.88l2.235-1.623a7.53 7.53 0 0 1 3.602 2.967z"];
})), WY, GY = o((() => {
	WY = ["M11.5 5c.8 0 1.6-.4 2-1 2 1.2 3.3 3.3 3.5 5.7 0 .5.5.9 1 .9.6 0 1-.5 1-1v-.1c-.2-3.3-2.2-6.2-5.1-7.6C13.7.8 12.7 0 11.5 0 10.1 0 9 1.1 9 2.5S10.1 5 11.5 5m5 7c-1.4 0-2.5 1.1-2.5 2.5 0 .4.1.7.2 1.1-1.1.9-2.6 1.4-4.2 1.4-1.9 0-3.6-.8-4.9-2-.2-.2-.5-.4-.8-.4-.5 0-1 .5-1 1 0 .3.1.5.3.7C5.3 18 7.5 19 10 19c2.2 0 4.2-.8 5.8-2.1.2.1.5.1.7.1 1.4 0 2.5-1.1 2.5-2.5S17.9 12 16.5 12M5 10.5c0-1.1-.7-2.1-1.7-2.4.5-1.9 1.9-3.5 3.6-4.4.3-.2.6-.5.6-.9 0-.5-.4-1-1-1-.2 0-.4.1-.6.2-2.4 1.2-4.2 3.6-4.7 6.4C.5 8.9 0 9.6 0 10.5 0 11.9 1.1 13 2.5 13S5 11.9 5 10.5"];
})), KY, qY = o((() => {
	KY = ["M19 16h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m0-5h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1M7 15c-.28 0-.53.11-.71.29L5 16.59V11c0-.55-.45-1-1-1s-1 .45-1 1v5.59L1.71 15.3A.97.97 0 0 0 1 15a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 7 15M19 1h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1m0 5h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1"];
})), JY, YY = o((() => {
	JY = ["M8 15c-.28 0-.53.11-.71.29L6 16.59v-5.58c0-.55-.45-1-1-1s-1 .45-1 1v5.58L2.71 15.3c-.18-.18-.43-.3-.71-.3a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 8 15m8.89-.79v-1.22H11.3v1.3h3.51L11 18.78V20h5.99v-1.3h-3.91zM14.97 0h-1.95L9.01 11.01h1.89l.98-2.92h4.17l.98 2.92h1.96zm-2.59 6.63 1.58-4.74H14l1.57 4.74z"];
})), XY, ZY = o((() => {
	XY = ["M8.01 15c-.28 0-.53.11-.71.29L6 16.59v-5.58c0-.55-.45-1-1-1s-1 .45-1 1v5.58L2.71 15.3c-.18-.18-.43-.3-.71-.3a1.003 1.003 0 0 0-.71 1.71l3 3a1.014 1.014 0 0 0 1.42 0l3-3c.18-.18.29-.43.29-.71.01-.55-.44-1-.99-1m4.44-5.65 6.4-7.88V0H10.5v1.67h5.91L10 9.44v1.57h9V9.35zm1.27 3.64L11 20h1.59l.56-1.56h2.68l.55 1.56h1.64l-2.68-7.01zm-.16 4.3.93-2.57h.02l.9 2.57z"];
})), QY, $Y = o((() => {
	QY = ["M10 8h5c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1h-5c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m0 5h7c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1h-7c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m0-10h3c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1h-3c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m9 12h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1M7 14c-.28 0-.53.11-.71.29L5 15.59V10c0-.55-.45-1-1-1s-1 .45-1 1v5.59L1.71 14.3A.97.97 0 0 0 1 14a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 7 14"];
})), eX, tX = o((() => {
	eX = ["M13 15h-3c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m-6-1c-.28 0-.53.11-.71.29L5 15.59V10c0-.55-.45-1-1-1s-1 .45-1 1v5.59L1.71 14.3A.97.97 0 0 0 1 14a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 7 14M19 0h-9c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h9c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-4 10h-5c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h5c.55 0 1-.45 1-1v-1c0-.55-.45-1-1-1m2-5h-7c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1"];
})), nX, rX = o((() => {
	nX = ["M9 14.99c-.28 0-.53.11-.71.29L7 16.58v-5.59c0-.55-.45-1-1-1s-1 .45-1 1v5.59l-1.29-1.29a.97.97 0 0 0-.71-.3 1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3c.18-.18.29-.43.29-.71a.99.99 0 0 0-1-1m8.88.23c-.08-.42-.22-.79-.42-1.12s-.47-.6-.8-.8-.76-.3-1.28-.3a2.33 2.33 0 0 0-1.72.71c-.21.22-.37.48-.49.78-.11.3-.17.62-.17.97 0 .27.04.54.13.8.08.26.22.5.4.7.19.21.43.38.71.5a2.14 2.14 0 0 0 1.72.02c.25-.12.47-.31.66-.58l.02.02c-.01.19-.04.4-.08.63-.04.24-.11.46-.21.67s-.23.38-.39.53a.92.92 0 0 1-.62.22c-.24 0-.44-.08-.6-.25s-.27-.36-.31-.59h-1.31c.04.29.12.56.24.79s.28.43.48.59c.19.16.42.28.67.36s.52.12.82.12c.49 0 .9-.1 1.23-.31.34-.21.61-.48.82-.82s.37-.71.47-1.13.15-.83.15-1.25q0-.645-.12-1.26m-1.42.63c-.05.15-.11.28-.2.4s-.2.21-.34.27-.3.1-.49.1c-.17 0-.33-.04-.46-.11s-.24-.17-.33-.29c-.08-.12-.15-.25-.19-.4s-.06-.31-.06-.47c0-.15.02-.3.07-.45s.11-.28.2-.39c.09-.12.2-.21.33-.28s.27-.11.44-.11.33.04.47.11.25.17.34.28a1.4 1.4 0 0 1 .28.86c.01.17-.02.33-.06.48M15.32 11H17V0h-1.25c-.05.34-.17.62-.34.85s-.39.42-.63.57c-.25.15-.52.25-.83.31-.3.06-.62.09-.94.09v1.41h2.31z"];
})), iX, aX = o((() => {
	iX = ["M9 15c-.28 0-.53.11-.71.29L7 16.59v-5.58c0-.55-.45-1-1-1s-1 .45-1 1v5.58L3.71 15.3c-.18-.18-.43-.3-.71-.3a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 9 15m6.7-1.33a1.5 1.5 0 0 1-.44.43c-.17.11-.37.19-.58.23-.22.04-.44.06-.67.05v1.07h1.66V20H17v-6.99h-1.06q-.06.39-.24.66m3.15-10.3c-.11-.68-.29-1.26-.55-1.76S17.68.72 17.22.43C16.75.14 16.17 0 15.46 0c-.54 0-1.03.09-1.46.27s-.79.44-1.09.76c-.3.33-.52.71-.67 1.15-.16.44-.24.92-.24 1.43 0 .54.08 1.04.23 1.47.15.44.37.81.65 1.12s.61.55 1 .72.82.26 1.3.26q.69 0 1.26-.33c.38-.22.68-.53.9-.94l.03.03c-.03.35-.07.74-.12 1.16s-.15.81-.29 1.18-.35.68-.61.92c-.26.25-.62.37-1.06.37-.43 0-.77-.13-1.03-.4-.25-.27-.4-.62-.44-1.05h-1.64c.02.43.11.83.29 1.18.17.35.39.66.67.91a3.03 3.03 0 0 0 2.07.8c.71 0 1.3-.17 1.79-.5q.72-.495 1.17-1.29c.3-.53.51-1.12.64-1.76S19 6.18 19 5.54c.01-.77-.05-1.49-.15-2.17M17.1 4.44c-.08.27-.19.5-.34.71s-.34.37-.57.49-.5.18-.8.18-.56-.06-.78-.19-.4-.29-.55-.49c-.14-.2-.25-.44-.32-.7-.07-.27-.11-.55-.11-.84 0-.28.04-.55.11-.82.07-.26.18-.49.32-.7.14-.2.33-.36.55-.48s.48-.17.78-.17c.31 0 .57.06.8.18q.345.18.57.48c.15.2.26.43.34.69s.11.53.11.82-.04.57-.11.84"];
})), oX, sX = o((() => {
	oX = ["m8.89.56 5 10c.06.13.11.28.11.44 0 .55-.45 1-1 1-.39 0-.72-.23-.89-.55L10.88 9H5.12l-1.23 2.44c-.17.33-.5.56-.89.56-.55 0-1-.45-1-1 0-.16.05-.31.12-.44l2.35-4.73.9-1.81L7.11.56C7.28.23 7.61 0 8 0s.72.23.89.56M6.12 7h3.76L8 3.24zm11.17 4.29a1.004 1.004 0 1 1 1.42 1.42l-7 7c-.18.18-.43.29-.71.29s-.53-.11-.71-.29l-3-3a1.003 1.003 0 1 1 1.42-1.42l2.29 2.3z"];
})), cX, lX = o((() => {
	cX = ["M6.308 8.306a1.03 1.03 0 0 1 1.464 0l2.929 2.955.071.08c.332.41.308 1.015-.071 1.398l-2.929 2.955a1.03 1.03 0 0 1-1.464 0 1.05 1.05 0 0 1 0-1.478l1.067-1.077c-1.182.13-2.255.342-3.128.625-1.04.337-1.758.759-2.069 1.217q-.233.347-.154.694.078.348.464.681c.513.44 1.413.826 2.594 1.114s2.598.467 4.088.516 2.995-.034 4.342-.24c1.347-.205 2.483-.525 3.278-.922q.596-.3.905-.635c.206-.224.31-.457.31-.69a1 1 0 0 1 2 0c0 .876-.403 1.569-.837 2.042-.425.463-.958.809-1.484 1.072-1.053.526-2.415.888-3.87 1.11a26 26 0 0 1-4.709.262c-1.599-.052-3.157-.245-4.498-.572-1.28-.312-2.548-.79-3.421-1.54-.454-.389-.935-.966-1.113-1.758-.193-.855.036-1.647.45-2.257.708-1.044 1.99-1.635 3.106-1.996 1.154-.374 2.534-.625 3.99-.756l-1.31-1.322a1.05 1.05 0 0 1 0-1.478m4.929-8a1.03 1.03 0 0 1 1.464 0c.404.408.404 1.07 0 1.478l-1.245 1.255c1.428.076 2.808.265 4.01.563.784.195 1.516.443 2.146.75.604.293 1.253.708 1.726 1.307.52.657.843 1.577.565 2.586-.247.895-.872 1.504-1.416 1.89-1.08.768-2.665 1.249-4.31 1.53a1 1 0 0 1-.337-1.971c1.55-.265 2.776-.683 3.488-1.188.356-.254.572-.521.647-.791.074-.27.009-.546-.205-.816-.212-.268-.563-.521-1.033-.75-.471-.23-1.062-.435-1.753-.606-1.009-.251-2.191-.42-3.443-.496l1.16 1.17a1.05 1.05 0 0 1 0 1.477 1.03 1.03 0 0 1-1.464 0l-2.93-2.955a1.05 1.05 0 0 1-.071-1.399l.071-.079zM4.915 3.514a1 1 0 0 1 .436 1.952c-.761.17-1.415.38-1.937.617-.523.237-.915.503-1.15.786-.24.286-.31.577-.225.861.084.286.328.569.727.834A1.001 1.001 0 0 1 1.66 10.23C1.08 9.845.396 9.228.12 8.298c-.316-1.068.046-2.037.608-2.71.51-.61 1.207-1.03 1.858-1.326.681-.309 1.474-.557 2.329-.748"];
})), uX, dX = o((() => {
	uX = ["M15 13a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-3-3a1.003 1.003 0 0 0-1.42 1.42L16.59 9H11V2h5v2c.77 0 1.47.3 2 .78V1c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v3.78C2.53 4.3 3.23 4 4 4V2h5v7H3.41L4.7 7.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-3 3C.11 9.47 0 9.72 0 10s.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42L3.41 11H9v7H4v-2c-.77 0-1.47-.3-2-.78V19c0 .55.45 1 1 1h14c.55 0 1-.45 1-1v-3.78c-.53.48-1.23.78-2 .78v2h-5v-7h5.59l-1.29 1.29c-.19.18-.3.43-.3.71"];
})), fX, pX = o((() => {
	fX = ["M8 .5a.5.5 0 0 1 .5-.5c.433 0 .5.269.5.269.338-.453.819-.245 1.34-.02.548.236 1.14.492 1.66.02v2.494c-.52.414-1.124.2-1.682.002-.512-.182-.985-.35-1.318-.002V5.02Q9.494 5 10 5c1.422 0 2.775.119 4 .333V1.5a.5.5 0 0 1 .5-.5c.433 0 .5.269.5.269.338-.453.819-.245 1.34-.02.548.236 1.14.492 1.66.02v2.494c-.52.414-1.124.2-1.682.002-.512-.182-.985-.35-1.318-.002v1.772c2.989.692 5 1.984 5 3.465 0 .631-.365 1.228-1.016 1.759C18.704 8.662 14.788 7 10 7s-8.703 1.662-8.984 3.759C.366 10.228 0 9.63 0 9c0-.903.748-1.736 2.009-2.405A.5.5 0 0 1 2 6.5v-5a.5.5 0 0 1 .5-.5c.433 0 .5.269.5.269.338-.453.819-.245 1.34-.02.548.236 1.14.492 1.66.02v2.494c-.52.414-1.124.2-1.682.002-.512-.182-.985-.35-1.318-.002v2.38c1.35-.53 3.075-.907 5-1.063zm9.868 10.969A1 1 0 0 0 18 11c0-.227-.1-.518-.432-.868-.337-.354-.872-.719-1.61-1.047C14.484 8.43 12.378 8 10 8s-4.484.43-5.958 1.085c-.738.328-1.273.693-1.61 1.047-.333.35-.432.641-.432.868 0 .134.035.291.132.469C3.962 12.401 6.807 13 10 13s6.037-.599 7.868-1.531M10 14c2.856 0 5.488-.461 7.442-1.243C18.47 12.347 19.357 11.644 20 11v6c0 1.343-2.943 2.618-7 3v-1a3 3 0 0 0-6 0v1c-4.057-.382-7-1.657-7-3v-6c.72.71 1.626 1.384 2.558 1.757C4.512 13.539 7.144 14 10 14"];
})), mX, hX = o((() => {
	mX = ["M19 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H2V2h16z"];
})), gX, _X = o((() => {
	gX = ["M12 2c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v4h4zm3 14h2c.55 0 1-.45 1-1v-5h-4v5c0 .55.45 1 1 1m3-10c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1v3h4zm-6 1H8v5h4zm-9 9h2c.55 0 1-.45 1-1v-3H2v3c0 .55.45 1 1 1m16 1H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M6 9c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v2h4zm3 7h2c.55 0 1-.45 1-1v-2H8v2c0 .55.45 1 1 1"];
})), vX, yX = o((() => {
	vX = ["M15 7H5a3 3 0 1 0 0 6h10a3 3 0 0 0 0-6M5 5h10a5 5 0 1 1 0 10H5A5 5 0 0 1 5 5"];
})), bX, xX = o((() => {
	bX = ["m10 0 3.1 6.6 6.9 1-5 5.1 1.2 7.3-6.2-3.4L3.8 20 5 12.7 0 7.6l6.9-1z"];
})), SX, CX = o((() => {
	SX = ["m20 7.6-6.9-1.1L10 0 6.9 6.6 0 7.6l5 5.1L3.8 20l6.2-3.4 6.2 3.4-1.2-7.2zM10 15l-4.5 2.4.9-5.2-3.6-3.6 5-.8L10 3.1l2.2 4.7 5 .8-3.6 3.7.9 5.2z"];
})), wX, TX = o((() => {
	wX = ["M15 3c-.23 0-.42.09-.59.21l-.01-.01L8 8V4c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-4l6.4 4.8.01-.01c.17.12.36.21.59.21.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), EX, DX = o((() => {
	EX = ["M19 16H2v-3h4c.55 0 1-.45 1-1V8h3v2c0 .55.45 1 1 1h5c.55 0 1-.45 1-1V6h2c.55 0 1-.45 1-1s-.45-1-1-1h-3c-.55 0-1 .45-1 1v4h-3V7c0-.55-.45-1-1-1H6c-.55 0-1 .45-1 1v4H2V3c0-.55-.45-1-1-1s-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), OX, kX = o((() => {
	OX = ["M15 3h-2c-.55 0-1 .45-1 1v4L5.6 3.2l-.01.01C5.42 3.09 5.23 3 5 3c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1 .23 0 .42-.09.59-.21l.01.01L12 12v4c0 .55.45 1 1 1h2c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), AX, jX = o((() => {
	AX = ["M16 3H4c-.55 0-1 .45-1 1v12c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), MX, NX = o((() => {
	MX = ["M10 6a6 6 0 1 0 6 6h-6zm-.998-1.938L9 4V2H7a1 1 0 1 1 0-2h6a1 1 0 0 1 0 2h-2v2l-.002.062A8.001 8.001 0 0 1 10 20a8 8 0 0 1-.998-15.938"];
})), PX, FX = o((() => {
	PX = ["M18 9h-4.46a5 5 0 0 0-.4-.14c-.19-.05-.51-.14-.96-.25s-.9-.23-1.37-.35-.89-.23-1.27-.33-.6-.16-.65-.17c-.53-.15-.95-.37-1.27-.66-.32-.28-.49-.68-.49-1.19 0-.36.09-.66.26-.9s.39-.43.65-.57q.39-.21.87-.3c.48-.09.63-.09.93-.09.89 0 1.63.19 2.21.57.45.3.75.76.89 1.38h2.63c-.06-.52-.2-.98-.42-1.4-.3-.57-.71-1.05-1.23-1.43a5.3 5.3 0 0 0-1.79-.87c-.7-.2-1.42-.3-2.19-.3-.66 0-1.31.08-1.96.25s-1.22.43-1.73.77-.92.79-1.23 1.32c-.31.52-.46 1.15-.46 1.87 0 .37.05.74.15 1.1s.28.7.53 1.02c.18.24.41.47.69.67H2c-.55 0-1 .45-1 1s.45 1 1 1h10.14c.02.01.05.02.07.02.3.11.58.29.84.55.25.26.38.67.38 1.21 0 .27-.06.53-.17.79q-.165.39-.54.69c-.25.2-.57.36-.97.49s-.88.19-1.44.19c-.52 0-1.01-.06-1.45-.17-.45-.11-.84-.29-1.19-.54s-.61-.56-.8-.95c-.05-.08-.09-.18-.12-.28H4.11c.09.43.22.82.4 1.18q.495.975 1.32 1.59c.55.41 1.2.72 1.94.92q1.11.3 2.37.3c.73 0 1.44-.08 2.14-.25s1.33-.43 1.88-.79.99-.83 1.33-1.39.51-1.25.51-2.05c0-.37-.06-.75-.18-1.12a3 3 0 0 0-.15-.39H18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), IX, LX = o((() => {
	IX = ["M18 18H2V2h12.3l2-2H1C.4 0 0 .4 0 1v18c0 .6.4 1 1 1h18c.6 0 1-.4 1-1V7.7l-2 2zm1.2-18-7.6 7.6 2.8 2.8L20 4.8V0zM4 15.9c3.1.2 5.9.2 8.2-2 1.1-1.1 1.1-3 0-4.1-.6-.5-1.3-.8-2-.8s-1.4.3-1.9.8C7.2 11 6.6 14.3 4 15.9"];
})), RX, zX = o((() => {
	RX = ["M.224 6.63a1 1 0 1 1 1.563-1.248L5 9.4l3.213-4.017A1 1 0 1 1 9.776 6.63L6.28 11l3.495 4.369a1 1 0 1 1-1.563 1.248L5 12.601l-3.213 4.016A1 1 0 1 1 .224 15.37L3.72 11zm15.8 11.33c.16-.19.34-.38.56-.55.21-.18.449-.36.709-.53.25-.18.5-.36.749-.56.25-.2.49-.41.73-.63.229-.22.439-.47.629-.74.18-.27.33-.56.44-.88S20 13.4 20 13c0-.32-.05-.65-.14-1s-.25-.68-.47-.97a2.5 2.5 0 0 0-.869-.74c-.36-.2-.809-.29-1.348-.29-.49 0-.93.1-1.299.29-.37.18-.69.44-.949.78-.26.33-.45.73-.58 1.2-.13.46-.2.96-.2 1.5h1.43c.01-.35.04-.67.09-.97s.14-.56.25-.78.259-.39.449-.52.43-.19.709-.19q.465 0 .75.18c.189.12.339.26.449.43s.18.36.22.56q.06.3.06.57c-.01.38-.1.72-.26 1.02-.15.3-.37.57-.63.83-.26.25-.54.49-.849.71-.31.22-.61.45-.889.68-.6.45-1.059.98-1.408 1.58-.35.61-.52 1.32-.53 2.13h5.984v-1.43h-4.276c.06-.21.17-.42.33-.61"];
})), BX, VX = o((() => {
	BX = ["M20 10a6 6 0 0 0-8.25-5.563A7.97 7.97 0 0 1 14 10a7.97 7.97 0 0 1-2.251 5.563A6 6 0 0 0 20 10M8.251 4.437a6 6 0 1 0 0 11.126A7.97 7.97 0 0 1 6 10c0-2.162.857-4.123 2.251-5.563m5.47.57q.14-.006.279-.007a5 5 0 0 1 0 10l-.278-.008-.222-.018.128-.196A8.97 8.97 0 0 0 15 10l-.006-.322a8.96 8.96 0 0 0-1.365-4.456l-.129-.197zM12 9.973a6 6 0 0 1-2 4.472 6 6 0 0 1-2-4.472A6 6 0 0 1 10 5.5q.23.206.438.435A5.98 5.98 0 0 1 12 9.972m-1.999-3-.085.114A5 5 0 0 0 9 9.972a5 5 0 0 0 .844 2.782l.156.22c.593-.79.943-1.74.994-2.748L11 9.972c0-1.01-.3-1.972-.844-2.781z"];
})), HX, UX = o((() => {
	HX = ["M16.024 7.96c.16-.19.34-.38.56-.55.21-.18.449-.36.709-.53.25-.18.5-.36.749-.56.25-.2.49-.41.73-.63.229-.22.439-.47.629-.74.18-.27.33-.56.44-.88S20 3.4 20 3c0-.32-.05-.65-.14-1s-.25-.68-.47-.97a2.5 2.5 0 0 0-.869-.74c-.36-.2-.809-.29-1.348-.29-.49 0-.93.1-1.299.29-.37.18-.69.44-.949.78-.26.33-.45.73-.58 1.2-.13.46-.2.96-.2 1.5h1.43c.01-.35.04-.67.09-.97s.14-.56.25-.78.259-.39.449-.52.43-.19.709-.19q.465 0 .75.18c.189.12.339.26.449.43s.18.36.22.56q.06.3.06.57c-.01.38-.1.72-.26 1.02-.15.3-.37.57-.63.83-.26.25-.54.49-.849.71-.31.22-.61.45-.889.68-.6.45-1.059.98-1.408 1.58-.35.61-.52 1.32-.53 2.13h5.984V8.57h-4.276c.06-.21.17-.42.33-.61M.224 6.63a1 1 0 1 1 1.563-1.248L5 9.4l3.213-4.017A1 1 0 1 1 9.776 6.63L6.28 11l3.495 4.369a1 1 0 1 1-1.563 1.249L5 12.6l-3.213 4.016A1 1 0 1 1 .224 15.37L3.72 11z"];
})), WX, GX = o((() => {
	WX = ["M16.02 10q-.015 0 0 0H16zM2 6h13.58l-2.29 2.29a1 1 0 0 0-.3.71 1.003 1.003 0 0 0 1.71.71l4-4c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-4-4a1.003 1.003 0 0 0-1.42 1.42L15.58 4H2c-.55 0-1 .45-1 1s.45 1 1 1m2 4h-.02zm14 4H4.42l2.29-2.29a1 1 0 0 0 .3-.71 1.003 1.003 0 0 0-1.71-.71l-4 4c-.18.18-.29.43-.29.71s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L4.42 16H18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), KX, qX = o((() => {
	KX = ["m9.71 5.3-4-4A1 1 0 0 0 5 1.01c-.28 0-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L4 4.42V18c0 .55.45 1 1 1s1-.45 1-1V4.42l2.29 2.29a1 1 0 0 0 .71.3 1.003 1.003 0 0 0 .71-1.71M10 3.98q0 .015 0 0V4zm0 12.04q0-.015 0 0V16zm9-3.03c-.28 0-.53.11-.71.29L16 15.58V2c0-.55-.45-1-1-1s-1 .45-1 1v13.58l-2.29-2.29a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4c.18-.18.29-.43.29-.71 0-.56-.45-1.01-1-1.01"];
})), JX, YX = o((() => {
	JX = ["M12.25 0C11.56 0 11 .56 11 1.25V11H7.25C6.56 11 6 11.56 6 12.25v1.5q0 .127-.004.25H19v-1.75c0-.69-.56-1.25-1.25-1.25H14V1.25C14 .56 13.44 0 12.75 0zM4.5 3a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1zm-2 3a.5.5 0 0 1 0-1h6a.5.5 0 0 1 0 1zm2 3a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1zM3 19c.55 0 2.457-1.163 2.905-4h13.032c-.168 1.895-.757 5-2.687 5H15v-2l-3 2h-2v-2l-3 2H3z"];
})), XX, ZX = o((() => {
	XX = ["m12.293 2.293 1.414 1.414-7.127 7.129a3.5 3.5 0 1 1-1.415-1.415zM16.5 9a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7m-13 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m13 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3"];
})), QX, $X = o((() => {
	QX = ["M10 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12"];
})), eZ, tZ = o((() => {
	eZ = ["M15 8.01h-3v-3c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v3H5c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h3v3c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-3h3c.55 0 1-.45 1-1v-2c0-.56-.45-1-1-1"];
})), nZ, rZ = o((() => {
	nZ = ["M15 10.01c0-.21-.08-.39-.18-.54l.02-.01-4-6-.02.01c-.18-.28-.47-.46-.82-.46s-.64.18-.82.45l-.01-.01-4 6 .02.01c-.11.16-.19.34-.19.55s.08.39.18.54l-.02.01 4 6 .02-.01c.18.27.47.46.82.46s.64-.19.82-.46l.02.01 4-6-.02-.01c.1-.16.18-.34.18-.54"];
})), iZ, aZ = o((() => {
	iZ = ["M16 5H4c-.5 0-1 .5-1 1v8c0 .5.5 1 1 1h12c.5 0 1-.5 1-1V6c0-.5-.5-1-1-1"];
})), oZ, sZ = o((() => {
	oZ = ["M15 4.01H5c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-10c0-.56-.45-1-1-1"];
})), cZ, lZ = o((() => {
	cZ = ["M16 5c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1 0 .16.05.31.11.44H4.1l5 10h.01c.17.33.5.56.89.56s.72-.23.89-.56h.01l5-10h-.01c.06-.13.11-.28.11-.44"];
})), uZ, dZ = o((() => {
	uZ = ["m15.89 14.56-4.99-10h-.01c-.17-.33-.5-.56-.89-.56s-.72.23-.89.56H9.1l-5 10h.01c-.06.13-.11.28-.11.44 0 .55.45 1 1 1h10c.55 0 1-.45 1-1 0-.16-.05-.31-.11-.44"];
})), fZ, pZ = o((() => {
	fZ = ["M15.146.854a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1-.708.708l-.646-.647L17.207 5.5l1.647 1.646a.5.5 0 0 1-.708.708l-.646-.647-1.146 1.146-7.5 7.5a.5.5 0 0 1-.708 0l-.646-.646-2.646 2.647a.5.5 0 0 1-.708 0l-.646-.647-2.646 2.647a.5.5 0 0 1-.708-.708L2.793 16.5l-.647-.646a.5.5 0 0 1 0-.708L4.793 12.5l-.647-.646a.5.5 0 0 1 0-.708l7.5-7.5L12.794 2.5l-.647-.646a.5.5 0 0 1 .708-.708L14.5 2.793 15.793 1.5zM12.707 4 16 7.293l.793-.793L13.5 3.207zm2.586 4L12 4.707 5.207 11.5 8.5 14.793 9.793 13.5l-1.647-1.646a.501.501 0 0 1 .708-.708l1.646 1.647 1.293-1.293-1.647-1.646a.5.5 0 1 1 .708-.708l1.646 1.647L13.793 9.5l-1.647-1.646a.5.5 0 0 1 .708-.708L14.5 8.793zM3.207 15.5 4.5 16.793 6.793 14.5 5.5 13.207zM16.5 2.207 15.207 3.5 16.5 4.793 17.793 3.5z"];
})), mZ, hZ = o((() => {
	mZ = ["M19 1H1c-.6 0-1 .5-1 1v16c0 .5.4 1 1 1h8a5 5 0 0 1-.9-2H8v-1c-.364 0-.706-.098-1-.269V17H2v-3h4c0-.362.095-.704.264-1H2v-3h5v2.166l1-1V10h4v1.166l.129.128c.164-.433.475-.795.871-1.025V10h5v1.999c.628.836 1 1.875 1 3.001.364 0 .706.098 1 .269V2c0-.5-.5-1-1-1M7 9H2V6h5zm5 0H8V6h4zm6 0h-5V6h5zm0 7.59V15c0-2.21-1.79-4-4-4-.55 0-1 .45-1 1s.45 1 1 1c1.1 0 2 .9 2 2v1.59l-.29-.3a1.003 1.003 0 0 0-1.42 1.42l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 19 16c-.28 0-.53.11-.71.3zm-9-2.18V16c0 2.21 1.79 4 4 4 .55 0 1-.45 1-1s-.45-1-1-1c-1.1 0-2-.9-2-2v-1.59l.29.3a1.003 1.003 0 0 0 1.42-1.42l-2-2A1 1 0 0 0 10 11c-.28 0-.53.11-.71.29l-2 2A1.003 1.003 0 0 0 8 15c.28 0 .53-.11.71-.3z"];
})), gZ, _Z = o((() => {
	gZ = ["M2 4a2 2 0 0 1 2-2h4.588a2 2 0 0 1 1.414.586l7.41 7.41a2 2 0 0 1 0 2.828l-4.588 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 2 8.588zm3.489-.006a1.495 1.495 0 1 0 0 2.99 1.495 1.495 0 0 0 0-2.99"];
})), vZ, yZ = o((() => {
	vZ = ["M15 1a1 1 0 0 1 1 1v2h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V6h-2a1 1 0 1 1 0-2h2V2a1 1 0 0 1 1-1m-4.19 2.393A2 2 0 0 0 12 7h1v1a2 2 0 0 0 3.607 1.19l.805.805a2 2 0 0 1 0 2.829l-4.588 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 2 8.588V4a2 2 0 0 1 2-2h4.588a2 2 0 0 1 1.414.586zM3.993 5.489a1.495 1.495 0 1 0 2.99 0 1.495 1.495 0 0 0-2.99 0"];
})), bZ, xZ = o((() => {
	bZ = ["M14.293 1.293c.39-.39 1.03-.39 1.42 0l2.98 2.966c.41.41.41 1.072 0 1.482l-2.98 2.966c-.39.39-1.03.39-1.42 0a1 1 0 0 1 0-1.413L16.592 5l-2.3-2.294a1 1 0 0 1 0-1.413m-2.579 0 2.98 2.966c.41.41.41 1.072 0 1.482l-2.98 2.966c-.39.39-1.03.39-1.42 0a1 1 0 0 1 0-1.413L12.593 5l-2.3-2.294a1 1 0 0 1 0-1.413c.39-.39 1.03-.39 1.42 0m4.912 7.917.786.785a2 2 0 0 1 0 2.829l-4.587 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 2 8.588V4a2 2 0 0 1 2-2h4.588A2 2 0 0 1 9 2.043c.011.497.206.99.585 1.37h.001L11.176 5l-1.59 1.586-.001.002a2 2 0 0 0 0 2.825c.78.782 2.053.782 2.834.002l.001-.002.709-.705a2.007 2.007 0 0 0 3.29.707l.001-.002zM3.994 5.488a1.495 1.495 0 1 0 2.99 0 1.495 1.495 0 0 0-2.99 0"];
})), SZ, CZ = o((() => {
	SZ = ["M13.29 7.29a1.003 1.003 0 0 1 1.42 1.42l-.3.29H16c.55 0 1-.45 1-1s.45-1 1-1 1 .45 1 1c0 1.66-1.34 3-3 3h-1.59l.3.29a1.003 1.003 0 0 1-1.42 1.42l-2-2A1 1 0 0 1 11 10c0-.28.11-.53.29-.71zm3.42-.58a1.003 1.003 0 0 1-1.42-1.42l.3-.29H14c-.55 0-1 .45-1 1s-.45 1-1 1-1-.45-1-1c0-1.66 1.34-3 3-3h1.59l-.3-.29a1.003 1.003 0 0 1 1.42-1.42l2 2c.18.18.29.43.29.71s-.11.53-.29.71zm-5.816-3.233A4 4 0 0 0 10 6c0 .854.539 1.585 1.294 1.871l-.711.712A2 2 0 0 0 10 10c0 .548.218 1.052.583 1.417l2 2A2.003 2.003 0 0 0 16 12a4 4 0 0 0 1.997-.532c-.015.493-.21.98-.585 1.356l-4.588 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 2 8.588V4a2 2 0 0 1 2-2h4.588a2 2 0 0 1 1.414.586zm-6.9 2.012a1.495 1.495 0 1 0 2.99 0 1.495 1.495 0 0 0-2.99 0"];
})), wZ, TZ = o((() => {
	wZ = ["M15 2a1 1 0 0 1 1-1c1.66 0 3 1.34 3 3s-1.34 3-3 3h-1.59l.3.29a1.003 1.003 0 0 1-1.42 1.42l-2-2A1 1 0 0 1 11 6c0-.28.11-.53.29-.71l2-2a1.003 1.003 0 0 1 1.42 1.42l-.3.29H16c.55 0 1-.45 1-1s-.45-1-1-1a1 1 0 0 1-1-1m.932 6.516 1.48 1.48a2 2 0 0 1 0 2.828l-4.588 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 2 8.588V4a2 2 0 0 1 2-2h4.588a2 2 0 0 1 1.414.586l1.289 1.289-.708.708A2 2 0 0 0 10 6c0 .548.218 1.052.583 1.417l2 2a2.004 2.004 0 0 0 3.35-.9M3.994 5.49a1.495 1.495 0 1 0 2.99 0 1.495 1.495 0 0 0-2.99 0"];
})), EZ, DZ = o((() => {
	EZ = ["M3 3a2 2 0 0 1 2-2h4.588a2 2 0 0 1 1.414.586l7.41 7.41a2 2 0 0 1 0 2.828l-4.588 4.588a2 2 0 0 1-2.829 0l-7.41-7.41A2 2 0 0 1 3 7.588zm3.489-.006a1.495 1.495 0 1 0 0 2.99 1.495 1.495 0 0 0 0-2.99M2 4.689l-.732 1.258c-.265.457-.337 1-.2 1.51l2.717 10.068a2.005 2.005 0 0 0 2.453 1.407l4.785-1.274a3 3 0 0 1-.735-.54L2.878 9.71A3 3 0 0 1 2 7.588z"];
})), OZ, kZ = o((() => {
	OZ = ["M5 7c.28 0 .53-.11.71-.29l5-5A1.003 1.003 0 0 0 9.29.29l-5 5A1.003 1.003 0 0 0 5 7m6 6a1.003 1.003 0 0 0 1.71.71l5-5a1.003 1.003 0 0 0-1.42-1.42l-5 5c-.18.18-.29.43-.29.71m8 5h-1c0-.55-.45-1-1-1h-7c-.55 0-1 .45-1 1H8c-.55 0-1 .45-1 1s.45 1 1 1h11c.55 0 1-.45 1-1s-.45-1-1-1m-9-6 6-6-1.29-1.29a1.003 1.003 0 0 0-1.42-1.42L12 2 6 8l1.29 1.29-7 7a1.003 1.003 0 0 0 1.42 1.42l7-7z"];
})), AZ, jZ = o((() => {
	AZ = ["M3.956 4.47A1 1 0 0 1 4.804 4h6.392a1 1 0 0 1 .848.47L13 6h5a1 1 0 1 1 0 2h-5v1h4a3 3 0 0 1 0 6H3a3 3 0 0 1 0-6V6.287a1 1 0 0 1 .152-.53zM3 11a1 1 0 0 0 0 2h14a1 1 0 0 0 0-2z"];
})), MZ, NZ = o((() => {
	MZ = ["M9 5a1 1 0 0 1 2 0v3a1 1 0 0 1-2 0zm3 4h3a1 1 0 1 1 0 2h-3a1 1 0 0 1 0-2m-8 1a1 1 0 0 1 1-1h3a1 1 0 0 1 0 2H5a1 1 0 0 1-1-1m6 1a1 1 0 0 1 1 1v3a1 1 0 0 1-2 0v-3a1 1 0 0 1 1-1m0 9C4.477 20 0 15.523 0 10S4.477 0 10 0s10 4.477 10 10-4.477 10-10 10m0-2a8 8 0 1 0 0-16.001A8 8 0 0 0 10 18"];
})), PZ, FZ = o((() => {
	PZ = ["M19 9h-.33l.33 1v.5c0 .15-.03.3-.07.44h.01L17 17.23v.27c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5V17H6v.5c0 .83-.67 1.5-1.5 1.5S3 18.33 3 17.5v-.27l-1.93-6.28h.01c-.05-.15-.08-.3-.08-.45V10s.02-.06.05-.16c.06-.17.16-.47.28-.84H1c-.55 0-1-.45-1-1s.45-1 1-1h1l1-3h-.01v-.01c.25-.64 1-1.31 1.67-1.5 0 0 .78-.21 2.33-.36V1c0-.55.45-1 1-1h4c.55 0 1 .45 1 1v1.13c1.55.14 2.33.36 2.33.36.67.19 1.42.86 1.67 1.5V4H17l1 3h1c.55 0 1 .45 1 1s-.45 1-1 1M3 11.5c0 .83.67 1.5 1.5 1.5S6 12.33 6 11.5 5.33 10 4.5 10 3 10.67 3 11.5M16 7l-1-3H5L4 7v1h12zm-.5 3c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5"];
})), IZ, LZ = o((() => {
	IZ = ["M17.691 15.328c-.456-1.056-2.68-1.752-4.154-2.408-1.48-.656-1.272-1.048-1.328-1.592-.008-.072-.008-.152-.016-.232.504-.448.92-1.064 1.192-1.776 0 0 .016-.04.016-.048q.082-.228.152-.48c.337-.072.537-.44.609-.784.08-.136.232-.48.2-.864-.048-.496-.248-.728-.472-.824v-.088c0-.632-.056-1.544-.177-2.144a3.64 3.64 0 0 0-1.393-2.352C11.69 1.256 10.8 1 10.009 1s-1.68.256-2.313.736a3.64 3.64 0 0 0-1.393 2.352c-.112.6-.176 1.512-.176 2.144v.08c-.232.088-.44.32-.488.832-.032.384.12.728.2.864.08.352.28.728.633.784.04.168.096.328.152.48 0 .008.008.024.008.032l.008.016c.272.728.696 1.352 1.216 1.8 0 .072-.008.144-.016.208-.056.544.104.936-1.376 1.592-1.481.656-3.698 1.352-4.154 2.408S2 19 2 19h16s.147-2.616-.309-3.672M1.34 15.15c-.148.302-.34.693-.34 3.85H0v-4c0-1.3.851-2.103 1.905-2.57 1.149-.51 1.168-.837 1.192-1.236l.012-.157q.012-.086.014-.182c-.455-.392-.826-.938-1.064-1.575l-.007-.014q0-.006-.004-.014l-.001-.005-.002-.009a4 4 0 0 1-.133-.42c-.308-.049-.484-.378-.554-.686a1.37 1.37 0 0 1-.175-.756c.042-.448.224-.651.428-.728v-.07c0-.553.056-1.351.154-1.876a3.2 3.2 0 0 1 1.218-2.058C3.536 2.224 4.313 2 5.007 2c.327 0 .673.05 1.005.147a4.5 4.5 0 0 0-.505 1.121 4.4 4.4 0 0 0-.139.612 14 14 0 0 0-.184 1.94c-.286.305-.45.729-.497 1.217v.009c-.045.541.12 1.007.254 1.277.064.227.167.479.33.707.102.141.238.287.41.406l.026.079c.017.056.034.11.064.17a5.5 5.5 0 0 0 1.128 1.818c-.01.151-.03.186-.159.277-.13.092-.343.214-.686.366-.24.106-.538.228-.858.36-.545.223-1.157.474-1.664.721a7.4 7.4 0 0 0-1.222.725c-.358.271-.721.63-.924 1.098zm12.606-3.004h.002c.282.126.59.253.924.39h.003l.27.112c.43.177.888.37 1.32.579a7.5 7.5 0 0 1 1.223.724c.359.271.75.73.953 1.2C18.792 15.5 19 16 19 19h1v-4c0-1.274-.875-2.111-1.905-2.57-1.123-.498-1.136-.822-1.15-1.209a3 3 0 0 0-.012-.184l-.007-.088v-.013l-.007-.102a4 4 0 0 0 1.043-1.554s.014-.035.014-.042c.05-.133.091-.273.133-.42.294-.063.47-.385.532-.686.07-.119.204-.42.176-.756-.043-.434-.218-.637-.414-.721v-.077c0-.553-.049-1.351-.154-1.876a3.2 3.2 0 0 0-1.219-2.058C16.478 2.224 15.7 2 15.008 2c-.327 0-.672.05-1.004.146.219.35.39.727.506 1.122.056.187.106.392.138.606.112.574.17 1.346.186 1.97.273.301.433.713.48 1.19v.012c.045.537-.118 1-.251 1.271a2.2 2.2 0 0 1-.32.696c-.097.14-.228.285-.395.406l-.01.03a5.65 5.65 0 0 1-1.19 2.025v.04l.001.018q.001.077.01.153c.033.039.195.198.788.461"];
})), RZ, zZ = o((() => {
	RZ = ["M11 0a2 2 0 0 0-2 2v10.535a4 4 0 1 0 4 0V2a2 2 0 0 0-2-2M3 2.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5M3.5 8a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zM5 5.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m.5 5.5a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1z"];
})), BZ, VZ = o((() => {
	BZ = ["M16 17c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1s1-.45 1-1-.45-1-1-1c-.77 0-1.47.3-2 .78-.53-.48-1.23-.78-2-.78-.55 0-1 .45-1 1s.45 1 1 1 1 .45 1 1v12c0 .55-.45 1-1 1s-1 .45-1 1 .45 1 1 1c.77 0 1.47-.3 2-.78.53.48 1.23.78 2 .78.55 0 1-.45 1-1s-.45-1-1-1m-4-4H2V7h10V5H1c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h11zm7-8h-3v2h2v6h-2v2h3c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1"];
})), HZ, UZ = o((() => {
	HZ = ["M19 1H1c-.6 0-1 .5-1 1v16c0 .5.4 1 1 1h18c.5 0 1-.5 1-1V2c0-.5-.5-1-1-1M7 17H2v-3h5zm0-4H2v-3h5zm0-4H2V6h5zm11 8H8v-3h10zm0-4H8v-3h10zm0-4H8V6h10z"];
})), WZ, GZ = o((() => {
	WZ = ["M15 1a1 1 0 0 1 2 0v2h2a1 1 0 0 1 0 2h-2v2a1 1 0 0 1-2 0V5h-2a1 1 0 0 1 0-2h2zm4 6v11a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2c0-.5.4-1 1-1h12a3 3 0 0 0-2.236 5H8v3h5.764a2.99 2.99 0 0 0 3.314.8l.09-.036A3 3 0 0 0 19 7m-3 3H8v3h9v-3zM7 9V6H2v3zm-5 1v3h5v-3zm0 4v3h5v-3zm15 0H8v3h9z"];
})), KZ, qZ = o((() => {
	KZ = ["M5.3 13.3c-.2.2-.3.4-.3.7 0 .6.4 1 1 1 .3 0 .5-.1.7-.3l3-3c.2-.2.3-.4.3-.7s-.1-.5-.3-.7l-3-3C6.5 7.1 6.3 7 6 7c-.6 0-1 .4-1 1 0 .3.1.5.3.7L6.6 10H1c-.6 0-1 .4-1 1s.4 1 1 1h5.6zM19 1H3c-.5 0-1 .5-1 1v6h1c0-1.7 1.3-3 3-3 .8 0 1.6.3 2.1.9l.1.1H9v.8l1 1V6h8v3h-6.8c.3.3.5.6.6 1H18v3h-6.8l-.1.1-.9.9H18v3h-8v-2.8l-1 1V17H4v-.8c-.6-.5-1-1.3-1-2.2H2v4c0 .5.5 1 1 1h16c.6 0 1-.5 1-1V2c0-.5-.5-1-1-1"];
})), JZ, YZ = o((() => {
	JZ = ["M14.25 1H19c.5 0 1 .5 1 1v16c0 .5-.5 1-1 1h-7.221l.278-2H18v-3h-5.527l.14-1H18v-3h-4.971l.139-1H18V6h-4.416l.637-4.587q.03-.209.03-.413m-6.03 0-.694 5H2v3h5.11l-.139 1H2v3h4.555l-.14 1H2v3h3.999l-.22 1.587q-.03.209-.03.413H1c-.6 0-1-.5-1-1V2c0-.5.4-1 1-1zM10.26.862a1 1 0 0 1 1.98.276l-2.5 18a1 1 0 0 1-1.98-.276z"];
})), XZ, ZZ = o((() => {
	XZ = ["m17.333 10 1.435-1.722a1 1 0 0 0 .232-.64V4.85l1-.9V18c0 .5-.5 1-1 1H1c-.6 0-1-.5-1-1V2c0-.5.4-1 1-1h6.722L12 4.85V6H8v3h4v1H8v3h10v-3zM7 17v-3H2v3zm0-4v-3H2v3zm0-4V6H2v3zm11 8v-3H8v3zm1.35-17a.642.642 0 0 1 .46 1.1l-3.03 3.03v2.95c0 .18-.07.34-.19.46l-1.28 1.29c-.11.1-.27.17-.45.17-.35 0-.64-.29-.64-.64V4.13L11.19 1.1a.642.642 0 0 1 .45-1.1z"];
})), QZ, $Z = o((() => {
	QZ = ["M19 1H1c-.6 0-1 .5-1 1v16c0 .5.4 1 1 1h18c.5 0 1-.5 1-1V2c0-.5-.5-1-1-1m-1 16H2v-3h16zm0-4H2v-3h16zm0-4H2V6h16z"];
})), eQ, tQ = o((() => {
	eQ = ["M16 0a1 1 0 0 0-1 1v2h-2a1 1 0 0 0 0 2h2v2a1 1 0 0 0 2 0V5h2a1 1 0 0 0 0-2h-2V1a1 1 0 0 0-1-1m1.168 9.764A3 3 0 0 0 19 7v11a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2c0-.5.4-1 1-1h12a3 3 0 0 0-2.236 5H2v3h11.764c.55.614 1.348 1 2.236 1H2v3h15v-3h-1a3 3 0 0 0 1.168-.236M2 14v3h15v-3z"];
})), nQ, rQ = o((() => {
	nQ = ["M3 8a1 1 0 0 1 1-1h5a1 1 0 0 1 0 2H6.414l5.293 5.293a1 1 0 1 1-1.414 1.414L5 10.414V13a1 1 0 0 1-2 0zm17 10a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2c0-.5.4-1 1-1h18a1 1 0 0 1 1 1zm-2-1V6H2v11z"];
})), iQ, aQ = o((() => {
	iQ = ["M15 1a1 1 0 1 1 2 0v2h2a1 1 0 1 1 0 2h-2v2a1 1 0 1 1-2 0V5h-2a1 1 0 1 1 0-2h2zM1 1h12a3 3 0 0 0-2.236 5H2v11h15V9.83A3 3 0 0 0 19 7v11a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2c0-.5.4-1 1-1m2 7a1 1 0 0 1 1-1h5a1 1 0 0 1 0 2H6.414l5.293 5.293a1 1 0 1 1-1.414 1.414L5 10.414V13a1 1 0 0 1-2 0z"];
})), oQ, sQ = o((() => {
	oQ = ["M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.856 7.71q.097-.086.19-.156c.278-.209.595-.383.896-.53.358-.174.81-.358 1.193-.515.206-.084.393-.16.534-.223a4 4 0 0 0 .203-.095 4 4 0 0 1-.305-.45C8.382 13.911 8.19 14 8 14c-.67 0-1.36-1.1-1.73-3h1.252c.047-.296.153-.571.323-.797l.01-.203H6.12C6.05 9.39 6 8.73 6 8s.05-1.39.12-2h3.76l.037.344a3.8 3.8 0 0 1 .979-.295L10.89 6h2.76q.04.116.076.233l.118-.04A3.6 3.6 0 0 1 14.998 6c.247 0 .51.028.772.086A8 8 0 0 0 8 0m5.17 5h-2.44c-.21-1.11-.51-2.03-.91-2.69 1.43.46 2.61 1.43 3.35 2.69M8 2c.67 0 1.36 1.1 1.73 3H6.27C6.64 3.1 7.33 2 8 2m-1.82.31c-.4.66-.71 1.58-.91 2.69H2.83a6.03 6.03 0 0 1 3.35-2.69M2 8c0-.7.13-1.37.35-2h2.76C5.04 6.62 5 7.28 5 8s.04 1.38.11 2H2.35C2.13 9.37 2 8.7 2 8m.83 3h2.44c.21 1.11.51 2.03.91 2.69A6.03 6.03 0 0 1 2.83 11m11.087 4.209c.21.094.444.19.685.288.912.374 1.927.789 2.188 1.355.31.722.186 1.148.186 1.148H6.026s-.13-.426.186-1.148c.256-.584 1.305-1.011 2.234-1.39.22-.088.432-.175.626-.26.909-.4.923-.662.94-.978l.008-.115.003-.072q.004-.037.004-.073a3.1 3.1 0 0 1-.839-1.237l-.007-.007-.003-.01-.003-.01a2 2 0 0 1-.11-.337c-.234-.042-.372-.296-.426-.537a1.05 1.05 0 0 1-.138-.598c.034-.35.179-.509.337-.57v-.056c0-.44.034-1.065.117-1.478q.021-.177.075-.343a2.5 2.5 0 0 1 .887-1.28c.426-.33 1.038-.501 1.58-.501.544 0 1.155.172 1.588.502a2.5 2.5 0 0 1 .963 1.622c.075.413.117 1.045.117 1.478v.062c.15.062.288.22.323.564.02.268-.083.502-.138.598-.048.234-.185.488-.42.537a3 3 0 0 1-.116.364 3.1 3.1 0 0 1-.818 1.224q-.002.084.007.158.006.072.007.14c.011.311.02.57.907.96m1.059-.639c-.24-.098-.455-.186-.65-.274l-.007-.003a4 4 0 0 1-.194-.091c.224-.288.41-.609.554-.946l.001-.002.013-.033q.028-.065.052-.13l.011-.027.016-.04c.105-.092.19-.19.256-.284a1.9 1.9 0 0 0 .265-.562c.105-.227.225-.593.192-1.027l-.001-.011-.002-.011a1.86 1.86 0 0 0-.325-.91 10 10 0 0 0-.12-1.246 3 3 0 0 0-.106-.474l-.001-.007a3.54 3.54 0 0 0-.763-1.353c.27-.092.56-.139.83-.139.495 0 1.05.156 1.444.456a2.27 2.27 0 0 1 .875 1.475c.069.375.106.95.106 1.344v.056c.138.056.263.2.294.513a1 1 0 0 1-.125.543c-.044.213-.169.444-.381.488-.025.1-.056.206-.094.3a2.8 2.8 0 0 1-.756 1.144q-.002.076.006.144.006.065.007.127c.01.283.018.518.824.873.192.086.404.172.623.262.83.34 1.752.717 1.99 1.231.28.657.168 1.044.168 1.044h-2.081a4 4 0 0 0-.188-.542l-.005-.013-.006-.012c-.183-.397-.491-.681-.76-.88a5.6 5.6 0 0 0-.896-.522 17 17 0 0 0-.916-.4z"];
})), cQ, lQ = o((() => {
	cQ = ["M18.55 6.56q-.465-.015-1.02-.06c.03 0 .06-.01.09-.01.88-.12 1.68-.63 1.76-1.37.08-.75-.58-1.25-1.46-1.33-.32-.03-.65-.05-.99-.08.59-.19 1.05-.54 1.09-1.2.05-.75-.99-1.32-1.87-1.41-.34-.03-.64-.05-.91-.07h-.11c-.28-.02-.54-.02-.77-.02-3.92-.08-7.29.6-9.36 1.93v7.72c2.67 1.66 5.95 4.61 5.26 7.08-.21.76.39 1.35 1.23 1.26 1.01-.11 1.71-1.18 1.75-2.28.05-1.29-.19-2.59-.62-3.74-.05-.32.01-.65.47-.68.61-.04 1.39-.08 1.99-.1.32 0 .64-.01.94-.03h.01c.52-.03 1-.07 1.42-.12.88-.11 1.69-.6 1.79-1.35s-.55-1.25-1.44-1.35c-.07-.01-.13-.02-.2-.02.21-.02.42-.04.61-.06.88-.11 1.69-.6 1.79-1.35.09-.75-.56-1.31-1.45-1.36M3 3H0v8h3c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), uQ, dQ = o((() => {
	uQ = ["M3 9H0v8h3c.55 0 1-.45 1-1v-6c0-.55-.45-1-1-1m16.99 3.09c-.1-.75-.91-1.24-1.79-1.35-.19-.02-.4-.05-.61-.06.07-.01.14-.01.2-.02.88-.1 1.53-.61 1.44-1.35-.1-.74-.91-1.24-1.79-1.35-.42-.05-.9-.09-1.42-.12h-.01l-.94-.03c-.6-.02-1.39-.05-1.99-.1-.45-.03-.51-.36-.47-.68.43-1.15.67-2.45.62-3.74-.04-1.11-.74-2.17-1.75-2.28-.84-.09-1.45.5-1.23 1.26.7 2.47-2.58 5.43-5.25 7.08v7.72c2.08 1.33 5.44 2.01 9.35 1.93.24 0 .49-.01.77-.02h.11c.27-.02.57-.04.91-.07.88-.08 1.92-.66 1.87-1.41-.04-.65-.5-1.01-1.09-1.2.34-.03.67-.05.99-.08.89-.08 1.55-.58 1.46-1.33-.08-.75-.88-1.25-1.76-1.37-.03 0-.06-.01-.09-.01q.555-.03 1.02-.06c.91-.05 1.55-.61 1.45-1.36"];
})), fQ, pQ = o((() => {
	fQ = ["M17 4c-.28 0-.53.11-.71.29L7 13.59 3.71 10.3A.97.97 0 0 0 3 10a1.003 1.003 0 0 0-.71 1.71l4 4c.18.18.43.29.71.29s.53-.11.71-.29l10-10A1.003 1.003 0 0 0 17 4"];
})), mQ, hQ = o((() => {
	mQ = ["M10 20C4.48 20 0 15.52 0 10S4.48 0 10 0s10 4.48 10 10-4.48 10-10 10m5-14c-.28 0-.53.11-.71.29L8 12.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l7-7A1.003 1.003 0 0 0 15 6"];
})), gQ, _Q = o((() => {
	gQ = ["M11 9.59V4c0-.55-.45-1-1-1s-1 .45-1 1v6c0 .28.11.53.29.71l3 3a1.003 1.003 0 0 0 1.42-1.42zM10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8"];
})), vQ, yQ = o((() => {
	vQ = ["M19 16H2V3c0-.55-.45-1-1-1s-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1m0-13.41-7.07 7.07-4.3-3.44-.01.01A1 1 0 0 0 7 6c-.24 0-.46.1-.63.24l-.01-.01L3 9.03V15h16z"];
})), bQ, xQ = o((() => {
	bQ = ["M19 17H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1M9 16h2c.55 0 1-.45 1-1V2c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v13c0 .55.45 1 1 1m6 0h2c.55 0 1-.45 1-1V6c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1M3 16h2c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1"];
})), SQ, CQ = o((() => {
	SQ = ["M5 5c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1s-1 .5-1 1v2c0 .6.4 1 1 1m10 0c.6 0 1-.4 1-1V2c0-.5-.4-1-1-1s-1 .5-1 1v2c0 .6.4 1 1 1m-9 9H4v2h2zM17 3v1c0 1.1-.9 2-2 2s-2-.9-2-2V3H7v1c0 1.1-.9 2-2 2s-2-.9-2-2V3H2c-.5 0-1 .5-1 1v14c0 .5.5 1 1 1h16c.5 0 1-.5 1-1V4c0-.5-.5-1-1-1zM7 17H3v-4h4zm0-5H3V8h4zm5 5H8v-4h4zm0-5H8V8h4zm5 5h-4v-4h4zm0-5h-4V8h4zm-6 2H9v2h2zm5-5h-2v2h2z"];
})), wQ, TQ = o((() => {
	wQ = ["M19 16H2v-1.59l5-5 3.29 3.29c.18.19.43.3.71.3s.53-.11.71-.29l7-7a1.003 1.003 0 0 0-1.42-1.42L11 10.59l-3.29-3.3C7.53 7.11 7.28 7 7 7s-.53.11-.71.29L2 11.59V3c0-.55-.45-1-1-1s-1 .45-1 1v14a1 1 0 0 0 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), EQ, DQ = o((() => {
	EQ = ["M9.86 2S3.98 9.18 3.98 12.17C3.99 15.4 6.78 18 9.96 18c3.18-.01 6.04-2.63 6.03-5.86C15.99 9.05 9.86 2 9.86 2"];
})), OQ, kQ = o((() => {
	OQ = ["M6.97 19c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-2h-6zm-3-15 3 4v8h6V8l3-4zm5 5c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1s-1-.45-1-1zm6-9h-10c-.55 0-1 .45-1 1v2h12V1c0-.55-.45-1-1-1"];
})), AQ, jQ = o((() => {
	AQ = ["M4.5 11a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9m11.499 1a4 4 0 1 1 0 8 4 4 0 0 1 0-8m-11.5 1.571a1.928 1.928 0 1 0 0 3.857 1.928 1.928 0 0 0 0-3.857M16 14.667a1.333 1.333 0 1 0 0 2.666 1.333 1.333 0 0 0 0-2.666M5.999 0C7.46 0 8.527.668 9 2l.851 4.256c1.433.096 2.82.217 4.147.362V2h2L16 6.862q1.444.195 2.767.435c.779.141 1.232.614 1.232 1.284L20 13a5 5 0 0 0-4-1.997A5 5 0 0 0 11.099 15h-1.12a5.5 5.5 0 0 0-5.478-4.994 5.48 5.48 0 0 0-3.377 1.157H.004v-1.18L0 7.327c-.002-.597.37-1.18.999-1.302V1a1 1 0 0 1 1-1zm1 2H3v4h.75c1.386.027 2.749.073 4.079.139z"];
})), MQ, NQ = o((() => {
	MQ = ["M16 18h-2l2 2H4l.12-.12L6 18H4c-1.1 0-2-.9-2-2V2c0-1.1 3.58-2 8-2s8 .9 8 2v14c0 1.1-.9 2-2 2M5.5 15c.83 0 1.5-.67 1.5-1.5S6.33 12 5.5 12 4 12.67 4 13.5 4.67 15 5.5 15M9 3H4v6h5zm7 0h-5v6h5zm-1.5 9c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5"];
})), PQ, FQ = o((() => {
	PQ = ["m19.89 18.56-4.99-10h-.01c-.17-.33-.5-.56-.89-.56s-.72.23-.89.56h-.01l-1.73 3.46-2.8-2.3 1.99-1.64C11.44 7.34 12 6.23 12 5V4h1c.55 0 1-.45 1-1s-.45-1-1-1H8V1c0-.55-.45-1-1-1S6 .45 6 1v1H1c-.55 0-1 .45-1 1s.45 1 1 1h9v1c0 .62-.28 1.18-.73 1.54L7 8.42 4.73 6.54C4.28 6.18 4 5.62 4 5H2c0 1.23.56 2.34 1.44 3.07l1.99 1.64-3.06 2.52.01.01c-.23.18-.38.45-.38.76 0 .55.45 1 1 1 .24 0 .45-.1.63-.24l.01.01L7 11l3.36 2.77.01-.01c.02.02.05.03.08.05.01 0 .01.01.02.02l-2.36 4.73h.01c-.07.13-.12.28-.12.44 0 .55.45 1 1 1 .39 0 .72-.23.89-.56h.01L11.12 17h5.76l1.22 2.45h.01c.17.32.5.55.89.55.55 0 1-.45 1-1 0-.16-.05-.31-.11-.44M12.12 15 14 11.24 15.88 15z"];
})), IQ, LQ = o((() => {
	IQ = ["M17 1h-5c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1H3c-.55 0-1 .45-1 1v1h16V2c0-.55-.45-1-1-1m.5 3h-15c-.28 0-.5.22-.5.5s.22.5.5.5H3v14c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V5h.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5M7 16c0 .55-.45 1-1 1s-1-.45-1-1V8c0-.55.45-1 1-1s1 .45 1 1zm4 0c0 .55-.45 1-1 1s-1-.45-1-1V8c0-.55.45-1 1-1s1 .45 1 1zm4 0c0 .55-.45 1-1 1s-1-.45-1-1V8c0-.55.45-1 1-1s1 .45 1 1z"];
})), RQ, zQ = o((() => {
	RQ = ["M11 15.542V20H9v-4.458L2 17l4.5-5.625L4 12l3.655-5.483L6 7l4-7 4 7-1.655-.483L16 12l-2.5-.625L18 17z"];
})), BQ, VQ = o((() => {
	BQ = ["M19 10c-.55 0-1 .45-1 1v1.37l-6.25-7.03-.01.01A.97.97 0 0 0 11 5c-.23 0-.42.09-.59.21l-.01-.01-3.43 2.58-5.42-3.61-.01.01A.97.97 0 0 0 1 4c-.55 0-1 .45-1 1 0 .35.19.64.46.82l-.01.01 6 4 .01-.02c.15.11.33.19.54.19.23 0 .42-.09.59-.21l.01.01 3.26-2.45L16.77 14H15c-.55 0-1 .45-1 1s.45 1 1 1h4c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1"];
})), HQ, UQ = o((() => {
	HQ = ["M19 4h-4c-.55 0-1 .45-1 1s.45 1 1 1h1.77l-5.91 6.65L7.6 10.2l-.01.01C7.42 10.09 7.23 10 7 10c-.21 0-.39.08-.54.18l-.01-.02-6 4 .01.02c-.27.18-.46.47-.46.82 0 .55.45 1 1 1 .21 0 .39-.08.54-.18l.01.02 5.41-3.61 3.43 2.58.01-.01c.18.11.37.2.6.2.3 0 .56-.14.74-.34l.01.01L18 7.63V9c0 .55.45 1 1 1s1-.45 1-1V5c0-.55-.45-1-1-1"];
})), WQ, GQ = o((() => {
	WQ = ["M5 1a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v2h4a1 1 0 0 1 1 1v2a5 5 0 0 1-5 5h-.416A5.01 5.01 0 0 1 11 13.9V18h3a1 1 0 0 1 0 2H6a1 1 0 0 1 0-2h3v-4.1A5.01 5.01 0 0 1 5.416 11H5a5 5 0 0 1-5-5V4a1 1 0 0 1 1-1h4zm0 4H2v1a3 3 0 0 0 3 3zm10 4a3 3 0 0 0 3-3V5h-3z"];
})), KQ, qQ = o((() => {
	KQ = ["M16 0a1 1 0 0 1 1 1v11a1 1 0 0 1 1 1v3h.5a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H17v1a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H6v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-1H1.5a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5H2v-3a1 1 0 0 1 1-1V1a1 1 0 1 1 2 0v3a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2V1a1 1 0 0 1 1-1m-4 10H8a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1m-7 4H4a1 1 0 0 0 0 2h1a1 1 0 0 0 0-2m11 0h-1a1 1 0 0 0 0 2h1a1 1 0 0 0 0-2m-4.5 0a.5.5 0 1 1 0 1h-3l-.09-.008A.5.5 0 0 1 8.5 14Zm0-1.5a.5.5 0 1 1 0 1h-3l-.09-.008a.5.5 0 0 1 .09-.992Zm0-1.5a.5.5 0 1 1 0 1h-3l-.09-.008A.5.5 0 0 1 8.5 11ZM14 5H6v3h8z"];
})), JQ, YQ = o((() => {
	JQ = ["M5 0H1C.45 0 0 .45 0 1v18c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m14.71 9.29-3-3A1.003 1.003 0 0 0 15 7v6a1.003 1.003 0 0 0 1.71.71l3-3c.18-.18.29-.43.29-.71s-.11-.53-.29-.71M12 0H8c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h4c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), XQ, ZQ = o((() => {
	XQ = ["M16.434 0a1 1 0 0 1 .857.486L20 5v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V5L2.709.486A1 1 0 0 1 3.566 0zM10 8c-.28 0-.53.11-.71.29l-3 3-.084.096A1.003 1.003 0 0 0 7.71 12.71L9 11.41v4.58l.007.116c.058.496.482.884.993.884.55 0 1-.45 1-1v-4.58l1.29 1.29.081.073A1 1 0 0 0 13 13a1.003 1.003 0 0 0 .71-1.71l-3-3-.096-.084A1 1 0 0 0 10 8m6-6H4L2 5.002h16z"];
})), QQ, $Q = o((() => {
	QQ = ["M10 17c3.3 0 6-2.7 6-6V3.5c0-.8-.7-1.5-1.5-1.5S13 2.7 13 3.5V11c0 1.7-1.3 3-3 3s-3-1.3-3-3V3.5C7 2.7 6.3 2 5.5 2S4 2.7 4 3.5V11c0 3.3 2.7 6 6 6m6.5 2h-13c-.3 0-.5.2-.5.5s.2.5.5.5h13c.3 0 .5-.2.5-.5s-.2-.5-.5-.5"];
})), e$, t$ = o((() => {
	e$ = ["M5 14c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m9-9H3.41L5.7 2.71c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71l-4 4C.11 5.47 0 5.72 0 6s.11.53.29.71l4 4a1.003 1.003 0 0 0 1.42-1.42L3.41 7H14c2.21 0 4 1.79 4 4s-1.79 4-4 4H9v2h5c3.31 0 6-2.69 6-6s-2.69-6-6-6"];
})), n$, r$ = o((() => {
	n$ = ["M4.5 6C2.01 6 0 8.01 0 10.5S2.01 15 4.5 15 9 12.99 9 10.5 6.99 6 4.5 6m11 0C13.01 6 11 8.01 11 10.5s2.01 4.5 4.5 4.5 4.5-2.01 4.5-4.5S17.99 6 15.5 6"];
})), i$, a$ = o((() => {
	i$ = ["M13 11.988v-4H4v-1l1-3h6V2.003a36 36 0 0 0-1-.015c-3.593 0-5.332.488-5.332.488-.67.188-1.424.864-1.674 1.503l-.004.009H3l-1 3H1a1 1 0 1 0 0 2h.333l-.28.84-.053.16v7.5a1.5 1.5 0 1 0 3 0v-.5h12v.5a1.5 1.5 0 1 0 3 0v-4.5h-5a1 1 0 0 1-1-1m-8.5 1a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3M19.83 2.782a2.4 2.4 0 0 0-.592-.853q-.415-.396-1.09-.663Q17.47 1 16.457 1q-.785 0-1.418.253a3.2 3.2 0 0 0-1.084.703q-.449.45-.698 1.065t-.264 1.353h2.096q0-.369.085-.69t.264-.56.456-.383.663-.143q.57 0 .89.3.322.3.321.93.015.368-.135.614t-.392.45a9 9 0 0 1-.527.41 3.5 3.5 0 0 0-.542.485q-.256.28-.45.676-.191.397-.234.984v.614h1.924v-.519q.056-.409.278-.683.22-.273.506-.484a14 14 0 0 1 .606-.424q.32-.211.584-.512.264-.3.442-.724.178-.423.178-1.079 0-.395-.178-.854m-4.54 6.099v2.103h2.237V8.881z"];
})), o$, s$ = o((() => {
	o$ = ["M16 0c2.21 0 4 1.79 4 4 0 1.11-.46 2.09-1.18 2.82l.01.01-3 3-.01-.01a4.05 4.05 0 0 1-2.064 1.107l-.932-.931L17.41 5.41c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2-.55 0-1.05.22-1.41.58L10 7.17l-.927-.926A4.05 4.05 0 0 1 10.18 4.18l-.01-.01 3-3 .01.01C13.91.46 14.89 0 16 0m-5.296 7.876L13.29 5.29a1.003 1.003 0 1 1 1.42 1.42l-2.586 2.586zM8.583 9.997l-.7-.7L2.59 14.59c-.37.36-.59.86-.59 1.41 0 1.1.9 2 2 2 .55 0 1.05-.22 1.41-.58l1-1 4.298-4.298-.705-.705L6.71 14.71a1.004 1.004 0 1 1-1.42-1.42zm-.934-.934L3.293 4.707a1 1 0 0 1 1.414-1.414l12 12a1 1 0 0 1-1.414 1.414l-4.356-4.356c.04.21.063.423.063.649 0 1.11-.46 2.09-1.18 2.82l.01.01-3 3-.01-.01C6.09 19.54 5.11 20 4 20c-2.21 0-4-1.79-4-4 0-1.11.46-2.09 1.18-2.82l-.01-.01 3-3 .01.01C4.91 9.46 5.89 9 7 9c.225 0 .438.023.649.063"];
})), c$, l$ = o((() => {
	c$ = ["M14 1c-2.21 0-4 1.79-4 4v4H2c-.55 0-1 .45-1 1v8c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-8c0-.55-.45-1-1-1h-2V5c0-1.1.9-2 2-2s2 .9 2 2v2c0 .55.45 1 1 1s1-.45 1-1V5c0-2.21-1.79-4-4-4"];
})), u$, d$ = o((() => {
	u$ = ["M11.77 1.16c-.81.81-.74 2.28.02 3.76L6.1 8.71c-2.17-1.46-4.12-2-4.94-1.18l4.95 4.95-2.12 3.54 3.54-2.12 4.95 4.95c.82-.82.27-2.77-1.19-4.94l3.8-5.69c1.47.76 2.94.84 3.76.02z"];
})), f$, p$ = o((() => {
	f$ = ["M11.47 12.46c.16-.36.29-.74.38-1.14 0-.02.01-.04.01-.06.09-.4.14-.82.14-1.26s-.05-.86-.14-1.27c0-.02-.01-.04-.01-.06-.09-.4-.22-.78-.38-1.14-.01-.02-.02-.03-.02-.05a6 6 0 0 0-.61-1.03c0-.01-.01-.01-.01-.02a6.3 6.3 0 0 0-2.1-1.77c-.19-.1-.39-.18-.59-.26-.03-.01-.06-.02-.1-.03-.17-.07-.34-.12-.52-.17-.05-.01-.1-.03-.15-.04a4 4 0 0 0-.52-.09c-.05-.01-.11-.02-.17-.03C6.46 4.02 6.23 4 6 4c-3.31 0-6 2.69-6 6s2.69 6 6 6c.23 0 .46-.02.68-.04l.17-.03c.17-.02.34-.06.51-.09.05-.01.1-.03.15-.04.18-.05.36-.1.53-.17l.09-.03a5.97 5.97 0 0 0 2.68-2.04c0-.01.01-.01.01-.02.24-.32.44-.66.61-1.03.02-.01.03-.03.04-.05M14 4c-.99 0-1.91.24-2.73.66a7.51 7.51 0 0 1 0 10.68c.82.42 1.74.66 2.73.66 3.31 0 6-2.69 6-6s-2.69-6-6-6"];
})), m$, h$ = o((() => {
	m$ = ["M10 0C6.71 0 3.82 1.6 2 4.05V2c0-.55-.45-1-1-1s-1 .45-1 1v4c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1H3.76C5.22 3.17 7.47 2 10 2c4.42 0 8 3.58 8 8s-3.58 8-8 8-8-3.58-8-8c0-.55-.45-1-1-1s-1 .45-1 1c0 5.52 4.48 10 10 10s10-4.48 10-10S15.52 0 10 0m4 7c-.28 0-.53.11-.71.29L9 11.58 6.71 9.29a1.003 1.003 0 0 0-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l5-5A1.003 1.003 0 0 0 14 7"];
})), g$, _$ = o((() => {
	g$ = ["M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0m4 10c-.28 0-.53-.11-.71-.29L11 7.41V15c0 .55-.45 1-1 1s-1-.45-1-1V7.41l-2.29 2.3a1.003 1.003 0 0 1-1.42-1.42l4-4c.18-.18.43-.29.71-.29s.53.11.71.29l4 4A1.003 1.003 0 0 1 14 10"];
})), v$, y$ = o((() => {
	v$ = ["M10 0C4.48 0 0 4.48 0 10c0 .33.02.65.05.97.01.12.03.23.05.35.03.2.05.4.09.59.03.14.06.28.1.42l.12.48c.05.16.1.31.15.46.05.13.09.27.15.4q.09.24.21.48c.05.11.1.22.16.33.09.17.17.34.27.5.05.09.1.17.15.25.11.18.22.35.34.52.04.06.08.11.12.17 1.19 1.62 2.85 2.86 4.78 3.53l.09.03c.46.15.93.27 1.42.36.08.01.17.03.25.04.49.07.99.12 1.5.12s1.01-.05 1.5-.12c.08-.01.17-.02.25-.04.49-.09.96-.21 1.42-.36l.09-.03c1.93-.67 3.59-1.91 4.78-3.53.04-.05.08-.1.12-.16.12-.17.23-.35.34-.53.05-.08.1-.16.15-.25q.15-.255.27-.51c.05-.11.1-.21.15-.32.07-.16.14-.32.21-.49.05-.13.1-.26.14-.39.05-.15.11-.31.15-.46.05-.16.08-.32.12-.48.03-.14.07-.28.1-.42.04-.19.06-.39.09-.59.02-.12.04-.23.05-.35.05-.32.07-.64.07-.97 0-5.52-4.48-10-10-10m0 18a7.94 7.94 0 0 1-6.15-2.89c.84-.44 1.86-.82 2.67-1.19 1.45-.65 1.3-1.05 1.35-1.59.01-.07.01-.14.01-.21-.51-.45-.93-1.08-1.2-1.8l-.01-.01c0-.01-.01-.02-.01-.03a4 4 0 0 1-.15-.48c-.33-.07-.53-.44-.61-.79-.08-.14-.23-.48-.2-.87.05-.51.26-.74.49-.83v-.08c0-.63.06-1.55.17-2.15.02-.17.06-.33.11-.5.21-.73.66-1.4 1.26-1.86.62-.47 1.5-.72 2.28-.72s1.65.25 2.27.73c.6.46 1.05 1.12 1.26 1.86.05.16.08.33.11.5.11.6.17 1.51.17 2.15v.09c.22.1.42.33.46.82.04.39-.12.73-.2.87-.07.34-.27.71-.6.78-.04.16-.09.33-.15.48 0 .01-.02.05-.02.05-.26.71-.67 1.33-1.17 1.78 0 .08.01.16.01.23.05.54-.15.94 1.31 1.59.81.36 1.84.74 2.68 1.19A7.96 7.96 0 0 1 10 18"];
})), b$, x$ = o((() => {
	b$ = ["M4.93 3.79a9.1 9.1 0 0 1 2.2-2.27L7.29 1c-1.38.59-2.57 1.33-3.55 2.22C2.46 4.39 1.49 5.72.83 7.23.28 8.51 0 9.81 0 11.12c0 2.28.83 4.57 2.49 6.86l.16-.55c-.49-1.23-.73-2.38-.73-3.44 0-1.67.28-3.46.84-5.36.55-1.9 1.28-3.51 2.17-4.84m9.38 8.39-.33-.2c-.37.54-.65.87-.82 1a.74.74 0 0 1-.42.12c-.19 0-.38-.12-.57-.37-.31-.42-.73-1.59-1.26-3.5.47-.85.86-1.41 1.19-1.67.23-.19.48-.29.74-.29.1 0 .28.04.53.11.26.07.48.11.68.11.27 0 .5-.1.68-.29q.27-.285.27-.75c0-.33-.09-.58-.27-.77s-.44-.29-.78-.29c-.3 0-.59.07-.86.22s-.61.47-1.02.97c-.31.37-.77 1.02-1.37 1.94a9.7 9.7 0 0 0-1.24-3.14l-3.24.59-.06.36c.24-.05.44-.07.61-.07.32 0 .59.14.8.43.33.45.8 1.8 1.39 4.07-.47.64-.78 1.06-.96 1.26-.28.32-.52.53-.7.62-.14.08-.3.11-.48.11-.14 0-.36-.08-.67-.23q-.315-.15-.57-.15c-.31 0-.57.11-.78.32s-.31.48-.31.8c0 .31.09.55.28.75.19.19.44.29.76.29.31 0 .6-.07.87-.2s.61-.42 1.02-.86.98-1.13 1.7-2.08c.28.9.52 1.56.72 1.97s.44.71.7.89q.39.27.99.27c.38 0 .77-.14 1.17-.43.54-.36 1.07-1 1.61-1.91M17.51 1l-.15.54c.49 1.24.73 2.39.73 3.45 0 1.43-.21 2.96-.63 4.6-.33 1.26-.75 2.45-1.27 3.55-.52 1.11-1.02 1.97-1.51 2.6-.49.62-1.09 1.2-1.8 1.72l-.17.53c1.38-.59 2.57-1.34 3.55-2.23 1.29-1.17 2.26-2.5 2.91-4 .55-1.28.83-2.59.83-3.91 0-2.27-.83-4.56-2.49-6.85"];
})), S$, C$ = o((() => {
	S$ = ["M7.13 2.02a9.1 9.1 0 0 0-2.2 2.27c-.89 1.33-1.62 2.94-2.17 4.84-.56 1.9-.84 3.69-.84 5.36 0 1.06.24 2.21.73 3.44l-.16.55C.83 16.19 0 13.9 0 11.62c0-1.31.28-2.61.83-3.89.66-1.51 1.63-2.84 2.91-4.01.98-.89 2.17-1.63 3.55-2.22zm2.33 3.86c.59.95 1 2 1.24 3.14.6-.92 1.06-1.57 1.37-1.94.41-.5.75-.82 1.02-.97s.56-.22.86-.22c.34 0 .6.1.78.29s.27.44.27.77q0 .465-.27.75c-.18.19-.41.29-.68.29-.2 0-.42-.04-.68-.11-.25-.07-.43-.11-.53-.11-.26 0-.51.1-.74.29-.33.26-.72.82-1.19 1.67q.523 1.883.903 2.802l-2.048 1.139-.008.003q-.274-.621-.637-1.784c-.72.95-1.29 1.64-1.7 2.08s-.75.73-1.02.86-.56.2-.87.2c-.32 0-.57-.1-.76-.29-.19-.2-.28-.44-.28-.75 0-.32.1-.59.31-.8s.47-.32.78-.32q.255 0 .57.15c.31.15.53.23.67.23.18 0 .34-.03.48-.11.18-.09.42-.3.7-.62.18-.2.49-.62.96-1.26-.59-2.27-1.06-3.62-1.39-4.07-.21-.29-.48-.43-.8-.43a3 3 0 0 0-.61.07l.06-.36zm8.05-4.38C19.17 3.79 20 6.08 20 8.35c0 1.32-.28 2.63-.83 3.91q-.144.33-.308.648l-1.934-1.075a22 22 0 0 0 .532-1.743c.42-1.64.63-3.17.63-4.6 0-1.06-.24-2.21-.73-3.45zm-7.26 13.945 4.5 2.5c.1.05.15.05.25.05s.15 0 .25-.05l4.5-2.5c.15-.1.25-.25.25-.45s-.1-.35-.25-.45l-4.5-2.5c-.1-.05-.15-.05-.25-.05s-.15 0-.25.05l-4.5 2.5c-.15.1-.25.25-.25.45s.1.35.25.45m9.25 1.05c-.1 0-.15 0-.25.05l-4.25 2.4-4.25-2.4c-.1-.05-.15-.05-.25-.05-.3 0-.5.2-.5.5 0 .2.1.35.25.45l4.5 2.5c.1.05.15.05.25.05s.15 0 .25-.05l4.5-2.5c.15-.1.25-.25.25-.45 0-.3-.2-.5-.5-.5"];
})), w$, T$ = o((() => {
	w$ = ["M11.286 1.7a1 1 0 0 1-.29-.71c0-.55.45-1 1-.99a1 1 0 0 1 .711.29l3.003 3a1.013 1.013 0 0 1 0 1.419l-3.003 2.999a1.003 1.003 0 0 1-1.712-.71c0-.28.12-.53.3-.71l1.292-1.29H5.001A1 1 0 0 1 4 4c0-.55.45-1 1-1h7.587zm-5.733 8.406a1 1 0 0 1 1.341.447L10 16.763l3.106-6.21a1 1 0 0 1 1.789.894l-4 8a1 1 0 0 1-1.79 0l-4-8a1 1 0 0 1 .448-1.341"];
})), E$, D$ = o((() => {
	E$ = ["M8 7H7c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1M3 9H2c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-9c0-.55-.45-1-1-1m10-5h-1c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m5-4h-1c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1"];
})), O$, k$ = o((() => {
	O$ = ["M3 0H2c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m5 4H7c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m5 3h-1c-.55 0-1 .45-1 1v11c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1m5 2h-1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-9c0-.55-.45-1-1-1"];
})), A$, j$ = o((() => {
	A$ = ["M1 2h18c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1s.45 1 1 1m2 5c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V8c0-.55-.45-1-1-1zm16 11H1c-.55 0-1 .45-1 1s.45 1 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), M$, N$ = o((() => {
	M$ = ["M0 0h20v1a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm6.293 11.293a1 1 0 0 0 0 1.412l2.962 2.963.038.04A1 1 0 0 0 10 16a1 1 0 0 0 .745-.332l2.962-2.963a.999.999 0 0 0-1.412-1.412L10 13.587l-2.295-2.294a1 1 0 0 0-1.412 0m0-3.998a.999.999 0 1 0 1.412 1.412L10 6.413l2.295 2.294a.999.999 0 1 0 1.412-1.412l-2.962-2.963-.038-.04A1 1 0 0 0 10 4a1 1 0 0 0-.745.332zM20 19v1H0v-1a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1"];
})), P$, F$ = o((() => {
	P$ = ["M19 2H1c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h18c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1M7 14V6l6 4z"];
})), I$, L$ = o((() => {
	I$ = ["m15.249 13.835 1.251 1.251.354-.354.087-.077a1 1 0 0 1 1.327 1.491l-2.122 2.122-.087.077a1 1 0 0 1-1.327-1.491l.354-.354-1.251-1.251A6.5 6.5 0 0 1 11 16.424L10.999 18h.501a1 1 0 0 1 .117 1.993L11.5 20h-3a1 1 0 0 1-.117-1.993L8.5 18h.499v-1.577a6.5 6.5 0 0 1-2.538-.97L5.414 16.5l.354.354a1 1 0 0 1-1.327 1.491l-.087-.077-2.122-2.122a1 1 0 0 1 1.327-1.491l.087.077.354.354.97-.97a6.5 6.5 0 0 1-1.384-3.057l-.025.002L2 11.06v.44a1 1 0 0 1-1.993.117L0 11.5v-3a1 1 0 0 1 1.993-.117L2 8.5v.56h1.567A6.47 6.47 0 0 1 4.97 5.883l-.971-.969-.353.354-.087.077a1 1 0 0 1-1.327-1.491l2.122-2.122.087-.077a1 1 0 0 1 1.327 1.491l-.354.353 1.047 1.048A6.5 6.5 0 0 1 9 3.577V2h-.5A1 1 0 0 1 8.383.007L8.5 0h3a1 1 0 0 1 .117 1.993L11.5 2H11v1.577a6.5 6.5 0 0 1 2.838 1.176l.04-.046L15.086 3.5l-.353-.353a1 1 0 0 1 1.327-1.491l.087.077 2.122 2.122a1 1 0 0 1-1.327 1.491l-.087-.077-.354-.354-1.207 1.207-.046.041a6.5 6.5 0 0 1 1.16 2.733H18V8.5a1 1 0 0 1 1.993-.117L20 8.5v3a1 1 0 0 1-1.993.117L18 11.5v-.605h-1.561a6.5 6.5 0 0 1-1.19 2.94M12.5 11a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4"];
})), R$, z$ = o((() => {
	R$ = ["m15.92 3.93-1.6 1.18A7.95 7.95 0 0 1 16 10c0 1.84-.63 3.54-1.68 4.89l1.6 1.18A9.88 9.88 0 0 0 18 10c0-2.29-.78-4.39-2.08-6.07M11 3c-.28 0-.53.11-.71.29L7.59 6H3c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h4.59l2.71 2.71c.17.18.42.29.7.29.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), B$, V$ = o((() => {
	B$ = ["M14 3c-.28 0-.53.11-.71.29L10.59 6H6c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h4.59l2.71 2.71c.17.18.42.29.7.29.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"];
})), H$, U$ = o((() => {
	H$ = ["M9 3.43c-.28 0-.53.11-.71.29l-2.7 2.71H1c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h4.59l2.71 2.71a1.003 1.003 0 0 0 1.71-.71v-12c-.01-.55-.46-1-1.01-1m8.31-1.56-1.62 1.2C17.14 5.16 18 7.69 18 10.43s-.86 5.27-2.31 7.37l1.62 1.2C19 16.57 20 13.62 20 10.43c0-3.18-1-6.13-2.69-8.56m-3.39 2.49-1.6 1.18A7.95 7.95 0 0 1 14 10.43c0 1.84-.63 3.54-1.68 4.89l1.6 1.18A9.94 9.94 0 0 0 16 10.43c0-2.28-.78-4.38-2.08-6.07"];
})), W$, G$ = o((() => {
	W$ = ["M16 10h-2c-.23 0-.42-.09-.59-.21l-.01.01-1.69-1.27-.63 3.14 2.62 2.62c.19.18.3.43.3.71v4c0 .55-.45 1-1 1s-1-.45-1-1v-3.59L9.39 12.8l-2.45 6.55h-.01c-.14.38-.5.65-.93.65-.55 0-1-.45-1-1 0-.12.03-.24.07-.35h-.01L9.43 7h-2.9l-1.7 2.55-.01-.01c-.18.27-.47.46-.82.46-.55 0-1-.45-1-1 0-.21.08-.39.18-.54l-.01-.01 2-3 .02.01C5.36 5.19 5.65 5 6 5h4.18l.36-.96c-.33-.43-.54-.96-.54-1.54a2.5 2.5 0 0 1 5 0A2.5 2.5 0 0 1 12.5 5c-.06 0-.12-.01-.18-.02l-.44 1.18L14.33 8H16c.55 0 1 .45 1 1s-.45 1-1 1"];
})), K$, q$ = o((() => {
	K$ = ["m19.86 17.52.01-.01-9-16-.01.01C10.69 1.21 10.37 1 10 1s-.69.21-.86.52l-.01-.01-9 16 .01.01c-.08.14-.14.3-.14.48 0 .55.45 1 1 1h18c.55 0 1-.45 1-1 0-.18-.06-.34-.14-.48M11 17H9v-2h2zm0-3H9V6h2z"];
})), J$, Y$ = o((() => {
	J$ = ["M13 7h2c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1h-2c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1m-9 8h1c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1m4-6h2c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1m11-5h-1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h1c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1m0 12H2V3c0-.55-.45-1-1-1s-1 .45-1 1v14a1 1 0 0 0 1 1h18c.55 0 1-.45 1-1s-.45-1-1-1"];
})), X$, Z$ = o((() => {
	X$ = ["M4.948 2.682a1 1 0 0 0-1.897.001l-.005.016-.027.074a6 6 0 0 1-.6 1.172C1.958 4.635 1.468 5 .999 5a1 1 0 0 0 0 2c1.457 0 2.442-1.027 3-1.825C4.558 5.973 5.543 7 7 7s2.442-1.027 3-1.825C10.558 5.973 11.543 7 13 7s2.442-1.027 3-1.825C16.558 5.973 17.544 7 19 7a1 1 0 1 0 0-2c-.47 0-.958-.365-1.418-1.055a6 6 0 0 1-.628-1.246l-.006-.016a1 1 0 0 0-1.896 0l-.006.016-.027.074a6 6 0 0 1-.6 1.172C13.959 4.635 13.469 5 13 5s-.958-.365-1.418-1.055a6 6 0 0 1-.628-1.246l-.006-.016a1 1 0 0 0-1.897 0l-.005.016-.027.074a6 6 0 0 1-.6 1.172C7.958 4.635 7.468 5 6.999 5s-.958-.365-1.418-1.055A6 6 0 0 1 4.954 2.7zm0 6a1 1 0 0 0-1.897.001l-.005.016-.027.074a6 6 0 0 1-.6 1.172C1.959 10.635 1.469 11 1 11a1 1 0 1 0 0 2c1.457 0 2.442-1.027 3-1.825C4.558 11.973 5.543 13 7 13s2.442-1.027 3-1.825c.558.798 1.543 1.825 3 1.825s2.442-1.027 3-1.825c.558.798 1.544 1.825 3 1.825a1 1 0 1 0 0-2c-.47 0-.958-.365-1.418-1.055a6 6 0 0 1-.628-1.246l-.006-.016a1 1 0 0 0-1.896 0l-.006.016-.027.074a6 6 0 0 1-.6 1.172c-.46.69-.95 1.055-1.419 1.055s-.958-.365-1.418-1.055a6 6 0 0 1-.628-1.246l-.006-.016a1 1 0 0 0-1.897 0l-.005.016-.027.074a6 6 0 0 1-.6 1.172C7.959 10.635 7.469 11 7 11s-.958-.365-1.418-1.055A6 6 0 0 1 4.954 8.7zm0 6 .006.017.027.074a6 6 0 0 0 .6 1.172C6.041 16.635 6.531 17 7 17s.958-.365 1.418-1.055a6 6 0 0 0 .628-1.246l.005-.016a1 1 0 0 1 1.897 0l.006.016.027.074a6 6 0 0 0 .6 1.172c.46.69.95 1.055 1.419 1.055s.958-.365 1.418-1.055a6 6 0 0 0 .628-1.246l.006-.016a1 1 0 0 1 1.896 0l.006.016.027.074a6 6 0 0 0 .6 1.172c.46.69.95 1.055 1.419 1.055a1 1 0 1 1 0 2c-1.456 0-2.442-1.027-3-1.825-.558.798-1.543 1.825-3 1.825s-2.442-1.027-3-1.825C9.442 17.973 8.457 19 7 19s-2.442-1.027-3-1.825C3.442 17.973 2.457 19 1 19a1 1 0 1 1 0-2c.47 0 .958-.365 1.418-1.055a6 6 0 0 0 .628-1.246l.005-.016a1 1 0 0 1 1.897-.001"];
})), Q$, $$ = o((() => {
	Q$ = ["M18 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2M2 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m15-1h2V5h-2zM3 5H1v10h2zM2 0C.9 0 0 .9 0 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m3 3h10V1H5zm13 13c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2M5 19h10v-2H5z"];
})), e1, t1 = o((() => {
	e1 = ["M1 4h18c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V5c0-.55.45-1 1-1m1 2v8h16V6zm4 5c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m4 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1m4 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"];
})), n1, r1 = o((() => {
	n1 = ["M17 0H3c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H4v-4h12zm0-5H4V2h12z"];
})), i1, a1 = o((() => {
	i1 = ["M17 0H3c-.55 0-1 .45-1 1v18c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V1c0-.55-.45-1-1-1m-1 18H4V7h12zm0-12H4V2h12z"];
})), o1, s1 = o((() => {
	o1 = ["M12 6a3 3 0 1 1 3 3H4a1 1 0 0 0 0 2h11a5 5 0 1 0-5-5 1 1 0 1 0 2 0M1 12a1 1 0 1 0 0 2h10a2 2 0 1 1 0 4c-.934 0-1.803-.614-2.057-1.333a1 1 0 1 0-1.886.666C7.627 18.944 9.321 20 11 20a4 4 0 0 0 0-8z"];
})), c1, l1 = o((() => {
	c1 = ["M4 6h3.5l1-4h3l1 4H16l1-4h3l-1.062 4H19a1 1 0 1 1 0 2h-.594l-.265 1H19a1 1 0 1 1 0 2h-1.39l-1.86 7h-3l-1.86-7H9.11l-1.86 7h-3l-1.86-7H1a1 1 0 1 1 0-2h.86l-.266-1H1a1 1 0 0 1 0-2h.063L0 2h3zm1.75 7 .5-2h-1zm8-2 .5 2 .5-2zM13 8l.25 1h2l.25-1zM4.75 9h2L7 8H4.5zm4.89 0h.72l-.266-1h-.188z"];
})), u1, d1 = o((() => {
	u1 = ["M16.5 9a3.5 3.5 0 1 1 0 7h-3.09l.29.29c.19.18.3.43.3.71a1.003 1.003 0 0 1-1.71.71l-2-2c-.18-.19-.29-.44-.29-.71 0-.28.11-.53.29-.71l2-2c.18-.18.43-.29.71-.29a.99.99 0 0 1 1 1c0 .28-.11.53-.29.71l-.3.29h3.09a1.5 1.5 0 0 0 0-3H1a1 1 0 1 1 0-2zM7 14a1 1 0 1 1 0 2H1a1 1 0 1 1 0-2zM19 4c.55 0 1 .45 1 1s-.45 1-1 1H1c-.55 0-1-.45-1-1s.45-1 1-1z"];
})), f1, p1 = o((() => {
	f1 = ["M19.8 4.44 16.13 8.1l-3.55-.71-.71-3.53L15.54.21c-2.01-.53-4.23-.03-5.8 1.53-1.86 1.85-2.23 4.6-1.14 6.83L.59 16.59C.22 16.95 0 17.45 0 18a2 2 0 0 0 2 2c.55 0 1.05-.22 1.41-.59l8.03-8.04c2.23 1.05 4.97.67 6.82-1.16 1.57-1.56 2.07-3.77 1.54-5.77"];
})), m1, h1 = o((() => {
	m1 = ["M4 9C2.34 9 1 7.66 1 6s1.34-3 3-3h1.59l-.3-.29a1.003 1.003 0 0 1 1.42-1.42l2 2c.18.18.29.43.29.71s-.11.53-.29.71l-2 2a1.003 1.003 0 0 1-1.42-1.42l.3-.29H4c-.55 0-1 .45-1 1s.45 1 1 1a1 1 0 1 1 0 2m9.5 7c-.821 0-1.6-.18-2.3-.503l-2.944 2.944a1.907 1.907 0 0 1-2.697-2.697L8.503 12.8a5.5 5.5 0 0 1 7.68-7.103l-3.744 3.742a1.5 1.5 0 1 0 2.122 2.122l3.742-3.743A5.5 5.5 0 0 1 13.5 16"];
})), g1, _1 = o((() => {
	g1 = ["M2 1h4a1 1 0 0 1 .775 1.632L4.08 6H6a1 1 0 0 1 0 2H2a1 1 0 0 1-.771-1.636L3.919 3H2a1 1 0 0 1 0-2m11.5 15c-.821 0-1.6-.18-2.3-.503l-2.944 2.944a1.907 1.907 0 0 1-2.697-2.697L8.503 12.8a5.5 5.5 0 0 1 7.68-7.103l-3.744 3.742a1.5 1.5 0 1 0 2.122 2.122l3.742-3.743A5.5 5.5 0 0 1 13.5 16"];
})), v1, y1 = o((() => {
	v1 = ["M1 4.5C1 2.57 2.57 1 4.5 1S8 2.57 8 4.5 6.43 8 4.5 8 1 6.43 1 4.5m3-2v2.21l1.56 1.56c.1.09.23.14.36.14.12 0 .25-.05.35-.14.19-.2.19-.51 0-.71L5 4.29V2.5c0-.28-.22-.5-.5-.5s-.5.22-.5.5M13.5 16c-.821 0-1.6-.18-2.3-.503l-2.944 2.944a1.907 1.907 0 0 1-2.697-2.697L8.503 12.8a5.5 5.5 0 0 1 7.68-7.103l-3.744 3.742a1.5 1.5 0 1 0 2.122 2.122l3.742-3.743A5.5 5.5 0 0 1 13.5 16"];
})), b1, x1 = o((() => {
	b1 = ["M10 8.546 14 2h3l-4.889 8H15a1 1 0 1 1 0 2h-3.5v1H15a1 1 0 1 1 0 2h-3.5v4h-3v-4H5a1 1 0 0 1 0-2h3.5v-1H5a1 1 0 0 1 0-2h2.889L3 2h3z"];
})), S1, C1 = o((() => {
	S1 = ["m19.56 17.44-4.94-4.94A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8S0 3.58 0 8s3.58 8 8 8c1.67 0 3.21-.51 4.5-1.38l4.94 4.94a1.498 1.498 0 1 0 2.12-2.12M8 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6m3-7H9V5c0-.55-.45-1-1-1s-1 .45-1 1v2H5c-.55 0-1 .45-1 1s.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V9h2c.55 0 1-.45 1-1s-.45-1-1-1"];
})), w1, T1 = o((() => {
	w1 = ["M11 7H5c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1m8.56 10.44-4.94-4.94A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8S0 3.58 0 8s3.58 8 8 8c1.67 0 3.21-.51 4.5-1.38l4.94 4.94a1.498 1.498 0 1 0 2.12-2.12M8 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6"];
})), E1, D1 = o((() => {
	E1 = ["M1 7c.55 0 1-.45 1-1V2h4c.55 0 1-.45 1-1s-.45-1-1-1H1C.45 0 0 .45 0 1v5c0 .55.45 1 1 1m5 1a1.003 1.003 0 0 0-1.71-.71l-2 2c-.18.18-.29.43-.29.71s.11.53.29.71l2 2a1.003 1.003 0 0 0 1.42-1.42L4.41 10 5.7 8.71c.19-.18.3-.43.3-.71m2-2c.28 0 .53-.11.71-.29L10 4.41l1.29 1.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71l-2-2C10.53 2.11 10.28 2 10 2s-.53.11-.71.29l-2 2A1.003 1.003 0 0 0 8 6M6 18H2v-4c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55.45 1 1 1h5c.55 0 1-.45 1-1s-.45-1-1-1m8-6a1.003 1.003 0 0 0 1.71.71l2-2c.18-.18.29-.43.29-.71s-.11-.53-.29-.71l-2-2a1.003 1.003 0 0 0-1.42 1.42l1.3 1.29-1.29 1.29c-.19.18-.3.43-.3.71m5-12h-5c-.55 0-1 .45-1 1s.45 1 1 1h4v4c0 .55.45 1 1 1s1-.45 1-1V1c0-.55-.45-1-1-1m-7 14c-.28 0-.53.11-.71.29L10 15.59 8.71 14.3A.97.97 0 0 0 8 14a1.003 1.003 0 0 0-.71 1.71l2 2c.18.18.43.29.71.29s.53-.11.71-.29l2-2A1.003 1.003 0 0 0 12 14m7-1c-.55 0-1 .45-1 1v4h-4c-.55 0-1 .45-1 1s.45 1 1 1h5c.55 0 1-.45 1-1v-5c0-.55-.45-1-1-1"];
})), O1 = /* @__PURE__ */ c({
	Add: () => bO,
	AddApplication: () => SO,
	AddChild: () => wO,
	AddClip: () => EO,
	AddColumnLeft: () => OO,
	AddColumnRight: () => AO,
	AddDerivedColumn: () => MO,
	AddLocation: () => PO,
	AddParent: () => IO,
	AddRowBottom: () => RO,
	AddRowTop: () => BO,
	AddTile: () => HO,
	AddToArtifact: () => WO,
	AddToFolder: () => KO,
	AimpointsTarget: () => JO,
	Airplane: () => XO,
	AlignCenter: () => QO,
	AlignJustify: () => ek,
	AlignLeft: () => nk,
	AlignRight: () => ik,
	AlignmentBottom: () => ok,
	AlignmentHorizontalCenter: () => ck,
	AlignmentLeft: () => uk,
	AlignmentRight: () => fk,
	AlignmentTop: () => mk,
	AlignmentVerticalCenter: () => gk,
	Ammunition: () => vk,
	Anchor: () => bk,
	Annotation: () => Sk,
	Announcement: () => wk,
	Antenna: () => Ek,
	AppHeader: () => Ok,
	Application: () => Ak,
	Applications: () => Mk,
	Archive: () => Pk,
	AreaOfInterest: () => Ik,
	Array: () => Rk,
	ArrayBoolean: () => Bk,
	ArrayDate: () => Hk,
	ArrayFloatingPoint: () => Wk,
	ArrayNumeric: () => Kk,
	ArrayObject: () => Jk,
	ArrayString: () => Xk,
	ArrayTimestamp: () => Qk,
	ArrowBottomLeft: () => eA,
	ArrowBottomRight: () => nA,
	ArrowDown: () => iA,
	ArrowLeft: () => oA,
	ArrowRight: () => cA,
	ArrowTopLeft: () => uA,
	ArrowTopRight: () => fA,
	ArrowUp: () => mA,
	ArrowsArc: () => gA,
	ArrowsHorizontal: () => vA,
	ArrowsVertical: () => bA,
	Asterisk: () => SA,
	At: () => wA,
	AutomaticUpdates: () => EA,
	Axle: () => OA,
	Backlink: () => AA,
	BackwardTen: () => MA,
	Badge: () => PA,
	BanCircle: () => IA,
	BankAccount: () => RA,
	Barcode: () => BA,
	BinaryNumber: () => HA,
	Blank: () => WA,
	BlockPromote: () => KA,
	BlockedPerson: () => JA,
	Bold: () => XA,
	Book: () => QA,
	Bookmark: () => ej,
	Box: () => nj,
	BranchLocked: () => ij,
	BranchUnlocked: () => oj,
	Briefcase: () => cj,
	BringData: () => uj,
	BringForward: () => fj,
	BritishPound: () => mj,
	Bug: () => gj,
	Buggy: () => vj,
	Build: () => bj,
	Bullseye: () => Sj,
	Calculator: () => wj,
	Calendar: () => Ej,
	Camera: () => Oj,
	CaretDown: () => Aj,
	CaretLeft: () => Mj,
	CaretRight: () => Pj,
	CaretUp: () => Ij,
	CargoShip: () => Rj,
	CellTower: () => Bj,
	Changes: () => Hj,
	Chart: () => Wj,
	Chat: () => Kj,
	ChevronBackward: () => Jj,
	ChevronDown: () => Xj,
	ChevronForward: () => Qj,
	ChevronLeft: () => eM,
	ChevronRight: () => nM,
	ChevronUp: () => iM,
	Circle: () => oM,
	CircleArrowDown: () => cM,
	CircleArrowLeft: () => uM,
	CircleArrowRight: () => fM,
	CircleArrowUp: () => mM,
	CircleDashed: () => gM,
	Citation: () => vM,
	Clean: () => bM,
	Clip: () => SM,
	Clipboard: () => wM,
	ClipboardFile: () => EM,
	Cloud: () => OM,
	CloudDownload: () => AM,
	CloudServer: () => MM,
	CloudTick: () => PM,
	CloudUpload: () => IM,
	Code: () => RM,
	CodeBlock: () => BM,
	Cog: () => HM,
	CollapseAll: () => WM,
	ColorFill: () => KM,
	ColumnLayout: () => JM,
	Comment: () => XM,
	Comparison: () => QM,
	Compass: () => eN,
	Compressed: () => nN,
	Confirm: () => iN,
	Console: () => oN,
	ConsoleAlert: () => cN,
	Construction: () => uN,
	Contrast: () => fN,
	Control: () => mN,
	CreditCard: () => gN,
	Crop: () => vN,
	Cross: () => bN,
	CrossCircle: () => SN,
	Crown: () => wN,
	CrystalBall: () => EN,
	CssStyle: () => ON,
	Cube: () => AN,
	CubeAdd: () => MN,
	CubeCutout: () => PN,
	CubeCutouts: () => IN,
	CubeEdit: () => RN,
	CubeRemove: () => BN,
	Cubes: () => HN,
	CurlyBraces: () => WN,
	CurvedRangeChart: () => KN,
	Cut: () => JN,
	Cycle: () => XN,
	Dashboard: () => QN,
	DataCloud: () => eP,
	DataConnection: () => nP,
	DataLineage: () => iP,
	DataSearch: () => oP,
	DataSync: () => cP,
	Database: () => uP,
	Delete: () => fP,
	DeleteClip: () => mP,
	Delta: () => gP,
	DeriveColumn: () => vP,
	Descendant: () => bP,
	Desktop: () => SP,
	Detection: () => wP,
	Diagnosis: () => EP,
	DiagramTree: () => OP,
	DirectionLeft: () => AP,
	DirectionRight: () => MP,
	Disable: () => PP,
	Divide: () => IP,
	Document: () => RP,
	DocumentCode: () => BP,
	DocumentLocked: () => HP,
	DocumentOpen: () => WP,
	DocumentShare: () => KP,
	Dollar: () => JP,
	Dot: () => XP,
	DoubleCaretHorizontal: () => QP,
	DoubleCaretVertical: () => eF,
	DoubleChevronDown: () => nF,
	DoubleChevronLeft: () => iF,
	DoubleChevronRight: () => oF,
	DoubleChevronUp: () => cF,
	DoughnutChart: () => uF,
	Download: () => fF,
	DragHandleHorizontal: () => mF,
	DragHandleVertical: () => gF,
	Draw: () => vF,
	DrawerLeft: () => bF,
	DrawerLeftFilled: () => SF,
	DrawerRight: () => wF,
	DrawerRightFilled: () => EF,
	DriveTime: () => OF,
	Drone: () => AF,
	DroneUav: () => MF,
	Duplicate: () => PF,
	Edit: () => IF,
	Eject: () => RF,
	Emoji: () => BF,
	Endnote: () => HF,
	Endorsed: () => WF,
	Engagement: () => KF,
	Envelope: () => JF,
	Equals: () => XF,
	Eraser: () => QF,
	Error: () => eI,
	Euro: () => nI,
	Excavator: () => iI,
	Exchange: () => oI,
	ExcludeRow: () => cI,
	ExpandAll: () => uI,
	Explain: () => fI,
	Export: () => mI,
	EyeOff: () => gI,
	EyeOn: () => vI,
	EyeOpen: () => bI,
	FastBackward: () => SI,
	FastForward: () => wI,
	Feed: () => EI,
	FeedSubscribed: () => OI,
	FighterJet: () => AI,
	Film: () => MI,
	Filter: () => PI,
	FilterKeep: () => II,
	FilterList: () => RI,
	FilterOpen: () => BI,
	FilterRemove: () => HI,
	FilterSortAsc: () => WI,
	FilterSortDesc: () => KI,
	Flag: () => JI,
	Flame: () => XI,
	Flash: () => QI,
	FloatingPoint: () => eL,
	FloppyDisk: () => nL,
	FlowBranch: () => iL,
	FlowEnd: () => oL,
	FlowLinear: () => cL,
	FlowReview: () => uL,
	FlowReviewBranch: () => fL,
	Flows: () => mL,
	FolderClose: () => gL,
	FolderNew: () => vL,
	FolderOpen: () => bL,
	FolderShared: () => SL,
	FolderSharedOpen: () => wL,
	Follower: () => EL,
	Following: () => OL,
	Font: () => AL,
	Fork: () => ML,
	ForkEnd: () => PL,
	Form: () => IL,
	ForwardTen: () => RL,
	FrameToFrame: () => BL,
	Fuel: () => HL,
	FullCircle: () => WL,
	FullStackedChart: () => KL,
	Fullscreen: () => JL,
	Function: () => XL,
	FunctionMinimal: () => QL,
	GanttChart: () => eR,
	Generate: () => nR,
	Geofence: () => iR,
	Geolocation: () => oR,
	Geosearch: () => cR,
	Geotime: () => uR,
	GiftBox: () => fR,
	GitBranch: () => mR,
	GitCommit: () => gR,
	GitMerge: () => vR,
	GitNewBranch: () => bR,
	GitPull: () => SR,
	GitPush: () => wR,
	GitRebase: () => ER,
	GitRepo: () => OR,
	Glass: () => AR,
	Globe: () => MR,
	GlobeNetwork: () => PR,
	GlobeNetworkAdd: () => IR,
	Graph: () => RR,
	GraphRemove: () => BR,
	GreaterThan: () => HR,
	GreaterThanOrEqualTo: () => WR,
	Grid: () => KR,
	GridView: () => JR,
	GroupItem: () => XR,
	GroupObjects: () => QR,
	GroupedBarChart: () => ez,
	Hand: () => nz,
	HandDown: () => iz,
	HandLeft: () => oz,
	HandRight: () => cz,
	HandUp: () => uz,
	Hat: () => fz,
	Header: () => mz,
	HeaderOne: () => gz,
	HeaderThree: () => vz,
	HeaderTwo: () => bz,
	Headset: () => Sz,
	Heart: () => wz,
	HeartBroken: () => Ez,
	HeatGrid: () => Oz,
	Heatmap: () => Az,
	Helicopter: () => Mz,
	Help: () => Pz,
	HelperManagement: () => Iz,
	Hexagon: () => Rz,
	HighPriority: () => Bz,
	HighVoltagePole: () => Hz,
	Highlight: () => Wz,
	History: () => Kz,
	Home: () => Jz,
	HorizontalBarChart: () => Xz,
	HorizontalBarChartAsc: () => Qz,
	HorizontalBarChartDesc: () => eB,
	HorizontalDistribution: () => nB,
	HorizontalInbetween: () => iB,
	Hurricane: () => oB,
	IdNumber: () => cB,
	ImageRotateLeft: () => uB,
	ImageRotateRight: () => fB,
	Import: () => mB,
	Inbox: () => gB,
	InboxFiltered: () => vB,
	InboxGeo: () => bB,
	InboxSearch: () => SB,
	InboxUpdate: () => wB,
	InfoSign: () => EB,
	Inheritance: () => OB,
	InheritedGroup: () => AB,
	InnerJoin: () => MB,
	Input: () => PB,
	Insert: () => IB,
	Intelligence: () => RB,
	Intersection: () => BB,
	IpAddress: () => HB,
	Issue: () => WB,
	IssueClosed: () => KB,
	IssueNew: () => JB,
	Italic: () => XB,
	JoinTable: () => QB,
	Key: () => eV,
	KeyBackspace: () => nV,
	KeyCommand: () => iV,
	KeyControl: () => oV,
	KeyDelete: () => cV,
	KeyEnter: () => uV,
	KeyEscape: () => fV,
	KeyOption: () => mV,
	KeyShift: () => gV,
	KeyTab: () => vV,
	KnownVehicle: () => bV,
	LabTest: () => SV,
	Label: () => wV,
	Layer: () => EV,
	LayerOutline: () => OV,
	Layers: () => AV,
	Layout: () => MV,
	LayoutAuto: () => PV,
	LayoutBalloon: () => IV,
	LayoutBottomRowThreeTiles: () => RV,
	LayoutBottomRowTwoTiles: () => BV,
	LayoutCircle: () => HV,
	LayoutGrid: () => WV,
	LayoutGroupBy: () => KV,
	LayoutHierarchy: () => JV,
	LayoutLeftColumnThreeTiles: () => XV,
	LayoutLeftColumnTwoTiles: () => QV,
	LayoutLinear: () => eH,
	LayoutRightColumnThreeTiles: () => nH,
	LayoutRightColumnTwoTiles: () => iH,
	LayoutSkewGrid: () => oH,
	LayoutSortedClusters: () => cH,
	LayoutThreeColumns: () => uH,
	LayoutThreeRows: () => fH,
	LayoutTopRowThreeTiles: () => mH,
	LayoutTopRowTwoTiles: () => gH,
	LayoutTwoColumns: () => vH,
	LayoutTwoRows: () => bH,
	Learning: () => SH,
	LeftJoin: () => wH,
	LengthenText: () => EH,
	LessThan: () => OH,
	LessThanOrEqualTo: () => AH,
	Lifesaver: () => MH,
	Lightbulb: () => PH,
	Lightning: () => IH,
	Link: () => RH,
	LinkedSquares: () => BH,
	List: () => HH,
	ListColumns: () => WH,
	ListDetailView: () => KH,
	Locate: () => JH,
	Lock: () => XH,
	Locomotive: () => QH,
	LogIn: () => eU,
	LogOut: () => nU,
	LowVoltagePole: () => iU,
	Manual: () => oU,
	ManuallyEnteredData: () => cU,
	ManyToMany: () => uU,
	ManyToOne: () => fU,
	Map: () => mU,
	MapCreate: () => gU,
	MapMarker: () => vU,
	Markdown: () => bU,
	Maximize: () => SU,
	Media: () => wU,
	Menu: () => EU,
	MenuClosed: () => OU,
	MenuOpen: () => AU,
	MergeColumns: () => MU,
	MergeLinks: () => PU,
	Microphone: () => IU,
	Minimize: () => RU,
	Minus: () => BU,
	MobilePhone: () => HU,
	MobileVideo: () => WU,
	Modal: () => KU,
	ModalFilled: () => JU,
	Model: () => XU,
	Moon: () => QU,
	More: () => eW,
	Mountain: () => nW,
	Move: () => iW,
	Mugshot: () => oW,
	MultiSelect: () => cW,
	Music: () => uW,
	Nest: () => fW,
	NewComment: () => mW,
	NewDrawing: () => gW,
	NewGridItem: () => vW,
	NewLayer: () => bW,
	NewLayers: () => SW,
	NewLink: () => wW,
	NewObject: () => EW,
	NewPerson: () => OW,
	NewPrescription: () => AW,
	NewShield: () => MW,
	NewTextBox: () => PW,
	Ninja: () => IW,
	NotEqualTo: () => RW,
	Notifications: () => BW,
	NotificationsAdd: () => HW,
	NotificationsSnooze: () => WW,
	NotificationsUpdated: () => KW,
	NumberedList: () => JW,
	Numerical: () => XW,
	ObjectView: () => QW,
	Office: () => eG,
	Offline: () => nG,
	OilField: () => iG,
	OneColumn: () => oG,
	OneToMany: () => cG,
	OneToOne: () => uG,
	OpenApplication: () => fG,
	Outdated: () => mG,
	OuterJoin: () => gG,
	Output: () => vG,
	Package: () => bG,
	PageBreak: () => SG,
	PageLayout: () => wG,
	Panel: () => EG,
	PanelStats: () => OG,
	PanelTable: () => AG,
	Paperclip: () => MG,
	Paragraph: () => PG,
	PasteVariable: () => IG,
	Path: () => RG,
	PathSearch: () => BG,
	Pause: () => HG,
	People: () => WG,
	Percentage: () => KG,
	Person: () => JG,
	Phone: () => XG,
	PhoneCall: () => QG,
	PhoneForward: () => eK,
	PhoneSearch: () => nK,
	PieChart: () => iK,
	Pill: () => oK,
	Pin: () => cK,
	Pistol: () => uK,
	Pivot: () => fK,
	PivotTable: () => mK,
	Play: () => gK,
	Playbook: () => vK,
	Plus: () => bK,
	PolygonFilter: () => SK,
	Popout: () => wK,
	Power: () => EK,
	PredictiveAnalysis: () => OK,
	Prescription: () => AK,
	Presentation: () => MK,
	Print: () => PK,
	Projects: () => IK,
	Properties: () => RK,
	Property: () => BK,
	PublishFunction: () => HK,
	Pulse: () => WK,
	Rain: () => KK,
	Random: () => JK,
	RangeRing: () => XK,
	Record: () => QK,
	RectHeight: () => eq,
	RectWidth: () => nq,
	Rectangle: () => iq,
	Redo: () => oq,
	Refresh: () => cq,
	RefreshOff: () => uq,
	Regex: () => fq,
	RegressionChart: () => mq,
	Remove: () => gq,
	RemoveColumn: () => vq,
	RemoveColumnLeft: () => bq,
	RemoveColumnRight: () => Sq,
	RemoveRowBottom: () => wq,
	RemoveRowTop: () => Eq,
	Repeat: () => Oq,
	Reset: () => Aq,
	Resolve: () => Mq,
	Rig: () => Pq,
	RightJoin: () => Iq,
	Ring: () => Rq,
	Rocket: () => Bq,
	RocketSlant: () => Hq,
	RootFolder: () => Wq,
	RotateCcw: () => Kq,
	RotateCw: () => Jq,
	RotateDocument: () => Xq,
	RotatePage: () => Qq,
	Route: () => eJ,
	RunHistory: () => nJ,
	Satellite: () => iJ,
	Saved: () => oJ,
	ScatterPlot: () => cJ,
	Search: () => uJ,
	SearchAround: () => fJ,
	SearchTemplate: () => mJ,
	SearchText: () => gJ,
	SegmentedControl: () => vJ,
	Select: () => bJ,
	Selection: () => SJ,
	SelectionBox: () => wJ,
	SelectionBoxAdd: () => EJ,
	SelectionBoxEdit: () => OJ,
	SelectionBoxRemove: () => AJ,
	SendBackward: () => MJ,
	SendMessage: () => PJ,
	SendTo: () => IJ,
	SendToGraph: () => RJ,
	SendToMap: () => BJ,
	Sensor: () => HJ,
	SeriesAdd: () => WJ,
	SeriesConfiguration: () => KJ,
	SeriesDerived: () => JJ,
	SeriesFiltered: () => XJ,
	SeriesSearch: () => QJ,
	Server: () => eY,
	ServerInstall: () => nY,
	Settings: () => iY,
	Shapes: () => oY,
	Share: () => cY,
	SharedFilter: () => uY,
	Shield: () => fY,
	Ship: () => mY,
	Shop: () => gY,
	ShoppingCart: () => vY,
	ShortenText: () => bY,
	SignalSearch: () => SY,
	SimCard: () => wY,
	Slash: () => EY,
	SmallCross: () => OY,
	SmallInfoSign: () => AY,
	SmallMinus: () => MY,
	SmallPlus: () => PY,
	SmallSquare: () => IY,
	SmallTick: () => RY,
	Snowflake: () => BY,
	SoccerBall: () => HY,
	SocialMedia: () => WY,
	Sort: () => KY,
	SortAlphabetical: () => JY,
	SortAlphabeticalDesc: () => XY,
	SortAsc: () => QY,
	SortDesc: () => eX,
	SortNumerical: () => nX,
	SortNumericalDesc: () => iX,
	SpellCheck: () => oX,
	Spin: () => cX,
	SplitColumns: () => uX,
	SportsStadium: () => fX,
	Square: () => mX,
	StackedChart: () => gX,
	StadiumGeometry: () => vX,
	Star: () => bX,
	StarEmpty: () => SX,
	StepBackward: () => wX,
	StepChart: () => EX,
	StepForward: () => OX,
	Stop: () => AX,
	Stopwatch: () => MX,
	Strikethrough: () => PX,
	Style: () => IX,
	Subscript: () => RX,
	SubtractRightJoin: () => BX,
	Superscript: () => HX,
	SwapHorizontal: () => WX,
	SwapVertical: () => KX,
	Sweep: () => JX,
	Switch: () => XX,
	SymbolCircle: () => QX,
	SymbolCross: () => eZ,
	SymbolDiamond: () => nZ,
	SymbolRectangle: () => iZ,
	SymbolSquare: () => oZ,
	SymbolTriangleDown: () => cZ,
	SymbolTriangleUp: () => uZ,
	Syringe: () => fZ,
	TableSync: () => mZ,
	Tag: () => gZ,
	TagAdd: () => vZ,
	TagPromote: () => bZ,
	TagRefresh: () => SZ,
	TagUndo: () => wZ,
	Tags: () => EZ,
	TakeAction: () => OZ,
	Tank: () => AZ,
	Target: () => MZ,
	Taxi: () => PZ,
	Team: () => IZ,
	Temperature: () => RZ,
	TextHighlight: () => BZ,
	Th: () => HZ,
	ThAdd: () => WZ,
	ThDerived: () => KZ,
	ThDisconnect: () => JZ,
	ThFiltered: () => XZ,
	ThList: () => QZ,
	ThListAdd: () => eQ,
	ThVirtual: () => nQ,
	ThVirtualAdd: () => iQ,
	ThirdParty: () => oQ,
	ThumbsDown: () => cQ,
	ThumbsUp: () => uQ,
	Tick: () => fQ,
	TickCircle: () => mQ,
	Time: () => gQ,
	TimelineAreaChart: () => vQ,
	TimelineBarChart: () => bQ,
	TimelineEvents: () => SQ,
	TimelineLineChart: () => wQ,
	Tint: () => EQ,
	Torch: () => OQ,
	Tractor: () => AQ,
	Train: () => MQ,
	Translate: () => PQ,
	Trash: () => IQ,
	Tree: () => RQ,
	TrendingDown: () => BQ,
	TrendingUp: () => HQ,
	Trophy: () => WQ,
	Truck: () => KQ,
	TwoColumns: () => JQ,
	Unarchive: () => XQ,
	Underline: () => QQ,
	Undo: () => e$,
	UngroupObjects: () => n$,
	UnknownVehicle: () => i$,
	Unlink: () => o$,
	Unlock: () => c$,
	Unpin: () => u$,
	Unresolve: () => f$,
	Updated: () => m$,
	Upload: () => g$,
	User: () => v$,
	Variable: () => b$,
	VariableLayer: () => S$,
	Vector: () => w$,
	VerticalBarChartAsc: () => E$,
	VerticalBarChartDesc: () => O$,
	VerticalDistribution: () => A$,
	VerticalInbetween: () => M$,
	Video: () => P$,
	Virus: () => I$,
	VolumeDown: () => R$,
	VolumeOff: () => B$,
	VolumeUp: () => H$,
	Walk: () => W$,
	WarningSign: () => K$,
	WaterfallChart: () => J$,
	Waves: () => X$,
	Widget: () => Q$,
	WidgetButton: () => e1,
	WidgetFooter: () => n1,
	WidgetHeader: () => i1,
	Wind: () => o1,
	Won: () => c1,
	WrapLines: () => u1,
	Wrench: () => f1,
	WrenchRedo: () => m1,
	WrenchSnooze: () => g1,
	WrenchTime: () => v1,
	Yen: () => b1,
	ZoomIn: () => S1,
	ZoomOut: () => w1,
	ZoomToFit: () => E1
}), k1 = o((() => {
	xO(), CO(), TO(), DO(), kO(), jO(), NO(), FO(), LO(), zO(), VO(), UO(), GO(), qO(), YO(), ZO(), $O(), tk(), rk(), ak(), sk(), lk(), dk(), pk(), hk(), _k(), yk(), xk(), Ck(), Tk(), Dk(), kk(), jk(), Nk(), Fk(), Lk(), zk(), Vk(), Uk(), Gk(), qk(), Yk(), Zk(), $k(), tA(), rA(), aA(), sA(), lA(), dA(), pA(), hA(), _A(), yA(), xA(), CA(), TA(), DA(), kA(), jA(), NA(), FA(), LA(), zA(), VA(), UA(), GA(), qA(), YA(), ZA(), $A(), tj(), rj(), aj(), sj(), lj(), dj(), pj(), hj(), _j(), yj(), xj(), Cj(), Tj(), Dj(), kj(), jj(), Nj(), Fj(), Lj(), zj(), Vj(), Uj(), Gj(), qj(), Yj(), Zj(), $j(), tM(), rM(), aM(), sM(), lM(), dM(), pM(), hM(), _M(), yM(), xM(), CM(), TM(), DM(), kM(), jM(), NM(), FM(), LM(), zM(), VM(), UM(), GM(), qM(), YM(), ZM(), $M(), tN(), rN(), aN(), sN(), lN(), dN(), pN(), hN(), _N(), yN(), xN(), CN(), TN(), DN(), kN(), jN(), NN(), FN(), LN(), zN(), VN(), UN(), GN(), qN(), YN(), ZN(), $N(), tP(), rP(), aP(), sP(), lP(), dP(), pP(), hP(), _P(), yP(), xP(), CP(), TP(), DP(), kP(), jP(), NP(), FP(), LP(), zP(), VP(), UP(), GP(), qP(), YP(), ZP(), $P(), tF(), rF(), aF(), sF(), lF(), dF(), pF(), hF(), _F(), yF(), xF(), CF(), TF(), DF(), kF(), jF(), NF(), FF(), LF(), zF(), VF(), UF(), GF(), qF(), YF(), ZF(), $F(), tI(), rI(), aI(), sI(), lI(), dI(), pI(), hI(), _I(), yI(), xI(), CI(), TI(), DI(), kI(), jI(), NI(), FI(), LI(), zI(), VI(), UI(), GI(), qI(), YI(), ZI(), $I(), tL(), rL(), aL(), sL(), lL(), dL(), pL(), hL(), _L(), yL(), xL(), CL(), TL(), DL(), kL(), jL(), NL(), FL(), LL(), zL(), VL(), UL(), GL(), qL(), YL(), ZL(), $L(), tR(), rR(), aR(), sR(), lR(), dR(), pR(), hR(), _R(), yR(), xR(), CR(), TR(), DR(), kR(), jR(), NR(), FR(), LR(), zR(), VR(), UR(), GR(), qR(), YR(), ZR(), $R(), tz(), rz(), az(), sz(), lz(), dz(), pz(), hz(), _z(), yz(), xz(), Cz(), Tz(), Dz(), kz(), jz(), Nz(), Fz(), Lz(), zz(), Vz(), Uz(), Gz(), qz(), Yz(), Zz(), $z(), tB(), rB(), aB(), sB(), lB(), dB(), pB(), hB(), _B(), yB(), xB(), CB(), TB(), DB(), kB(), jB(), NB(), FB(), LB(), zB(), VB(), UB(), GB(), qB(), YB(), ZB(), $B(), tV(), rV(), aV(), sV(), lV(), dV(), pV(), hV(), _V(), yV(), xV(), CV(), TV(), DV(), kV(), jV(), NV(), FV(), LV(), zV(), VV(), UV(), GV(), qV(), YV(), ZV(), $V(), tH(), rH(), aH(), sH(), lH(), dH(), pH(), hH(), _H(), yH(), xH(), CH(), TH(), DH(), kH(), jH(), NH(), FH(), LH(), zH(), VH(), UH(), GH(), qH(), YH(), ZH(), $H(), tU(), rU(), aU(), sU(), lU(), dU(), pU(), hU(), _U(), yU(), xU(), CU(), TU(), DU(), kU(), jU(), NU(), FU(), LU(), zU(), VU(), UU(), GU(), qU(), YU(), ZU(), $U(), tW(), rW(), aW(), sW(), lW(), dW(), pW(), hW(), _W(), yW(), xW(), CW(), TW(), DW(), kW(), jW(), NW(), FW(), LW(), zW(), VW(), UW(), GW(), qW(), YW(), ZW(), $W(), tG(), rG(), aG(), sG(), lG(), dG(), pG(), hG(), _G(), yG(), xG(), CG(), TG(), DG(), kG(), jG(), NG(), FG(), LG(), zG(), VG(), UG(), GG(), qG(), YG(), ZG(), $G(), tK(), rK(), aK(), sK(), lK(), dK(), pK(), hK(), _K(), yK(), xK(), CK(), TK(), DK(), kK(), jK(), NK(), FK(), LK(), zK(), VK(), UK(), GK(), qK(), YK(), ZK(), $K(), tq(), rq(), aq(), sq(), lq(), dq(), pq(), hq(), _q(), yq(), xq(), Cq(), Tq(), Dq(), kq(), jq(), Nq(), Fq(), Lq(), zq(), Vq(), Uq(), Gq(), qq(), Yq(), Zq(), $q(), tJ(), rJ(), aJ(), sJ(), lJ(), dJ(), pJ(), hJ(), _J(), yJ(), xJ(), CJ(), TJ(), DJ(), kJ(), jJ(), NJ(), FJ(), LJ(), zJ(), VJ(), UJ(), GJ(), qJ(), YJ(), ZJ(), $J(), tY(), rY(), aY(), sY(), lY(), dY(), pY(), hY(), _Y(), yY(), xY(), CY(), TY(), DY(), kY(), jY(), NY(), FY(), LY(), zY(), VY(), UY(), GY(), qY(), YY(), ZY(), $Y(), tX(), rX(), aX(), sX(), lX(), dX(), pX(), hX(), _X(), yX(), xX(), CX(), TX(), DX(), kX(), jX(), NX(), FX(), LX(), zX(), VX(), UX(), GX(), qX(), YX(), ZX(), $X(), tZ(), rZ(), aZ(), sZ(), lZ(), dZ(), pZ(), hZ(), _Z(), yZ(), xZ(), CZ(), TZ(), DZ(), kZ(), jZ(), NZ(), FZ(), LZ(), zZ(), VZ(), UZ(), GZ(), qZ(), YZ(), ZZ(), $Z(), tQ(), rQ(), aQ(), sQ(), lQ(), dQ(), pQ(), hQ(), _Q(), yQ(), xQ(), CQ(), TQ(), DQ(), kQ(), jQ(), NQ(), FQ(), LQ(), zQ(), VQ(), UQ(), GQ(), qQ(), YQ(), ZQ(), $Q(), t$(), r$(), a$(), s$(), l$(), d$(), p$(), h$(), _$(), y$(), x$(), C$(), T$(), D$(), k$(), j$(), N$(), F$(), L$(), z$(), V$(), U$(), G$(), q$(), Y$(), Z$(), $$(), t1(), r1(), a1(), s1(), l1(), d1(), p1(), h1(), _1(), y1(), x1(), C1(), T1(), D1();
})), X, A1 = o((() => {
	(function(e) {
		e[e.STANDARD = 16] = "STANDARD", e[e.LARGE = 20] = "LARGE";
	})(X ||= {});
})), j1 = /* @__PURE__ */ c({
	IconSvgPaths16: () => vO,
	IconSvgPaths20: () => O1,
	getIconPaths: () => M1,
	iconNameToPathsRecordKey: () => N1
});
function M1(e, t) {
	let n = mn(e);
	return t === X.STANDARD ? vO[n] : O1[n];
}
function N1(e) {
	return mn(e);
}
var P1 = o((() => {
	Dn(), yO(), k1(), A1();
})), Z;
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/iconNames.js
(function(e) {
	e.AddApplication = "add-application", e.AddChild = "add-child", e.AddClip = "add-clip", e.AddColumnLeft = "add-column-left", e.AddColumnRight = "add-column-right", e.AddDerivedColumn = "add-derived-column", e.AddLocation = "add-location", e.AddParent = "add-parent", e.AddRowBottom = "add-row-bottom", e.AddRowTop = "add-row-top", e.AddTile = "add-tile", e.AddToArtifact = "add-to-artifact", e.AddToFolder = "add-to-folder", e.Add = "add", e.AimpointsTarget = "aimpoints-target", e.Airplane = "airplane", e.AlignCenter = "align-center", e.AlignJustify = "align-justify", e.AlignLeft = "align-left", e.AlignRight = "align-right", e.AlignmentBottom = "alignment-bottom", e.AlignmentHorizontalCenter = "alignment-horizontal-center", e.AlignmentLeft = "alignment-left", e.AlignmentRight = "alignment-right", e.AlignmentTop = "alignment-top", e.AlignmentVerticalCenter = "alignment-vertical-center", e.Ammunition = "ammunition", e.Anchor = "anchor", e.Annotation = "annotation", e.Announcement = "announcement", e.Antenna = "antenna", e.AppHeader = "app-header", e.Application = "application", e.Applications = "applications", e.Archive = "archive", e.AreaOfInterest = "area-of-interest", e.ArrayBoolean = "array-boolean", e.ArrayDate = "array-date", e.ArrayFloatingPoint = "array-floating-point", e.ArrayNumeric = "array-numeric", e.ArrayObject = "array-object", e.ArrayString = "array-string", e.ArrayTimestamp = "array-timestamp", e.Array = "array", e.ArrowBottomLeft = "arrow-bottom-left", e.ArrowBottomRight = "arrow-bottom-right", e.ArrowDown = "arrow-down", e.ArrowLeft = "arrow-left", e.ArrowRight = "arrow-right", e.ArrowTopLeft = "arrow-top-left", e.ArrowTopRight = "arrow-top-right", e.ArrowUp = "arrow-up", e.ArrowsArc = "arrows-arc", e.ArrowsHorizontal = "arrows-horizontal", e.ArrowsVertical = "arrows-vertical", e.Asterisk = "asterisk", e.At = "at", e.AutomaticUpdates = "automatic-updates", e.Axle = "axle", e.Backlink = "backlink", e.BackwardTen = "backward-ten", e.Badge = "badge", e.BanCircle = "ban-circle", e.BankAccount = "bank-account", e.Barcode = "barcode", e.BinaryNumber = "binary-number", e.Blank = "blank", e.BlockPromote = "block-promote", e.BlockedPerson = "blocked-person", e.Bold = "bold", e.Book = "book", e.Bookmark = "bookmark", e.Box = "box", e.BranchLocked = "branch-locked", e.BranchUnlocked = "branch-unlocked", e.Briefcase = "briefcase", e.BringData = "bring-data", e.BringForward = "bring-forward", e.BritishPound = "british-pound", e.Bug = "bug", e.Buggy = "buggy", e.Build = "build", e.Bullseye = "bullseye", e.Calculator = "calculator", e.Calendar = "calendar", e.Camera = "camera", e.CaretDown = "caret-down", e.CaretLeft = "caret-left", e.CaretRight = "caret-right", e.CaretUp = "caret-up", e.CargoShip = "cargo-ship", e.CellTower = "cell-tower", e.Changes = "changes", e.Chart = "chart", e.Chat = "chat", e.ChevronBackward = "chevron-backward", e.ChevronDown = "chevron-down", e.ChevronForward = "chevron-forward", e.ChevronLeft = "chevron-left", e.ChevronRight = "chevron-right", e.ChevronUp = "chevron-up", e.CircleArrowDown = "circle-arrow-down", e.CircleArrowLeft = "circle-arrow-left", e.CircleArrowRight = "circle-arrow-right", e.CircleArrowUp = "circle-arrow-up", e.CircleDashed = "circle-dashed", e.Circle = "circle", e.Citation = "citation", e.Clean = "clean", e.Clip = "clip", e.ClipboardFile = "clipboard-file", e.Clipboard = "clipboard", e.CloudDownload = "cloud-download", e.CloudServer = "cloud-server", e.CloudTick = "cloud-tick", e.CloudUpload = "cloud-upload", e.Cloud = "cloud", e.CodeBlock = "code-block", e.Code = "code", e.Cog = "cog", e.CollapseAll = "collapse-all", e.ColorFill = "color-fill", e.ColumnLayout = "column-layout", e.Comment = "comment", e.Comparison = "comparison", e.Compass = "compass", e.Compressed = "compressed", e.Confirm = "confirm", e.ConsoleAlert = "console-alert", e.Console = "console", e.Construction = "construction", e.Contrast = "contrast", e.Control = "control", e.CreditCard = "credit-card", e.Crop = "crop", e.CrossCircle = "cross-circle", e.Cross = "cross", e.Crown = "crown", e.CrystalBall = "crystal-ball", e.CssStyle = "css-style", e.CubeAdd = "cube-add", e.CubeCutout = "cube-cutout", e.CubeCutouts = "cube-cutouts", e.CubeEdit = "cube-edit", e.CubeRemove = "cube-remove", e.Cube = "cube", e.Cubes = "cubes", e.CurlyBraces = "curly-braces", e.CurvedRangeChart = "curved-range-chart", e.Cut = "cut", e.Cycle = "cycle", e.Dashboard = "dashboard", e.DataCloud = "data-cloud", e.DataConnection = "data-connection", e.DataLineage = "data-lineage", e.DataSearch = "data-search", e.DataSync = "data-sync", e.Database = "database", e.DeleteClip = "delete-clip", e.Delete = "delete", e.Delta = "delta", e.DeriveColumn = "derive-column", e.Descendant = "descendant", e.Desktop = "desktop", e.Detection = "detection", e.Diagnosis = "diagnosis", e.DiagramTree = "diagram-tree", e.DirectionLeft = "direction-left", e.DirectionRight = "direction-right", e.Disable = "disable", e.Divide = "divide", e.DocumentCode = "document-code", e.DocumentLocked = "document-locked", e.DocumentOpen = "document-open", e.DocumentShare = "document-share", e.Document = "document", e.Dollar = "dollar", e.Dot = "dot", e.DoubleCaretHorizontal = "double-caret-horizontal", e.DoubleCaretVertical = "double-caret-vertical", e.DoubleChevronDown = "double-chevron-down", e.DoubleChevronLeft = "double-chevron-left", e.DoubleChevronRight = "double-chevron-right", e.DoubleChevronUp = "double-chevron-up", e.DoughnutChart = "doughnut-chart", e.Download = "download", e.DragHandleHorizontal = "drag-handle-horizontal", e.DragHandleVertical = "drag-handle-vertical", e.Draw = "draw", e.DrawerLeftFilled = "drawer-left-filled", e.DrawerLeft = "drawer-left", e.DrawerRightFilled = "drawer-right-filled", e.DrawerRight = "drawer-right", e.DriveTime = "drive-time", e.DroneUav = "drone-uav", e.Drone = "drone", e.Duplicate = "duplicate", e.Edit = "edit", e.Eject = "eject", e.Emoji = "emoji", e.Endnote = "endnote", e.Endorsed = "endorsed", e.Engagement = "engagement", e.Envelope = "envelope", e.Equals = "equals", e.Eraser = "eraser", e.Error = "error", e.Euro = "euro", e.Excavator = "excavator", e.Exchange = "exchange", e.ExcludeRow = "exclude-row", e.ExpandAll = "expand-all", e.Explain = "explain", e.Export = "export", e.EyeOff = "eye-off", e.EyeOn = "eye-on", e.EyeOpen = "eye-open", e.FastBackward = "fast-backward", e.FastForward = "fast-forward", e.FeedSubscribed = "feed-subscribed", e.Feed = "feed", e.FighterJet = "fighter-jet", e.Film = "film", e.FilterKeep = "filter-keep", e.FilterList = "filter-list", e.FilterOpen = "filter-open", e.FilterRemove = "filter-remove", e.FilterSortAsc = "filter-sort-asc", e.FilterSortDesc = "filter-sort-desc", e.Filter = "filter", e.Flag = "flag", e.Flame = "flame", e.Flash = "flash", e.FloatingPoint = "floating-point", e.FloppyDisk = "floppy-disk", e.FlowBranch = "flow-branch", e.FlowEnd = "flow-end", e.FlowLinear = "flow-linear", e.FlowReviewBranch = "flow-review-branch", e.FlowReview = "flow-review", e.Flows = "flows", e.FolderClose = "folder-close", e.FolderNew = "folder-new", e.FolderOpen = "folder-open", e.FolderSharedOpen = "folder-shared-open", e.FolderShared = "folder-shared", e.Follower = "follower", e.Following = "following", e.Font = "font", e.ForkEnd = "fork-end", e.Fork = "fork", e.Form = "form", e.ForwardTen = "forward-ten", e.FrameToFrame = "frame-to-frame", e.Fuel = "fuel", e.FullCircle = "full-circle", e.FullStackedChart = "full-stacked-chart", e.Fullscreen = "fullscreen", e.FunctionMinimal = "function-minimal", e.Function = "function", e.GanttChart = "gantt-chart", e.Generate = "generate", e.Geofence = "geofence", e.Geolocation = "geolocation", e.Geosearch = "geosearch", e.Geotime = "geotime", e.GiftBox = "gift-box", e.GitBranch = "git-branch", e.GitCommit = "git-commit", e.GitMerge = "git-merge", e.GitNewBranch = "git-new-branch", e.GitPull = "git-pull", e.GitPush = "git-push", e.GitRebase = "git-rebase", e.GitRepo = "git-repo", e.Glass = "glass", e.GlobeNetworkAdd = "globe-network-add", e.GlobeNetwork = "globe-network", e.Globe = "globe", e.GraphRemove = "graph-remove", e.Graph = "graph", e.GreaterThanOrEqualTo = "greater-than-or-equal-to", e.GreaterThan = "greater-than", e.GridView = "grid-view", e.Grid = "grid", e.GroupItem = "group-item", e.GroupObjects = "group-objects", e.GroupedBarChart = "grouped-bar-chart", e.HandDown = "hand-down", e.HandLeft = "hand-left", e.HandRight = "hand-right", e.HandUp = "hand-up", e.Hand = "hand", e.Hat = "hat", e.HeaderOne = "header-one", e.HeaderThree = "header-three", e.HeaderTwo = "header-two", e.Header = "header", e.Headset = "headset", e.HeartBroken = "heart-broken", e.Heart = "heart", e.HeatGrid = "heat-grid", e.Heatmap = "heatmap", e.Helicopter = "helicopter", e.Help = "help", e.HelperManagement = "helper-management", e.Hexagon = "hexagon", e.HighPriority = "high-priority", e.HighVoltagePole = "high-voltage-pole", e.Highlight = "highlight", e.History = "history", e.Home = "home", e.HorizontalBarChartAsc = "horizontal-bar-chart-asc", e.HorizontalBarChartDesc = "horizontal-bar-chart-desc", e.HorizontalBarChart = "horizontal-bar-chart", e.HorizontalDistribution = "horizontal-distribution", e.HorizontalInbetween = "horizontal-inbetween", e.Hurricane = "hurricane", e.IdNumber = "id-number", e.ImageRotateLeft = "image-rotate-left", e.ImageRotateRight = "image-rotate-right", e.Import = "import", e.InboxFiltered = "inbox-filtered", e.InboxGeo = "inbox-geo", e.InboxSearch = "inbox-search", e.InboxUpdate = "inbox-update", e.Inbox = "inbox", e.InfoSign = "info-sign", e.Inheritance = "inheritance", e.InheritedGroup = "inherited-group", e.InnerJoin = "inner-join", e.Input = "input", e.Insert = "insert", e.Intelligence = "intelligence", e.Intersection = "intersection", e.IpAddress = "ip-address", e.IssueClosed = "issue-closed", e.IssueNew = "issue-new", e.Issue = "issue", e.Italic = "italic", e.JoinTable = "join-table", e.KeyBackspace = "key-backspace", e.KeyCommand = "key-command", e.KeyControl = "key-control", e.KeyDelete = "key-delete", e.KeyEnter = "key-enter", e.KeyEscape = "key-escape", e.KeyOption = "key-option", e.KeyShift = "key-shift", e.KeyTab = "key-tab", e.Key = "key", e.KnownVehicle = "known-vehicle", e.LabTest = "lab-test", e.Label = "label", e.LayerOutline = "layer-outline", e.Layer = "layer", e.Layers = "layers", e.LayoutAuto = "layout-auto", e.LayoutBalloon = "layout-balloon", e.LayoutBottomRowThreeTiles = "layout-bottom-row-three-tiles", e.LayoutBottomRowTwoTiles = "layout-bottom-row-two-tiles", e.LayoutCircle = "layout-circle", e.LayoutGrid = "layout-grid", e.LayoutGroupBy = "layout-group-by", e.LayoutHierarchy = "layout-hierarchy", e.LayoutLeftColumnThreeTiles = "layout-left-column-three-tiles", e.LayoutLeftColumnTwoTiles = "layout-left-column-two-tiles", e.LayoutLinear = "layout-linear", e.LayoutRightColumnThreeTiles = "layout-right-column-three-tiles", e.LayoutRightColumnTwoTiles = "layout-right-column-two-tiles", e.LayoutSkewGrid = "layout-skew-grid", e.LayoutSortedClusters = "layout-sorted-clusters", e.LayoutThreeColumns = "layout-three-columns", e.LayoutThreeRows = "layout-three-rows", e.LayoutTopRowThreeTiles = "layout-top-row-three-tiles", e.LayoutTopRowTwoTiles = "layout-top-row-two-tiles", e.LayoutTwoColumns = "layout-two-columns", e.LayoutTwoRows = "layout-two-rows", e.Layout = "layout", e.Learning = "learning", e.LeftJoin = "left-join", e.LengthenText = "lengthen-text", e.LessThanOrEqualTo = "less-than-or-equal-to", e.LessThan = "less-than", e.Lifesaver = "lifesaver", e.Lightbulb = "lightbulb", e.Lightning = "lightning", e.Link = "link", e.LinkedSquares = "linked-squares", e.ListColumns = "list-columns", e.ListDetailView = "list-detail-view", e.List = "list", e.Locate = "locate", e.Lock = "lock", e.Locomotive = "locomotive", e.LogIn = "log-in", e.LogOut = "log-out", e.LowVoltagePole = "low-voltage-pole", e.Manual = "manual", e.ManuallyEnteredData = "manually-entered-data", e.ManyToMany = "many-to-many", e.ManyToOne = "many-to-one", e.MapCreate = "map-create", e.MapMarker = "map-marker", e.Map = "map", e.Markdown = "markdown", e.Maximize = "maximize", e.Media = "media", e.MenuClosed = "menu-closed", e.MenuOpen = "menu-open", e.Menu = "menu", e.MergeColumns = "merge-columns", e.MergeLinks = "merge-links", e.Microphone = "microphone", e.Minimize = "minimize", e.Minus = "minus", e.MobilePhone = "mobile-phone", e.MobileVideo = "mobile-video", e.ModalFilled = "modal-filled", e.Modal = "modal", e.Model = "model", e.Moon = "moon", e.More = "more", e.Mountain = "mountain", e.Move = "move", e.Mugshot = "mugshot", e.MultiSelect = "multi-select", e.Music = "music", e.Nest = "nest", e.NewComment = "new-comment", e.NewDrawing = "new-drawing", e.NewGridItem = "new-grid-item", e.NewLayer = "new-layer", e.NewLayers = "new-layers", e.NewLink = "new-link", e.NewObject = "new-object", e.NewPerson = "new-person", e.NewPrescription = "new-prescription", e.NewShield = "new-shield", e.NewTextBox = "new-text-box", e.Ninja = "ninja", e.NotEqualTo = "not-equal-to", e.NotificationsAdd = "notifications-add", e.NotificationsSnooze = "notifications-snooze", e.NotificationsUpdated = "notifications-updated", e.Notifications = "notifications", e.NumberedList = "numbered-list", e.Numerical = "numerical", e.ObjectView = "object-view", e.Office = "office", e.Offline = "offline", e.OilField = "oil-field", e.OneColumn = "one-column", e.OneToMany = "one-to-many", e.OneToOne = "one-to-one", e.OpenApplication = "open-application", e.Outdated = "outdated", e.OuterJoin = "outer-join", e.Output = "output", e.Package = "package", e.PageBreak = "page-break", e.PageLayout = "page-layout", e.PanelStats = "panel-stats", e.PanelTable = "panel-table", e.Panel = "panel", e.Paperclip = "paperclip", e.Paragraph = "paragraph", e.PasteVariable = "paste-variable", e.PathSearch = "path-search", e.Path = "path", e.Pause = "pause", e.People = "people", e.Percentage = "percentage", e.Person = "person", e.PhoneCall = "phone-call", e.PhoneForward = "phone-forward", e.PhoneSearch = "phone-search", e.Phone = "phone", e.PieChart = "pie-chart", e.Pill = "pill", e.Pin = "pin", e.Pistol = "pistol", e.PivotTable = "pivot-table", e.Pivot = "pivot", e.Play = "play", e.Playbook = "playbook", e.Plus = "plus", e.PolygonFilter = "polygon-filter", e.Popout = "popout", e.Power = "power", e.PredictiveAnalysis = "predictive-analysis", e.Prescription = "prescription", e.Presentation = "presentation", e.Print = "print", e.Projects = "projects", e.Properties = "properties", e.Property = "property", e.PublishFunction = "publish-function", e.Pulse = "pulse", e.Rain = "rain", e.Random = "random", e.RangeRing = "range-ring", e.Record = "record", e.RectHeight = "rect-height", e.RectWidth = "rect-width", e.Rectangle = "rectangle", e.Redo = "redo", e.RefreshOff = "refresh-off", e.Refresh = "refresh", e.Regex = "regex", e.RegressionChart = "regression-chart", e.RemoveColumnLeft = "remove-column-left", e.RemoveColumnRight = "remove-column-right", e.RemoveColumn = "remove-column", e.RemoveRowBottom = "remove-row-bottom", e.RemoveRowTop = "remove-row-top", e.Remove = "remove", e.Repeat = "repeat", e.Reset = "reset", e.Resolve = "resolve", e.Rig = "rig", e.RightJoin = "right-join", e.Ring = "ring", e.RocketSlant = "rocket-slant", e.Rocket = "rocket", e.RootFolder = "root-folder", e.RotateCcw = "rotate-ccw", e.RotateCw = "rotate-cw", e.RotateDocument = "rotate-document", e.RotatePage = "rotate-page", e.Route = "route", e.RunHistory = "run-history", e.Satellite = "satellite", e.Saved = "saved", e.ScatterPlot = "scatter-plot", e.SearchAround = "search-around", e.SearchTemplate = "search-template", e.SearchText = "search-text", e.Search = "search", e.SegmentedControl = "segmented-control", e.Select = "select", e.SelectionBoxAdd = "selection-box-add", e.SelectionBoxEdit = "selection-box-edit", e.SelectionBoxRemove = "selection-box-remove", e.SelectionBox = "selection-box", e.Selection = "selection", e.SendBackward = "send-backward", e.SendMessage = "send-message", e.SendToGraph = "send-to-graph", e.SendToMap = "send-to-map", e.SendTo = "send-to", e.Sensor = "sensor", e.SeriesAdd = "series-add", e.SeriesConfiguration = "series-configuration", e.SeriesDerived = "series-derived", e.SeriesFiltered = "series-filtered", e.SeriesSearch = "series-search", e.ServerInstall = "server-install", e.Server = "server", e.Settings = "settings", e.Shapes = "shapes", e.Share = "share", e.SharedFilter = "shared-filter", e.Shield = "shield", e.Ship = "ship", e.Shop = "shop", e.ShoppingCart = "shopping-cart", e.ShortenText = "shorten-text", e.SignalSearch = "signal-search", e.SimCard = "sim-card", e.Slash = "slash", e.SmallCross = "small-cross", e.SmallInfoSign = "small-info-sign", e.SmallMinus = "small-minus", e.SmallPlus = "small-plus", e.SmallSquare = "small-square", e.SmallTick = "small-tick", e.Snowflake = "snowflake", e.SoccerBall = "soccer-ball", e.SocialMedia = "social-media", e.SortAlphabeticalDesc = "sort-alphabetical-desc", e.SortAlphabetical = "sort-alphabetical", e.SortAsc = "sort-asc", e.SortDesc = "sort-desc", e.SortNumericalDesc = "sort-numerical-desc", e.SortNumerical = "sort-numerical", e.Sort = "sort", e.SpellCheck = "spell-check", e.Spin = "spin", e.SplitColumns = "split-columns", e.SportsStadium = "sports-stadium", e.Square = "square", e.StackedChart = "stacked-chart", e.StadiumGeometry = "stadium-geometry", e.StarEmpty = "star-empty", e.Star = "star", e.StepBackward = "step-backward", e.StepChart = "step-chart", e.StepForward = "step-forward", e.Stop = "stop", e.Stopwatch = "stopwatch", e.Strikethrough = "strikethrough", e.Style = "style", e.Subscript = "subscript", e.SubtractRightJoin = "subtract-right-join", e.Superscript = "superscript", e.SwapHorizontal = "swap-horizontal", e.SwapVertical = "swap-vertical", e.Sweep = "sweep", e.Switch = "switch", e.SymbolCircle = "symbol-circle", e.SymbolCross = "symbol-cross", e.SymbolDiamond = "symbol-diamond", e.SymbolRectangle = "symbol-rectangle", e.SymbolSquare = "symbol-square", e.SymbolTriangleDown = "symbol-triangle-down", e.SymbolTriangleUp = "symbol-triangle-up", e.Syringe = "syringe", e.TableSync = "table-sync", e.TagAdd = "tag-add", e.TagPromote = "tag-promote", e.TagRefresh = "tag-refresh", e.TagUndo = "tag-undo", e.Tag = "tag", e.Tags = "tags", e.TakeAction = "take-action", e.Tank = "tank", e.Target = "target", e.Taxi = "taxi", e.Team = "team", e.Temperature = "temperature", e.TextHighlight = "text-highlight", e.ThAdd = "th-add", e.ThDerived = "th-derived", e.ThDisconnect = "th-disconnect", e.ThFiltered = "th-filtered", e.ThListAdd = "th-list-add", e.ThList = "th-list", e.ThVirtualAdd = "th-virtual-add", e.ThVirtual = "th-virtual", e.Th = "th", e.ThirdParty = "third-party", e.ThumbsDown = "thumbs-down", e.ThumbsUp = "thumbs-up", e.TickCircle = "tick-circle", e.Tick = "tick", e.Time = "time", e.TimelineAreaChart = "timeline-area-chart", e.TimelineBarChart = "timeline-bar-chart", e.TimelineEvents = "timeline-events", e.TimelineLineChart = "timeline-line-chart", e.Tint = "tint", e.Torch = "torch", e.Tractor = "tractor", e.Train = "train", e.Translate = "translate", e.Trash = "trash", e.Tree = "tree", e.TrendingDown = "trending-down", e.TrendingUp = "trending-up", e.Trophy = "trophy", e.Truck = "truck", e.TwoColumns = "two-columns", e.Unarchive = "unarchive", e.Underline = "underline", e.Undo = "undo", e.UngroupObjects = "ungroup-objects", e.UnknownVehicle = "unknown-vehicle", e.Unlink = "unlink", e.Unlock = "unlock", e.Unpin = "unpin", e.Unresolve = "unresolve", e.Updated = "updated", e.Upload = "upload", e.User = "user", e.VariableLayer = "variable-layer", e.Variable = "variable", e.Vector = "vector", e.VerticalBarChartAsc = "vertical-bar-chart-asc", e.VerticalBarChartDesc = "vertical-bar-chart-desc", e.VerticalDistribution = "vertical-distribution", e.VerticalInbetween = "vertical-inbetween", e.Video = "video", e.Virus = "virus", e.VolumeDown = "volume-down", e.VolumeOff = "volume-off", e.VolumeUp = "volume-up", e.Walk = "walk", e.WarningSign = "warning-sign", e.WaterfallChart = "waterfall-chart", e.Waves = "waves", e.WidgetButton = "widget-button", e.WidgetFooter = "widget-footer", e.WidgetHeader = "widget-header", e.Widget = "widget", e.Wind = "wind", e.Won = "won", e.WrapLines = "wrap-lines", e.WrenchRedo = "wrench-redo", e.WrenchSnooze = "wrench-snooze", e.WrenchTime = "wrench-time", e.Wrench = "wrench", e.Yen = "yen", e.ZoomIn = "zoom-in", e.ZoomOut = "zoom-out", e.ZoomToFit = "zoom-to-fit";
})(Z ||= {}), Z.AddApplication, Z.AddChild, Z.AddClip, Z.AddColumnLeft, Z.AddColumnRight, Z.AddDerivedColumn, Z.AddLocation, Z.AddParent, Z.AddRowBottom, Z.AddRowTop, Z.AddTile, Z.AddToArtifact, Z.AddToFolder, Z.Add, Z.AimpointsTarget, Z.Airplane, Z.AlignCenter, Z.AlignJustify, Z.AlignLeft, Z.AlignRight, Z.AlignmentBottom, Z.AlignmentHorizontalCenter, Z.AlignmentLeft, Z.AlignmentRight, Z.AlignmentTop, Z.AlignmentVerticalCenter, Z.Ammunition, Z.Anchor, Z.Annotation, Z.Announcement, Z.Antenna, Z.AppHeader, Z.Application, Z.Applications, Z.Archive, Z.AreaOfInterest, Z.ArrayBoolean, Z.ArrayDate, Z.ArrayFloatingPoint, Z.ArrayNumeric, Z.ArrayObject, Z.ArrayString, Z.ArrayTimestamp, Z.Array, Z.ArrowBottomLeft, Z.ArrowBottomRight, Z.ArrowDown, Z.ArrowLeft, Z.ArrowRight, Z.ArrowTopLeft, Z.ArrowTopRight, Z.ArrowUp, Z.ArrowsArc, Z.ArrowsHorizontal, Z.ArrowsVertical, Z.Asterisk, Z.At, Z.AutomaticUpdates, Z.Axle, Z.Backlink, Z.BackwardTen, Z.Badge, Z.BanCircle, Z.BankAccount, Z.Barcode, Z.BinaryNumber, Z.Blank, Z.BlockPromote, Z.BlockedPerson, Z.Bold, Z.Book, Z.Bookmark, Z.Box, Z.BranchLocked, Z.BranchUnlocked, Z.Briefcase, Z.BringData, Z.BringForward, Z.BritishPound, Z.Bug, Z.Buggy, Z.Build, Z.Bullseye, Z.Calculator, Z.Calendar, Z.Camera, Z.CaretDown, Z.CaretLeft, Z.CaretRight, Z.CaretUp, Z.CargoShip, Z.CellTower, Z.Changes, Z.Chart, Z.Chat, Z.ChevronBackward, Z.ChevronDown, Z.ChevronForward, Z.ChevronLeft, Z.ChevronRight, Z.ChevronUp, Z.CircleArrowDown, Z.CircleArrowLeft, Z.CircleArrowRight, Z.CircleArrowUp, Z.CircleDashed, Z.Circle, Z.Citation, Z.Clean, Z.Clip, Z.ClipboardFile, Z.Clipboard, Z.CloudDownload, Z.CloudServer, Z.CloudTick, Z.CloudUpload, Z.Cloud, Z.CodeBlock, Z.Code, Z.Cog, Z.CollapseAll, Z.ColorFill, Z.ColumnLayout, Z.Comment, Z.Comparison, Z.Compass, Z.Compressed, Z.Confirm, Z.ConsoleAlert, Z.Console, Z.Construction, Z.Contrast, Z.Control, Z.CreditCard, Z.Crop, Z.CrossCircle, Z.Cross, Z.Crown, Z.CrystalBall, Z.CssStyle, Z.CubeAdd, Z.CubeCutout, Z.CubeCutouts, Z.CubeEdit, Z.CubeRemove, Z.Cube, Z.Cubes, Z.CurlyBraces, Z.CurvedRangeChart, Z.Cut, Z.Cycle, Z.Dashboard, Z.DataCloud, Z.DataConnection, Z.DataLineage, Z.DataSearch, Z.DataSync, Z.Database, Z.DeleteClip, Z.Delete, Z.Delta, Z.DeriveColumn, Z.Descendant, Z.Desktop, Z.Detection, Z.Diagnosis, Z.DiagramTree, Z.DirectionLeft, Z.DirectionRight, Z.Disable, Z.Divide, Z.DocumentCode, Z.DocumentLocked, Z.DocumentOpen, Z.DocumentShare, Z.Document, Z.Dollar, Z.Dot, Z.DoubleCaretHorizontal, Z.DoubleCaretVertical, Z.DoubleChevronDown, Z.DoubleChevronLeft, Z.DoubleChevronRight, Z.DoubleChevronUp, Z.DoughnutChart, Z.Download, Z.DragHandleHorizontal, Z.DragHandleVertical, Z.Draw, Z.DrawerLeftFilled, Z.DrawerLeft, Z.DrawerRightFilled, Z.DrawerRight, Z.DriveTime, Z.DroneUav, Z.Drone, Z.Duplicate, Z.Edit, Z.Eject, Z.Emoji, Z.Endnote, Z.Endorsed, Z.Engagement, Z.Envelope, Z.Equals, Z.Eraser, Z.Error, Z.Euro, Z.Excavator, Z.Exchange, Z.ExcludeRow, Z.ExpandAll, Z.Explain, Z.Export, Z.EyeOff, Z.EyeOn, Z.EyeOpen, Z.FastBackward, Z.FastForward, Z.FeedSubscribed, Z.Feed, Z.FighterJet, Z.Film, Z.FilterKeep, Z.FilterList, Z.FilterOpen, Z.FilterRemove, Z.FilterSortAsc, Z.FilterSortDesc, Z.Filter, Z.Flag, Z.Flame, Z.Flash, Z.FloatingPoint, Z.FloppyDisk, Z.FlowBranch, Z.FlowEnd, Z.FlowLinear, Z.FlowReviewBranch, Z.FlowReview, Z.Flows, Z.FolderClose, Z.FolderNew, Z.FolderOpen, Z.FolderSharedOpen, Z.FolderShared, Z.Follower, Z.Following, Z.Font, Z.ForkEnd, Z.Fork, Z.Form, Z.ForwardTen, Z.FrameToFrame, Z.Fuel, Z.FullCircle, Z.FullStackedChart, Z.Fullscreen, Z.FunctionMinimal, Z.Function, Z.GanttChart, Z.Generate, Z.Geofence, Z.Geolocation, Z.Geosearch, Z.Geotime, Z.GiftBox, Z.GitBranch, Z.GitCommit, Z.GitMerge, Z.GitNewBranch, Z.GitPull, Z.GitPush, Z.GitRebase, Z.GitRepo, Z.Glass, Z.GlobeNetworkAdd, Z.GlobeNetwork, Z.Globe, Z.GraphRemove, Z.Graph, Z.GreaterThanOrEqualTo, Z.GreaterThan, Z.GridView, Z.Grid, Z.GroupItem, Z.GroupObjects, Z.GroupedBarChart, Z.HandDown, Z.HandLeft, Z.HandRight, Z.HandUp, Z.Hand, Z.Hat, Z.HeaderOne, Z.HeaderThree, Z.HeaderTwo, Z.Header, Z.Headset, Z.HeartBroken, Z.Heart, Z.HeatGrid, Z.Heatmap, Z.Helicopter, Z.Help, Z.HelperManagement, Z.Hexagon, Z.HighPriority, Z.HighVoltagePole, Z.Highlight, Z.History, Z.Home, Z.HorizontalBarChartAsc, Z.HorizontalBarChartDesc, Z.HorizontalBarChart, Z.HorizontalDistribution, Z.HorizontalInbetween, Z.Hurricane, Z.IdNumber, Z.ImageRotateLeft, Z.ImageRotateRight, Z.Import, Z.InboxFiltered, Z.InboxGeo, Z.InboxSearch, Z.InboxUpdate, Z.Inbox, Z.InfoSign, Z.Inheritance, Z.InheritedGroup, Z.InnerJoin, Z.Input, Z.Insert, Z.Intelligence, Z.Intersection, Z.IpAddress, Z.IssueClosed, Z.IssueNew, Z.Issue, Z.Italic, Z.JoinTable, Z.KeyBackspace, Z.KeyCommand, Z.KeyControl, Z.KeyDelete, Z.KeyEnter, Z.KeyEscape, Z.KeyOption, Z.KeyShift, Z.KeyTab, Z.Key, Z.KnownVehicle, Z.LabTest, Z.Label, Z.LayerOutline, Z.Layer, Z.Layers, Z.LayoutAuto, Z.LayoutBalloon, Z.LayoutBottomRowThreeTiles, Z.LayoutBottomRowTwoTiles, Z.LayoutCircle, Z.LayoutGrid, Z.LayoutGroupBy, Z.LayoutHierarchy, Z.LayoutLeftColumnThreeTiles, Z.LayoutLeftColumnTwoTiles, Z.LayoutLinear, Z.LayoutRightColumnThreeTiles, Z.LayoutRightColumnTwoTiles, Z.LayoutSkewGrid, Z.LayoutSortedClusters, Z.LayoutThreeColumns, Z.LayoutThreeRows, Z.LayoutTopRowThreeTiles, Z.LayoutTopRowTwoTiles, Z.LayoutTwoColumns, Z.LayoutTwoRows, Z.Layout, Z.Learning, Z.LeftJoin, Z.LengthenText, Z.LessThanOrEqualTo, Z.LessThan, Z.Lifesaver, Z.Lightbulb, Z.Lightning, Z.Link, Z.LinkedSquares, Z.ListColumns, Z.ListDetailView, Z.List, Z.Locate, Z.Lock, Z.Locomotive, Z.LogIn, Z.LogOut, Z.LowVoltagePole, Z.Manual, Z.ManuallyEnteredData, Z.ManyToMany, Z.ManyToOne, Z.MapCreate, Z.MapMarker, Z.Map, Z.Markdown, Z.Maximize, Z.Media, Z.MenuClosed, Z.MenuOpen, Z.Menu, Z.MergeColumns, Z.MergeLinks, Z.Microphone, Z.Minimize, Z.Minus, Z.MobilePhone, Z.MobileVideo, Z.ModalFilled, Z.Modal, Z.Model, Z.Moon, Z.More, Z.Mountain, Z.Move, Z.Mugshot, Z.MultiSelect, Z.Music, Z.Nest, Z.NewComment, Z.NewDrawing, Z.NewGridItem, Z.NewLayer, Z.NewLayers, Z.NewLink, Z.NewObject, Z.NewPerson, Z.NewPrescription, Z.NewShield, Z.NewTextBox, Z.Ninja, Z.NotEqualTo, Z.NotificationsAdd, Z.NotificationsSnooze, Z.NotificationsUpdated, Z.Notifications, Z.NumberedList, Z.Numerical, Z.ObjectView, Z.Office, Z.Offline, Z.OilField, Z.OneColumn, Z.OneToMany, Z.OneToOne, Z.OpenApplication, Z.Outdated, Z.OuterJoin, Z.Output, Z.Package, Z.PageBreak, Z.PageLayout, Z.PanelStats, Z.PanelTable, Z.Panel, Z.Paperclip, Z.Paragraph, Z.PasteVariable, Z.PathSearch, Z.Path, Z.Pause, Z.People, Z.Percentage, Z.Person, Z.PhoneCall, Z.PhoneForward, Z.PhoneSearch, Z.Phone, Z.PieChart, Z.Pill, Z.Pin, Z.Pistol, Z.PivotTable, Z.Pivot, Z.Play, Z.Playbook, Z.Plus, Z.PolygonFilter, Z.Popout, Z.Power, Z.PredictiveAnalysis, Z.Prescription, Z.Presentation, Z.Print, Z.Projects, Z.Properties, Z.Property, Z.PublishFunction, Z.Pulse, Z.Rain, Z.Random, Z.RangeRing, Z.Record, Z.RectHeight, Z.RectWidth, Z.Rectangle, Z.Redo, Z.RefreshOff, Z.Refresh, Z.Regex, Z.RegressionChart, Z.RemoveColumnLeft, Z.RemoveColumnRight, Z.RemoveColumn, Z.RemoveRowBottom, Z.RemoveRowTop, Z.Remove, Z.Repeat, Z.Reset, Z.Resolve, Z.Rig, Z.RightJoin, Z.Ring, Z.RocketSlant, Z.Rocket, Z.RootFolder, Z.RotateCcw, Z.RotateCw, Z.RotateDocument, Z.RotatePage, Z.Route, Z.RunHistory, Z.Satellite, Z.Saved, Z.ScatterPlot, Z.SearchAround, Z.SearchTemplate, Z.SearchText, Z.Search, Z.SegmentedControl, Z.Select, Z.SelectionBoxAdd, Z.SelectionBoxEdit, Z.SelectionBoxRemove, Z.SelectionBox, Z.Selection, Z.SendBackward, Z.SendMessage, Z.SendToGraph, Z.SendToMap, Z.SendTo, Z.Sensor, Z.SeriesAdd, Z.SeriesConfiguration, Z.SeriesDerived, Z.SeriesFiltered, Z.SeriesSearch, Z.ServerInstall, Z.Server, Z.Settings, Z.Shapes, Z.Share, Z.SharedFilter, Z.Shield, Z.Ship, Z.Shop, Z.ShoppingCart, Z.ShortenText, Z.SignalSearch, Z.SimCard, Z.Slash, Z.SmallCross, Z.SmallInfoSign, Z.SmallMinus, Z.SmallPlus, Z.SmallSquare, Z.SmallTick, Z.Snowflake, Z.SoccerBall, Z.SocialMedia, Z.SortAlphabeticalDesc, Z.SortAlphabetical, Z.SortAsc, Z.SortDesc, Z.SortNumericalDesc, Z.SortNumerical, Z.Sort, Z.SpellCheck, Z.Spin, Z.SplitColumns, Z.SportsStadium, Z.Square, Z.StackedChart, Z.StadiumGeometry, Z.StarEmpty, Z.Star, Z.StepBackward, Z.StepChart, Z.StepForward, Z.Stop, Z.Stopwatch, Z.Strikethrough, Z.Style, Z.Subscript, Z.SubtractRightJoin, Z.Superscript, Z.SwapHorizontal, Z.SwapVertical, Z.Sweep, Z.Switch, Z.SymbolCircle, Z.SymbolCross, Z.SymbolDiamond, Z.SymbolRectangle, Z.SymbolSquare, Z.SymbolTriangleDown, Z.SymbolTriangleUp, Z.Syringe, Z.TableSync, Z.TagAdd, Z.TagPromote, Z.TagRefresh, Z.TagUndo, Z.Tag, Z.Tags, Z.TakeAction, Z.Tank, Z.Target, Z.Taxi, Z.Team, Z.Temperature, Z.TextHighlight, Z.ThAdd, Z.ThDerived, Z.ThDisconnect, Z.ThFiltered, Z.ThListAdd, Z.ThList, Z.ThVirtualAdd, Z.ThVirtual, Z.Th, Z.ThirdParty, Z.ThumbsDown, Z.ThumbsUp, Z.TickCircle, Z.Tick, Z.Time, Z.TimelineAreaChart, Z.TimelineBarChart, Z.TimelineEvents, Z.TimelineLineChart, Z.Tint, Z.Torch, Z.Tractor, Z.Train, Z.Translate, Z.Trash, Z.Tree, Z.TrendingDown, Z.TrendingUp, Z.Trophy, Z.Truck, Z.TwoColumns, Z.Unarchive, Z.Underline, Z.Undo, Z.UngroupObjects, Z.UnknownVehicle, Z.Unlink, Z.Unlock, Z.Unpin, Z.Unresolve, Z.Updated, Z.Upload, Z.User, Z.VariableLayer, Z.Variable, Z.Vector, Z.VerticalBarChartAsc, Z.VerticalBarChartDesc, Z.VerticalDistribution, Z.VerticalInbetween, Z.Video, Z.Virus, Z.VolumeDown, Z.VolumeOff, Z.VolumeUp, Z.Walk, Z.WarningSign, Z.WaterfallChart, Z.Waves, Z.WidgetButton, Z.WidgetFooter, Z.WidgetHeader, Z.Widget, Z.Wind, Z.Won, Z.WrapLines, Z.WrenchRedo, Z.WrenchSnooze, Z.WrenchTime, Z.Wrench, Z.Yen, Z.ZoomIn, Z.ZoomOut, Z.ZoomToFit, Dn();
var F1 = {}, I1 = {};
for (let e of Object.values(Z)) F1[mn(e)] = e, I1[Tn(e).toUpperCase()] = e;
var L1 = {
	...F1,
	...I1
}, R1 = new Set(Object.values(L1));
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/loaderUtils.js
function z1(e) {
	return typeof NODE_ENV < "u" && NODE_ENV === e;
}
async function B1(e, t) {
	let n = z1("development") && typeof performance < "u", r;
	if (n && (r = performance.now(), console.info(`Started '${e}'...`)), await t(), n) {
		let t = Math.round(performance.now() - r);
		console.info(`Finished '${e}' in ${t}ms`);
	}
}
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/paths-loaders/allPathsLoader.js
var V1 = /* @__PURE__ */ c({ allPathsLoader: () => H1 }), H1, U1 = o((() => {
	H1 = async (e, t) => {
		let { getIconPaths: n } = await Promise.resolve().then(() => (P1(), j1));
		return n(e, t);
	};
})), W1 = /* @__PURE__ */ c({ splitPathsBySizeLoader: () => G1 }), G1, K1 = o((() => {
	Dn(), A1(), G1 = async (e, t) => {
		let n = mn(e), r;
		return r = t === X.STANDARD ? await Promise.resolve().then(() => (yO(), vO)) : await Promise.resolve().then(() => (k1(), O1)), r[n];
	};
}));
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/iconLoader.js
A1();
async function q1(e) {
	let { loader: t = Y1.defaultLoader } = e;
	return typeof t == "function" ? t : t === "all" ? (await Promise.resolve().then(() => (U1(), V1))).allPathsLoader : (await Promise.resolve().then(() => (K1(), W1))).splitPathsBySizeLoader;
}
var J1 = class {
	defaultLoader = "split-by-size";
	loadedIconPaths16 = /* @__PURE__ */ new Map();
	loadedIconPaths20 = /* @__PURE__ */ new Map();
	static setLoaderOptions(e) {
		e.loader !== void 0 && (Y1.defaultLoader = e.loader);
	}
	static async load(e, t, n) {
		Array.isArray(e) || (e = [e]), await Promise.all(e.map((e) => this.loadImpl(e, t, n)));
	}
	static async loadAll(e) {
		let t = Object.values(L1);
		B1("[Blueprint] loading all icons", async () => {
			await Promise.all([this.load(t, X.STANDARD, e), this.load(t, X.LARGE, e)]);
		});
	}
	static getPaths(e, t) {
		if (this.isValidIconName(e)) return (t < X.LARGE ? Y1.loadedIconPaths16 : Y1.loadedIconPaths20).get(e);
	}
	static async loadImpl(e, t, n = {}) {
		if (!this.isValidIconName(e)) {
			console.error(`[Blueprint] Unknown icon '${e}'`);
			return;
		}
		let r = t < X.LARGE ? Y1.loadedIconPaths16 : Y1.loadedIconPaths20;
		if (r.has(e)) return;
		let i = await q1(n);
		try {
			let n = await i(e, t < X.LARGE ? X.STANDARD : X.LARGE);
			r.set(e, n);
		} catch (n) {
			console.error(`[Blueprint] Unable to load ${t}px icon '${e}'`, n);
		}
	}
	static isValidIconName(e) {
		return R1.has(e);
	}
}, Y1 = new J1(), X1 = "bp6-icon", Z1 = /* @__PURE__ */ new Map();
function Q1(e) {
	let t = Z1.get(e) ?? 0;
	return Z1.set(e, t + 1), `${e}-${t}`;
}
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/svgIconContainer.js
var Q = Qt(), $ = /* @__PURE__ */ u($t());
A1();
var $1 = (0, D.forwardRef)((e, t) => {
	let { children: n, className: r, color: i, htmlTitle: a, iconName: o, size: s = X.STANDARD, svgProps: c, tagName: l = "span", title: u, ...d } = e, f = s >= X.LARGE ? X.LARGE : X.STANDARD, p = `0 0 ${f} ${f}`, m = Q1("iconTitle"), h = {
		fill: i,
		height: s,
		role: "img",
		viewBox: p,
		width: s,
		...c
	};
	return l === null ? (0, Q.jsxs)("svg", {
		"aria-labelledby": u ? m : void 0,
		"data-icon": o,
		ref: t,
		...h,
		...d,
		className: (0, $.default)(r, c?.className),
		children: [u && (0, Q.jsx)("title", {
			id: m,
			children: u
		}), n]
	}) : (0, D.createElement)(l, {
		"aria-hidden": !u || void 0,
		...d,
		className: (0, $.default)(X1, `${X1}-${o}`, r),
		ref: t,
		title: a
	}, (0, Q.jsxs)("svg", {
		"data-icon": o,
		...h,
		className: c?.className,
		children: [u && (0, Q.jsx)("title", { children: u }), n]
	}));
});
//#endregion
//#region node_modules/@blueprintjs/icons/lib/esm/generated/components/small-cross.js
$1.displayName = "Blueprint6.SVGIconContainer", A1();
var e0 = ["m9.41 8 2.29-2.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L8 6.59l-2.29-2.3a1.003 1.003 0 0 0-1.42 1.42L6.59 8 4.3 10.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71L8 9.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"], t0 = ["m11.41 10 3.29-3.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L10 8.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42L8.59 10 5.3 13.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l3.29-3.3 3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"], n0 = D.forwardRef((e, t) => {
	let n = (e.size ?? X.STANDARD) >= X.LARGE ? t0 : e0;
	return (0, Q.jsx)($1, {
		iconName: "small-cross",
		ref: t,
		...e,
		children: n.map((e, t) => (0, Q.jsx)("path", {
			d: e,
			fillRule: "evenodd"
		}, t))
	});
});
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/icon/icon.js
n0.displayName = "Blueprint6.Icon.SmallCrossIcon", A1();
var r0 = (0, D.forwardRef)((e, t) => {
	let { autoLoad: n = !0, className: r, color: i, icon: a, intent: o, tagName: s = "span", svgProps: c, title: l, htmlTitle: u, ...d } = e, f = e.size ?? X.STANDARD, [p, m] = (0, D.useState)(() => typeof a == "string" ? J1.getPaths(a, f) : void 0);
	if ((0, D.useEffect)(() => {
		let e = !1;
		if (typeof a == "string") {
			let t = J1.getPaths(a, f);
			t === void 0 ? n ? J1.load(a, f).then(() => {
				e || m(J1.getPaths(a, f));
			}).catch((e) => {
				console.error(`[Blueprint] Icon '${a}' (${f}px) could not be loaded.`, e);
			}) : console.error(`[Blueprint] Icon '${a}' (${f}px) is not loaded yet and autoLoad={false}, did you call Icons.load('${a}', ${f})?`) : m(t);
		}
		return () => {
			e = !0;
		};
	}, [
		n,
		a,
		f
	]), a == null || typeof a == "boolean") return null;
	if (typeof a != "string") {
		if ((0, D.isValidElement)(a)) {
			let t = (0, $.default)(a.props.className, r, Ct(o));
			if (Gt(a)) {
				let n = { className: t }, r = a.props.size ?? e.size;
				r != null && (n.size = r);
				let o = a.props.color ?? i;
				return o != null && (n.color = o), (0, D.cloneElement)(a, n);
			}
			return (0, D.cloneElement)(a, { className: t });
		}
		return a;
	}
	if (p == null) {
		let e = f === X.STANDARD ? _t : f === X.LARGE ? vt : void 0;
		return (0, D.createElement)(s || "span", {
			"aria-hidden": !l || void 0,
			...Rt(d),
			className: (0, $.default)(gt, e, St(a), Ct(o), r),
			"data-icon": a,
			ref: t,
			title: u
		});
	} else return (0, Q.jsx)($1, {
		children: p.map((e, t) => (0, Q.jsx)("path", {
			d: e,
			fillRule: "evenodd"
		}, t)),
		className: (0, $.default)(Ct(o), r),
		color: i,
		htmlTitle: u,
		iconName: a,
		ref: t,
		size: f,
		svgProps: c,
		tagName: s,
		title: l,
		...Rt(d)
	});
});
r0.displayName = `${O}.Icon`;
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/spinner/spinner.js
var i0;
(function(e) {
	e[e.SMALL = 20] = "SMALL", e[e.STANDARD = 50] = "STANDARD", e[e.LARGE = 100] = "LARGE";
})(i0 ||= {});
var a0 = 45, o0 = `M 50,50 m 0,-${a0} a ${a0},${a0} 0 1 1 0,${a0 * 2} a ${a0},${a0} 0 1 1 0,-${a0 * 2}`, s0 = 280, c0 = 10, l0 = 4, u0 = 16, d0 = (e) => {
	let { className: t = "", intent: n, value: r, tagName: i = "div", size: a, ...o } = e;
	en(() => {
		let e = a != null, n = t.indexOf(se) >= 0 || t.indexOf(S) >= 0;
		e && n && console.warn(Nt);
	}, [t, a]);
	let s = f0(a, t), c = Math.min(u0, l0 * i0.LARGE / s), l = s0 - s0 * (r == null ? .25 : Ft(r, 0, 1)), u = (0, $.default)(rt, Ct(n), { [ot]: r != null }, t);
	return (0, D.createElement)(i, {
		"aria-label": "loading",
		"aria-valuemax": 100,
		"aria-valuemin": 0,
		"aria-valuenow": r === void 0 ? void 0 : r * 100,
		className: u,
		role: "progressbar",
		...o
	}, (0, D.createElement)(i, { className: it }, (0, Q.jsxs)("svg", {
		width: s,
		height: s,
		strokeWidth: c.toFixed(2),
		viewBox: p0(c),
		children: [(0, Q.jsx)("path", {
			className: st,
			d: o0
		}), (0, Q.jsx)("path", {
			className: at,
			d: o0,
			pathLength: s0,
			strokeDasharray: `${s0} ${s0}`,
			strokeDashoffset: l
		})]
	})));
};
d0.displayName = `${O}.Spinner`;
var f0 = (e, t) => e == null ? t.indexOf(se) >= 0 ? i0.SMALL : t.indexOf(S) >= 0 ? i0.LARGE : i0.STANDARD : Math.max(c0, e), p0 = (e) => {
	let t = a0 + e / 2, n = (50 - t).toFixed(2), r = (t * 2).toFixed(2);
	return `${n} ${n} ${r} ${r}`;
}, m0 = E() ? D.useLayoutEffect : D.useEffect, h0 = (0, D.forwardRef)(({ children: e, tagName: t = "div", title: n, className: r, ellipsize: i = !1, ...a }, o) => {
	let s = (0, D.useRef)(), c = (0, D.useMemo)(() => Xt(s, o), [o]), [l, u] = (0, D.useState)(""), [d, f] = (0, D.useState)();
	return m0(() => {
		s.current?.textContent != null && (f(i && s.current.scrollWidth > s.current.clientWidth), u(s.current.textContent));
	}, [
		s,
		e,
		i
	]), (0, D.createElement)(t, {
		...a,
		className: (0, $.default)({ [le]: i }, r),
		ref: c,
		title: n ?? (d ? l : void 0)
	}, e);
});
h0.displayName = `${O}.Text`;
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/button/buttons.js
var g0 = (0, D.forwardRef)((e, t) => {
	let n = v0(e, t);
	return (0, Q.jsx)("button", {
		type: "button",
		...Rt(e),
		...n,
		children: y0(e)
	});
});
g0.displayName = `${O}.Button`;
var _0 = (0, D.forwardRef)((e, t) => {
	let { href: n } = e, r = v0(e, t, {
		defaultTabIndex: 0,
		disabledTabIndex: -1
	});
	return (0, Q.jsx)("a", {
		role: "button",
		...Rt(e),
		...r,
		"aria-disabled": r.disabled,
		href: r.disabled ? void 0 : n,
		children: y0(e)
	});
});
_0.displayName = `${O}.AnchorButton`;
function v0(e, t, n) {
	let { alignText: r, fill: i, large: a, loading: o = !1, minimal: s, outlined: c, size: l = "medium", small: u, variant: d = "solid" } = e, f = e.disabled || o, [p, m] = nn(!f, e, t, n), h = (0, $.default)(he, {
		[g]: p,
		[b]: f,
		[x]: i,
		[C]: o
	}, bt(r), Ct(e.intent), Tt(l, {
		large: a,
		small: u
	}), Et(d, {
		minimal: s,
		outlined: c
	}), e.className);
	return {
		...m,
		className: h,
		disabled: f
	};
}
function y0(e) {
	let { children: t, ellipsizeText: n, endIcon: r, icon: i, loading: a, rightIcon: o, text: s, textClassName: c } = e, l = !zt(s) || !zt(t);
	return (0, Q.jsxs)(Q.Fragment, { children: [
		a && (0, Q.jsx)(d0, {
			className: _e,
			size: i0.SMALL
		}),
		(0, Q.jsx)(r0, { icon: i }),
		l && (0, Q.jsxs)(h0, {
			className: (0, $.default)(ve, c),
			ellipsize: n,
			tagName: "span",
			children: [s, t]
		}),
		(0, Q.jsx)(r0, { icon: r ?? o })
	] });
}
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/html/html.js
function b0(e, t) {
	return (0, D.forwardRef)((n, r) => {
		let { className: i, children: a, ...o } = n;
		return (0, D.createElement)(e, {
			...o,
			className: (0, $.default)(t, i),
			ref: r
		}, a);
	});
}
b0("h1", T), b0("h2", T), b0("h3", T);
var x0 = b0("h4", T);
b0("h5", T), b0("h6", T), b0("blockquote", w), b0("code", ue), b0("pre", de), b0("label", Ve), b0("ol", fe), b0("ul", fe);
//#endregion
//#region node_modules/scheduler/cjs/scheduler.production.min.js
var S0 = /* @__PURE__ */ s(((e) => {
	function t(e, t) {
		var n = e.length;
		e.push(t);
		a: for (; 0 < n;) {
			var r = n - 1 >>> 1, a = e[r];
			if (0 < i(a, t)) e[r] = t, e[n] = a, n = r;
			else break a;
		}
	}
	function n(e) {
		return e.length === 0 ? null : e[0];
	}
	function r(e) {
		if (e.length === 0) return null;
		var t = e[0], n = e.pop();
		if (n !== t) {
			e[0] = n;
			a: for (var r = 0, a = e.length, o = a >>> 1; r < o;) {
				var s = 2 * (r + 1) - 1, c = e[s], l = s + 1, u = e[l];
				if (0 > i(c, n)) l < a && 0 > i(u, c) ? (e[r] = u, e[l] = n, r = l) : (e[r] = c, e[s] = n, r = s);
				else if (l < a && 0 > i(u, n)) e[r] = u, e[l] = n, r = l;
				else break a;
			}
		}
		return t;
	}
	function i(e, t) {
		var n = e.sortIndex - t.sortIndex;
		return n === 0 ? e.id - t.id : n;
	}
	if (typeof performance == "object" && typeof performance.now == "function") {
		var a = performance;
		e.unstable_now = function() {
			return a.now();
		};
	} else {
		var o = Date, s = o.now();
		e.unstable_now = function() {
			return o.now() - s;
		};
	}
	var c = [], l = [], u = 1, d = null, f = 3, p = !1, m = !1, h = !1, g = typeof setTimeout == "function" ? setTimeout : null, _ = typeof clearTimeout == "function" ? clearTimeout : null, v = typeof setImmediate < "u" ? setImmediate : null;
	typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
	function y(e) {
		for (var i = n(l); i !== null;) {
			if (i.callback === null) r(l);
			else if (i.startTime <= e) r(l), i.sortIndex = i.expirationTime, t(c, i);
			else break;
			i = n(l);
		}
	}
	function b(e) {
		if (h = !1, y(e), !m) if (n(c) !== null) m = !0, ce(x);
		else {
			var t = n(l);
			t !== null && le(b, t.startTime - e);
		}
	}
	function x(t, i) {
		m = !1, h && (h = !1, _(S), S = -1), p = !0;
		var a = f;
		try {
			for (y(i), d = n(c); d !== null && (!(d.expirationTime > i) || t && !re());) {
				var o = d.callback;
				if (typeof o == "function") {
					d.callback = null, f = d.priorityLevel;
					var s = o(d.expirationTime <= i);
					i = e.unstable_now(), typeof s == "function" ? d.callback = s : d === n(c) && r(c), y(i);
				} else r(c);
				d = n(c);
			}
			if (d !== null) var u = !0;
			else {
				var g = n(l);
				g !== null && le(b, g.startTime - i), u = !1;
			}
			return u;
		} finally {
			d = null, f = a, p = !1;
		}
	}
	var ee = !1, te = null, S = -1, C = 5, ne = -1;
	function re() {
		return !(e.unstable_now() - ne < C);
	}
	function ie() {
		if (te !== null) {
			var t = e.unstable_now();
			ne = t;
			var n = !0;
			try {
				n = te(!0, t);
			} finally {
				n ? ae() : (ee = !1, te = null);
			}
		} else ee = !1;
	}
	var ae;
	if (typeof v == "function") ae = function() {
		v(ie);
	};
	else if (typeof MessageChannel < "u") {
		var oe = new MessageChannel(), se = oe.port2;
		oe.port1.onmessage = ie, ae = function() {
			se.postMessage(null);
		};
	} else ae = function() {
		g(ie, 0);
	};
	function ce(e) {
		te = e, ee || (ee = !0, ae());
	}
	function le(t, n) {
		S = g(function() {
			t(e.unstable_now());
		}, n);
	}
	e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(e) {
		e.callback = null;
	}, e.unstable_continueExecution = function() {
		m || p || (m = !0, ce(x));
	}, e.unstable_forceFrameRate = function(e) {
		0 > e || 125 < e ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : C = 0 < e ? Math.floor(1e3 / e) : 5;
	}, e.unstable_getCurrentPriorityLevel = function() {
		return f;
	}, e.unstable_getFirstCallbackNode = function() {
		return n(c);
	}, e.unstable_next = function(e) {
		switch (f) {
			case 1:
			case 2:
			case 3:
				var t = 3;
				break;
			default: t = f;
		}
		var n = f;
		f = t;
		try {
			return e();
		} finally {
			f = n;
		}
	}, e.unstable_pauseExecution = function() {}, e.unstable_requestPaint = function() {}, e.unstable_runWithPriority = function(e, t) {
		switch (e) {
			case 1:
			case 2:
			case 3:
			case 4:
			case 5: break;
			default: e = 3;
		}
		var n = f;
		f = e;
		try {
			return t();
		} finally {
			f = n;
		}
	}, e.unstable_scheduleCallback = function(r, i, a) {
		var o = e.unstable_now();
		switch (typeof a == "object" && a ? (a = a.delay, a = typeof a == "number" && 0 < a ? o + a : o) : a = o, r) {
			case 1:
				var s = -1;
				break;
			case 2:
				s = 250;
				break;
			case 5:
				s = 1073741823;
				break;
			case 4:
				s = 1e4;
				break;
			default: s = 5e3;
		}
		return s = a + s, r = {
			id: u++,
			callback: i,
			priorityLevel: r,
			startTime: a,
			expirationTime: s,
			sortIndex: -1
		}, a > o ? (r.sortIndex = a, t(l, r), n(c) === null && r === n(l) && (h ? (_(S), S = -1) : h = !0, le(b, a - o))) : (r.sortIndex = s, t(c, r), m || p || (m = !0, ce(x))), r;
	}, e.unstable_shouldYield = re, e.unstable_wrapCallback = function(e) {
		var t = f;
		return function() {
			var n = f;
			f = t;
			try {
				return e.apply(this, arguments);
			} finally {
				f = n;
			}
		};
	};
})), C0 = /* @__PURE__ */ s(((e, t) => {
	t.exports = S0();
})), w0 = /* @__PURE__ */ s(((e) => {
	var t = Ot(), n = C0();
	function r(e) {
		for (var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, n = 1; n < arguments.length; n++) t += "&args[]=" + encodeURIComponent(arguments[n]);
		return "Minified React error #" + e + "; visit " + t + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
	}
	var i = /* @__PURE__ */ new Set(), a = {};
	function o(e, t) {
		s(e, t), s(e + "Capture", t);
	}
	function s(e, t) {
		for (a[e] = t, e = 0; e < t.length; e++) i.add(t[e]);
	}
	var c = !(typeof window > "u" || window.document === void 0 || window.document.createElement === void 0), l = Object.prototype.hasOwnProperty, u = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, d = {}, f = {};
	function p(e) {
		return l.call(f, e) ? !0 : l.call(d, e) ? !1 : u.test(e) ? f[e] = !0 : (d[e] = !0, !1);
	}
	function m(e, t, n, r) {
		if (n !== null && n.type === 0) return !1;
		switch (typeof t) {
			case "function":
			case "symbol": return !0;
			case "boolean": return r ? !1 : n === null ? (e = e.toLowerCase().slice(0, 5), e !== "data-" && e !== "aria-") : !n.acceptsBooleans;
			default: return !1;
		}
	}
	function h(e, t, n, r) {
		if (t == null || m(e, t, n, r)) return !0;
		if (r) return !1;
		if (n !== null) switch (n.type) {
			case 3: return !t;
			case 4: return !1 === t;
			case 5: return isNaN(t);
			case 6: return isNaN(t) || 1 > t;
		}
		return !1;
	}
	function g(e, t, n, r, i, a, o) {
		this.acceptsBooleans = t === 2 || t === 3 || t === 4, this.attributeName = r, this.attributeNamespace = i, this.mustUseProperty = n, this.propertyName = e, this.type = t, this.sanitizeURL = a, this.removeEmptyString = o;
	}
	var _ = {};
	"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
		_[e] = new g(e, 0, !1, e, null, !1, !1);
	}), [
		["acceptCharset", "accept-charset"],
		["className", "class"],
		["htmlFor", "for"],
		["httpEquiv", "http-equiv"]
	].forEach(function(e) {
		var t = e[0];
		_[t] = new g(t, 1, !1, e[1], null, !1, !1);
	}), [
		"contentEditable",
		"draggable",
		"spellCheck",
		"value"
	].forEach(function(e) {
		_[e] = new g(e, 2, !1, e.toLowerCase(), null, !1, !1);
	}), [
		"autoReverse",
		"externalResourcesRequired",
		"focusable",
		"preserveAlpha"
	].forEach(function(e) {
		_[e] = new g(e, 2, !1, e, null, !1, !1);
	}), "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
		_[e] = new g(e, 3, !1, e.toLowerCase(), null, !1, !1);
	}), [
		"checked",
		"multiple",
		"muted",
		"selected"
	].forEach(function(e) {
		_[e] = new g(e, 3, !0, e, null, !1, !1);
	}), ["capture", "download"].forEach(function(e) {
		_[e] = new g(e, 4, !1, e, null, !1, !1);
	}), [
		"cols",
		"rows",
		"size",
		"span"
	].forEach(function(e) {
		_[e] = new g(e, 6, !1, e, null, !1, !1);
	}), ["rowSpan", "start"].forEach(function(e) {
		_[e] = new g(e, 5, !1, e.toLowerCase(), null, !1, !1);
	});
	var v = /[\-:]([a-z])/g;
	function y(e) {
		return e[1].toUpperCase();
	}
	"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
		var t = e.replace(v, y);
		_[t] = new g(t, 1, !1, e, null, !1, !1);
	}), "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
		var t = e.replace(v, y);
		_[t] = new g(t, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
	}), [
		"xml:base",
		"xml:lang",
		"xml:space"
	].forEach(function(e) {
		var t = e.replace(v, y);
		_[t] = new g(t, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
	}), ["tabIndex", "crossOrigin"].forEach(function(e) {
		_[e] = new g(e, 1, !1, e.toLowerCase(), null, !1, !1);
	}), _.xlinkHref = new g("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1), [
		"src",
		"href",
		"action",
		"formAction"
	].forEach(function(e) {
		_[e] = new g(e, 1, !1, e.toLowerCase(), null, !0, !0);
	});
	function b(e, t, n, r) {
		var i = _.hasOwnProperty(t) ? _[t] : null;
		(i === null ? r || !(2 < t.length) || t[0] !== "o" && t[0] !== "O" || t[1] !== "n" && t[1] !== "N" : i.type !== 0) && (h(t, n, i, r) && (n = null), r || i === null ? p(t) && (n === null ? e.removeAttribute(t) : e.setAttribute(t, "" + n)) : i.mustUseProperty ? e[i.propertyName] = n === null ? i.type !== 3 && "" : n : (t = i.attributeName, r = i.attributeNamespace, n === null ? e.removeAttribute(t) : (i = i.type, n = i === 3 || i === 4 && !0 === n ? "" : "" + n, r ? e.setAttributeNS(r, t, n) : e.setAttribute(t, n))));
	}
	var x = t.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, ee = Symbol.for("react.element"), te = Symbol.for("react.portal"), S = Symbol.for("react.fragment"), C = Symbol.for("react.strict_mode"), ne = Symbol.for("react.profiler"), re = Symbol.for("react.provider"), ie = Symbol.for("react.context"), ae = Symbol.for("react.forward_ref"), oe = Symbol.for("react.suspense"), se = Symbol.for("react.suspense_list"), ce = Symbol.for("react.memo"), le = Symbol.for("react.lazy"), w = Symbol.for("react.offscreen"), ue = Symbol.iterator;
	function de(e) {
		return typeof e != "object" || !e ? null : (e = ue && e[ue] || e["@@iterator"], typeof e == "function" ? e : null);
	}
	var T = Object.assign, fe;
	function pe(e) {
		if (fe === void 0) try {
			throw Error();
		} catch (e) {
			var t = e.stack.trim().match(/\n( *(at )?)/);
			fe = t && t[1] || "";
		}
		return "\n" + fe + e;
	}
	var me = !1;
	function he(e, t) {
		if (!e || me) return "";
		me = !0;
		var n = Error.prepareStackTrace;
		Error.prepareStackTrace = void 0;
		try {
			if (t) if (t = function() {
				throw Error();
			}, Object.defineProperty(t.prototype, "props", { set: function() {
				throw Error();
			} }), typeof Reflect == "object" && Reflect.construct) {
				try {
					Reflect.construct(t, []);
				} catch (e) {
					var r = e;
				}
				Reflect.construct(e, [], t);
			} else {
				try {
					t.call();
				} catch (e) {
					r = e;
				}
				e.call(t.prototype);
			}
			else {
				try {
					throw Error();
				} catch (e) {
					r = e;
				}
				e();
			}
		} catch (t) {
			if (t && r && typeof t.stack == "string") {
				for (var i = t.stack.split("\n"), a = r.stack.split("\n"), o = i.length - 1, s = a.length - 1; 1 <= o && 0 <= s && i[o] !== a[s];) s--;
				for (; 1 <= o && 0 <= s; o--, s--) if (i[o] !== a[s]) {
					if (o !== 1 || s !== 1) do
						if (o--, s--, 0 > s || i[o] !== a[s]) {
							var c = "\n" + i[o].replace(" at new ", " at ");
							return e.displayName && c.includes("<anonymous>") && (c = c.replace("<anonymous>", e.displayName)), c;
						}
					while (1 <= o && 0 <= s);
					break;
				}
			}
		} finally {
			me = !1, Error.prepareStackTrace = n;
		}
		return (e = e ? e.displayName || e.name : "") ? pe(e) : "";
	}
	function ge(e) {
		switch (e.tag) {
			case 5: return pe(e.type);
			case 16: return pe("Lazy");
			case 13: return pe("Suspense");
			case 19: return pe("SuspenseList");
			case 0:
			case 2:
			case 15: return e = he(e.type, !1), e;
			case 11: return e = he(e.type.render, !1), e;
			case 1: return e = he(e.type, !0), e;
			default: return "";
		}
	}
	function _e(e) {
		if (e == null) return null;
		if (typeof e == "function") return e.displayName || e.name || null;
		if (typeof e == "string") return e;
		switch (e) {
			case S: return "Fragment";
			case te: return "Portal";
			case ne: return "Profiler";
			case C: return "StrictMode";
			case oe: return "Suspense";
			case se: return "SuspenseList";
		}
		if (typeof e == "object") switch (e.$$typeof) {
			case ie: return (e.displayName || "Context") + ".Consumer";
			case re: return (e._context.displayName || "Context") + ".Provider";
			case ae:
				var t = e.render;
				return e = e.displayName, e ||= (e = t.displayName || t.name || "", e === "" ? "ForwardRef" : "ForwardRef(" + e + ")"), e;
			case ce: return t = e.displayName || null, t === null ? _e(e.type) || "Memo" : t;
			case le:
				t = e._payload, e = e._init;
				try {
					return _e(e(t));
				} catch {}
		}
		return null;
	}
	function ve(e) {
		var t = e.type;
		switch (e.tag) {
			case 24: return "Cache";
			case 9: return (t.displayName || "Context") + ".Consumer";
			case 10: return (t._context.displayName || "Context") + ".Provider";
			case 18: return "DehydratedFragment";
			case 11: return e = t.render, e = e.displayName || e.name || "", t.displayName || (e === "" ? "ForwardRef" : "ForwardRef(" + e + ")");
			case 7: return "Fragment";
			case 5: return t;
			case 4: return "Portal";
			case 3: return "Root";
			case 6: return "Text";
			case 16: return _e(t);
			case 8: return t === C ? "StrictMode" : "Mode";
			case 22: return "Offscreen";
			case 12: return "Profiler";
			case 21: return "Scope";
			case 13: return "Suspense";
			case 19: return "SuspenseList";
			case 25: return "TracingMarker";
			case 1:
			case 0:
			case 17:
			case 2:
			case 14:
			case 15:
				if (typeof t == "function") return t.displayName || t.name || null;
				if (typeof t == "string") return t;
		}
		return null;
	}
	function ye(e) {
		switch (typeof e) {
			case "boolean":
			case "number":
			case "string":
			case "undefined": return e;
			case "object": return e;
			default: return "";
		}
	}
	function be(e) {
		var t = e.type;
		return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
	}
	function xe(e) {
		var t = be(e) ? "checked" : "value", n = Object.getOwnPropertyDescriptor(e.constructor.prototype, t), r = "" + e[t];
		if (!e.hasOwnProperty(t) && n !== void 0 && typeof n.get == "function" && typeof n.set == "function") {
			var i = n.get, a = n.set;
			return Object.defineProperty(e, t, {
				configurable: !0,
				get: function() {
					return i.call(this);
				},
				set: function(e) {
					r = "" + e, a.call(this, e);
				}
			}), Object.defineProperty(e, t, { enumerable: n.enumerable }), {
				getValue: function() {
					return r;
				},
				setValue: function(e) {
					r = "" + e;
				},
				stopTracking: function() {
					e._valueTracker = null, delete e[t];
				}
			};
		}
	}
	function Se(e) {
		e._valueTracker ||= xe(e);
	}
	function Ce(e) {
		if (!e) return !1;
		var t = e._valueTracker;
		if (!t) return !0;
		var n = t.getValue(), r = "";
		return e && (r = be(e) ? e.checked ? "true" : "false" : e.value), e = r, e === n ? !1 : (t.setValue(e), !0);
	}
	function we(e) {
		if (e ||= typeof document < "u" ? document : void 0, e === void 0) return null;
		try {
			return e.activeElement || e.body;
		} catch {
			return e.body;
		}
	}
	function Te(e, t) {
		var n = t.checked;
		return T({}, t, {
			defaultChecked: void 0,
			defaultValue: void 0,
			value: void 0,
			checked: n ?? e._wrapperState.initialChecked
		});
	}
	function Ee(e, t) {
		var n = t.defaultValue == null ? "" : t.defaultValue, r = t.checked == null ? t.defaultChecked : t.checked;
		n = ye(t.value == null ? n : t.value), e._wrapperState = {
			initialChecked: r,
			initialValue: n,
			controlled: t.type === "checkbox" || t.type === "radio" ? t.checked != null : t.value != null
		};
	}
	function De(e, t) {
		t = t.checked, t != null && b(e, "checked", t, !1);
	}
	function Oe(e, t) {
		De(e, t);
		var n = ye(t.value), r = t.type;
		if (n != null) r === "number" ? (n === 0 && e.value === "" || e.value != n) && (e.value = "" + n) : e.value !== "" + n && (e.value = "" + n);
		else if (r === "submit" || r === "reset") {
			e.removeAttribute("value");
			return;
		}
		t.hasOwnProperty("value") ? Ae(e, t.type, n) : t.hasOwnProperty("defaultValue") && Ae(e, t.type, ye(t.defaultValue)), t.checked == null && t.defaultChecked != null && (e.defaultChecked = !!t.defaultChecked);
	}
	function ke(e, t, n) {
		if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
			var r = t.type;
			if (!(r !== "submit" && r !== "reset" || t.value !== void 0 && t.value !== null)) return;
			t = "" + e._wrapperState.initialValue, n || t === e.value || (e.value = t), e.defaultValue = t;
		}
		n = e.name, n !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, n !== "" && (e.name = n);
	}
	function Ae(e, t, n) {
		(t !== "number" || we(e.ownerDocument) !== e) && (n == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + n && (e.defaultValue = "" + n));
	}
	var je = Array.isArray;
	function Me(e, t, n, r) {
		if (e = e.options, t) {
			t = {};
			for (var i = 0; i < n.length; i++) t["$" + n[i]] = !0;
			for (n = 0; n < e.length; n++) i = t.hasOwnProperty("$" + e[n].value), e[n].selected !== i && (e[n].selected = i), i && r && (e[n].defaultSelected = !0);
		} else {
			for (n = "" + ye(n), t = null, i = 0; i < e.length; i++) {
				if (e[i].value === n) {
					e[i].selected = !0, r && (e[i].defaultSelected = !0);
					return;
				}
				t !== null || e[i].disabled || (t = e[i]);
			}
			t !== null && (t.selected = !0);
		}
	}
	function Ne(e, t) {
		if (t.dangerouslySetInnerHTML != null) throw Error(r(91));
		return T({}, t, {
			value: void 0,
			defaultValue: void 0,
			children: "" + e._wrapperState.initialValue
		});
	}
	function Pe(e, t) {
		var n = t.value;
		if (n == null) {
			if (n = t.children, t = t.defaultValue, n != null) {
				if (t != null) throw Error(r(92));
				if (je(n)) {
					if (1 < n.length) throw Error(r(93));
					n = n[0];
				}
				t = n;
			}
			t ??= "", n = t;
		}
		e._wrapperState = { initialValue: ye(n) };
	}
	function Fe(e, t) {
		var n = ye(t.value), r = ye(t.defaultValue);
		n != null && (n = "" + n, n !== e.value && (e.value = n), t.defaultValue == null && e.defaultValue !== n && (e.defaultValue = n)), r != null && (e.defaultValue = "" + r);
	}
	function Ie(e) {
		var t = e.textContent;
		t === e._wrapperState.initialValue && t !== "" && t !== null && (e.value = t);
	}
	function Le(e) {
		switch (e) {
			case "svg": return "http://www.w3.org/2000/svg";
			case "math": return "http://www.w3.org/1998/Math/MathML";
			default: return "http://www.w3.org/1999/xhtml";
		}
	}
	function Re(e, t) {
		return e == null || e === "http://www.w3.org/1999/xhtml" ? Le(t) : e === "http://www.w3.org/2000/svg" && t === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
	}
	var ze, Be = function(e) {
		return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, n, r, i) {
			MSApp.execUnsafeLocalFunction(function() {
				return e(t, n, r, i);
			});
		} : e;
	}(function(e, t) {
		if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e) e.innerHTML = t;
		else {
			for (ze ||= document.createElement("div"), ze.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>", t = ze.firstChild; e.firstChild;) e.removeChild(e.firstChild);
			for (; t.firstChild;) e.appendChild(t.firstChild);
		}
	});
	function Ve(e, t) {
		if (t) {
			var n = e.firstChild;
			if (n && n === e.lastChild && n.nodeType === 3) {
				n.nodeValue = t;
				return;
			}
		}
		e.textContent = t;
	}
	var He = {
		animationIterationCount: !0,
		aspectRatio: !0,
		borderImageOutset: !0,
		borderImageSlice: !0,
		borderImageWidth: !0,
		boxFlex: !0,
		boxFlexGroup: !0,
		boxOrdinalGroup: !0,
		columnCount: !0,
		columns: !0,
		flex: !0,
		flexGrow: !0,
		flexPositive: !0,
		flexShrink: !0,
		flexNegative: !0,
		flexOrder: !0,
		gridArea: !0,
		gridRow: !0,
		gridRowEnd: !0,
		gridRowSpan: !0,
		gridRowStart: !0,
		gridColumn: !0,
		gridColumnEnd: !0,
		gridColumnSpan: !0,
		gridColumnStart: !0,
		fontWeight: !0,
		lineClamp: !0,
		lineHeight: !0,
		opacity: !0,
		order: !0,
		orphans: !0,
		tabSize: !0,
		widows: !0,
		zIndex: !0,
		zoom: !0,
		fillOpacity: !0,
		floodOpacity: !0,
		stopOpacity: !0,
		strokeDasharray: !0,
		strokeDashoffset: !0,
		strokeMiterlimit: !0,
		strokeOpacity: !0,
		strokeWidth: !0
	}, Ue = [
		"Webkit",
		"ms",
		"Moz",
		"O"
	];
	Object.keys(He).forEach(function(e) {
		Ue.forEach(function(t) {
			t = t + e.charAt(0).toUpperCase() + e.substring(1), He[t] = He[e];
		});
	});
	function We(e, t, n) {
		return t == null || typeof t == "boolean" || t === "" ? "" : n || typeof t != "number" || t === 0 || He.hasOwnProperty(e) && He[e] ? ("" + t).trim() : t + "px";
	}
	function Ge(e, t) {
		for (var n in e = e.style, t) if (t.hasOwnProperty(n)) {
			var r = n.indexOf("--") === 0, i = We(n, t[n], r);
			n === "float" && (n = "cssFloat"), r ? e.setProperty(n, i) : e[n] = i;
		}
	}
	var Ke = T({ menuitem: !0 }, {
		area: !0,
		base: !0,
		br: !0,
		col: !0,
		embed: !0,
		hr: !0,
		img: !0,
		input: !0,
		keygen: !0,
		link: !0,
		meta: !0,
		param: !0,
		source: !0,
		track: !0,
		wbr: !0
	});
	function qe(e, t) {
		if (t) {
			if (Ke[e] && (t.children != null || t.dangerouslySetInnerHTML != null)) throw Error(r(137, e));
			if (t.dangerouslySetInnerHTML != null) {
				if (t.children != null) throw Error(r(60));
				if (typeof t.dangerouslySetInnerHTML != "object" || !("__html" in t.dangerouslySetInnerHTML)) throw Error(r(61));
			}
			if (t.style != null && typeof t.style != "object") throw Error(r(62));
		}
	}
	function Je(e, t) {
		if (e.indexOf("-") === -1) return typeof t.is == "string";
		switch (e) {
			case "annotation-xml":
			case "color-profile":
			case "font-face":
			case "font-face-src":
			case "font-face-uri":
			case "font-face-format":
			case "font-face-name":
			case "missing-glyph": return !1;
			default: return !0;
		}
	}
	var Ye = null;
	function Xe(e) {
		return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
	}
	var Ze = null, Qe = null, $e = null;
	function et(e) {
		if (e = Zi(e)) {
			if (typeof Ze != "function") throw Error(r(280));
			var t = e.stateNode;
			t && (t = $i(t), Ze(e.stateNode, e.type, t));
		}
	}
	function tt(e) {
		Qe ? $e ? $e.push(e) : $e = [e] : Qe = e;
	}
	function nt() {
		if (Qe) {
			var e = Qe, t = $e;
			if ($e = Qe = null, et(e), t) for (e = 0; e < t.length; e++) et(t[e]);
		}
	}
	function rt(e, t) {
		return e(t);
	}
	function it() {}
	var at = !1;
	function ot(e, t, n) {
		if (at) return e(t, n);
		at = !0;
		try {
			return rt(e, t, n);
		} finally {
			at = !1, (Qe !== null || $e !== null) && (it(), nt());
		}
	}
	function st(e, t) {
		var n = e.stateNode;
		if (n === null) return null;
		var i = $i(n);
		if (i === null) return null;
		n = i[t];
		a: switch (t) {
			case "onClick":
			case "onClickCapture":
			case "onDoubleClick":
			case "onDoubleClickCapture":
			case "onMouseDown":
			case "onMouseDownCapture":
			case "onMouseMove":
			case "onMouseMoveCapture":
			case "onMouseUp":
			case "onMouseUpCapture":
			case "onMouseEnter":
				(i = !i.disabled) || (e = e.type, i = !(e === "button" || e === "input" || e === "select" || e === "textarea")), e = !i;
				break a;
			default: e = !1;
		}
		if (e) return null;
		if (n && typeof n != "function") throw Error(r(231, t, typeof n));
		return n;
	}
	var ct = !1;
	if (c) try {
		var lt = {};
		Object.defineProperty(lt, "passive", { get: function() {
			ct = !0;
		} }), window.addEventListener("test", lt, lt), window.removeEventListener("test", lt, lt);
	} catch {
		ct = !1;
	}
	function ut(e, t, n, r, i, a, o, s, c) {
		var l = Array.prototype.slice.call(arguments, 3);
		try {
			t.apply(n, l);
		} catch (e) {
			this.onError(e);
		}
	}
	var dt = !1, ft = null, pt = !1, mt = null, ht = { onError: function(e) {
		dt = !0, ft = e;
	} };
	function gt(e, t, n, r, i, a, o, s, c) {
		dt = !1, ft = null, ut.apply(ht, arguments);
	}
	function _t(e, t, n, i, a, o, s, c, l) {
		if (gt.apply(this, arguments), dt) {
			if (dt) {
				var u = ft;
				dt = !1, ft = null;
			} else throw Error(r(198));
			pt || (pt = !0, mt = u);
		}
	}
	function vt(e) {
		var t = e, n = e;
		if (e.alternate) for (; t.return;) t = t.return;
		else {
			e = t;
			do
				t = e, t.flags & 4098 && (n = t.return), e = t.return;
			while (e);
		}
		return t.tag === 3 ? n : null;
	}
	function yt(e) {
		if (e.tag === 13) {
			var t = e.memoizedState;
			if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null) return t.dehydrated;
		}
		return null;
	}
	function bt(e) {
		if (vt(e) !== e) throw Error(r(188));
	}
	function xt(e) {
		var t = e.alternate;
		if (!t) {
			if (t = vt(e), t === null) throw Error(r(188));
			return t === e ? e : null;
		}
		for (var n = e, i = t;;) {
			var a = n.return;
			if (a === null) break;
			var o = a.alternate;
			if (o === null) {
				if (i = a.return, i !== null) {
					n = i;
					continue;
				}
				break;
			}
			if (a.child === o.child) {
				for (o = a.child; o;) {
					if (o === n) return bt(a), e;
					if (o === i) return bt(a), t;
					o = o.sibling;
				}
				throw Error(r(188));
			}
			if (n.return !== i.return) n = a, i = o;
			else {
				for (var s = !1, c = a.child; c;) {
					if (c === n) {
						s = !0, n = a, i = o;
						break;
					}
					if (c === i) {
						s = !0, i = a, n = o;
						break;
					}
					c = c.sibling;
				}
				if (!s) {
					for (c = o.child; c;) {
						if (c === n) {
							s = !0, n = o, i = a;
							break;
						}
						if (c === i) {
							s = !0, i = o, n = a;
							break;
						}
						c = c.sibling;
					}
					if (!s) throw Error(r(189));
				}
			}
			if (n.alternate !== i) throw Error(r(190));
		}
		if (n.tag !== 3) throw Error(r(188));
		return n.stateNode.current === n ? e : t;
	}
	function St(e) {
		return e = xt(e), e === null ? null : Ct(e);
	}
	function Ct(e) {
		if (e.tag === 5 || e.tag === 6) return e;
		for (e = e.child; e !== null;) {
			var t = Ct(e);
			if (t !== null) return t;
			e = e.sibling;
		}
		return null;
	}
	var wt = n.unstable_scheduleCallback, Tt = n.unstable_cancelCallback, Et = n.unstable_shouldYield, Dt = n.unstable_requestPaint, E = n.unstable_now, kt = n.unstable_getCurrentPriorityLevel, At = n.unstable_ImmediatePriority, jt = n.unstable_UserBlockingPriority, Mt = n.unstable_NormalPriority, Nt = n.unstable_LowPriority, D = n.unstable_IdlePriority, Pt = null, Ft = null;
	function It(e) {
		if (Ft && typeof Ft.onCommitFiberRoot == "function") try {
			Ft.onCommitFiberRoot(Pt, e, void 0, (e.current.flags & 128) == 128);
		} catch {}
	}
	var O = Math.clz32 ? Math.clz32 : zt, Lt = Math.log, Rt = Math.LN2;
	function zt(e) {
		return e >>>= 0, e === 0 ? 32 : 31 - (Lt(e) / Rt | 0) | 0;
	}
	var Bt = 64, Vt = 4194304;
	function Ht(e) {
		switch (e & -e) {
			case 1: return 1;
			case 2: return 2;
			case 4: return 4;
			case 8: return 8;
			case 16: return 16;
			case 32: return 32;
			case 64:
			case 128:
			case 256:
			case 512:
			case 1024:
			case 2048:
			case 4096:
			case 8192:
			case 16384:
			case 32768:
			case 65536:
			case 131072:
			case 262144:
			case 524288:
			case 1048576:
			case 2097152: return e & 4194240;
			case 4194304:
			case 8388608:
			case 16777216:
			case 33554432:
			case 67108864: return e & 130023424;
			case 134217728: return 134217728;
			case 268435456: return 268435456;
			case 536870912: return 536870912;
			case 1073741824: return 1073741824;
			default: return e;
		}
	}
	function Ut(e, t) {
		var n = e.pendingLanes;
		if (n === 0) return 0;
		var r = 0, i = e.suspendedLanes, a = e.pingedLanes, o = n & 268435455;
		if (o !== 0) {
			var s = o & ~i;
			s === 0 ? (a &= o, a !== 0 && (r = Ht(a))) : r = Ht(s);
		} else o = n & ~i, o === 0 ? a !== 0 && (r = Ht(a)) : r = Ht(o);
		if (r === 0) return 0;
		if (t !== 0 && t !== r && (t & i) === 0 && (i = r & -r, a = t & -t, i >= a || i === 16 && a & 4194240)) return t;
		if (r & 4 && (r |= n & 16), t = e.entangledLanes, t !== 0) for (e = e.entanglements, t &= r; 0 < t;) n = 31 - O(t), i = 1 << n, r |= e[n], t &= ~i;
		return r;
	}
	function Wt(e, t) {
		switch (e) {
			case 1:
			case 2:
			case 4: return t + 250;
			case 8:
			case 16:
			case 32:
			case 64:
			case 128:
			case 256:
			case 512:
			case 1024:
			case 2048:
			case 4096:
			case 8192:
			case 16384:
			case 32768:
			case 65536:
			case 131072:
			case 262144:
			case 524288:
			case 1048576:
			case 2097152: return t + 5e3;
			case 4194304:
			case 8388608:
			case 16777216:
			case 33554432:
			case 67108864: return -1;
			case 134217728:
			case 268435456:
			case 536870912:
			case 1073741824: return -1;
			default: return -1;
		}
	}
	function Gt(e, t) {
		for (var n = e.suspendedLanes, r = e.pingedLanes, i = e.expirationTimes, a = e.pendingLanes; 0 < a;) {
			var o = 31 - O(a), s = 1 << o, c = i[o];
			c === -1 ? ((s & n) === 0 || (s & r) !== 0) && (i[o] = Wt(s, t)) : c <= t && (e.expiredLanes |= s), a &= ~s;
		}
	}
	function Kt(e) {
		return e = e.pendingLanes & -1073741825, e === 0 ? e & 1073741824 ? 1073741824 : 0 : e;
	}
	function qt() {
		var e = Bt;
		return Bt <<= 1, !(Bt & 4194240) && (Bt = 64), e;
	}
	function Jt(e) {
		for (var t = [], n = 0; 31 > n; n++) t.push(e);
		return t;
	}
	function Yt(e, t, n) {
		e.pendingLanes |= t, t !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, t = 31 - O(t), e[t] = n;
	}
	function Xt(e, t) {
		var n = e.pendingLanes & ~t;
		e.pendingLanes = t, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t, t = e.entanglements;
		var r = e.eventTimes;
		for (e = e.expirationTimes; 0 < n;) {
			var i = 31 - O(n), a = 1 << i;
			t[i] = 0, r[i] = -1, e[i] = -1, n &= ~a;
		}
	}
	function Zt(e, t) {
		var n = e.entangledLanes |= t;
		for (e = e.entanglements; n;) {
			var r = 31 - O(n), i = 1 << r;
			i & t | e[r] & t && (e[r] |= t), n &= ~i;
		}
	}
	var k = 0;
	function Qt(e) {
		return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
	}
	var $t, en, tn, nn, rn, an = !1, on = [], sn = null, cn = null, ln = null, un = /* @__PURE__ */ new Map(), dn = /* @__PURE__ */ new Map(), fn = [], pn = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
	function mn(e, t) {
		switch (e) {
			case "focusin":
			case "focusout":
				sn = null;
				break;
			case "dragenter":
			case "dragleave":
				cn = null;
				break;
			case "mouseover":
			case "mouseout":
				ln = null;
				break;
			case "pointerover":
			case "pointerout":
				un.delete(t.pointerId);
				break;
			case "gotpointercapture":
			case "lostpointercapture": dn.delete(t.pointerId);
		}
	}
	function hn(e, t, n, r, i, a) {
		return e === null || e.nativeEvent !== a ? (e = {
			blockedOn: t,
			domEventName: n,
			eventSystemFlags: r,
			nativeEvent: a,
			targetContainers: [i]
		}, t !== null && (t = Zi(t), t !== null && en(t)), e) : (e.eventSystemFlags |= r, t = e.targetContainers, i !== null && t.indexOf(i) === -1 && t.push(i), e);
	}
	function gn(e, t, n, r, i) {
		switch (t) {
			case "focusin": return sn = hn(sn, e, t, n, r, i), !0;
			case "dragenter": return cn = hn(cn, e, t, n, r, i), !0;
			case "mouseover": return ln = hn(ln, e, t, n, r, i), !0;
			case "pointerover":
				var a = i.pointerId;
				return un.set(a, hn(un.get(a) || null, e, t, n, r, i)), !0;
			case "gotpointercapture": return a = i.pointerId, dn.set(a, hn(dn.get(a) || null, e, t, n, r, i)), !0;
		}
		return !1;
	}
	function _n(e) {
		var t = Xi(e.target);
		if (t !== null) {
			var n = vt(t);
			if (n !== null) {
				if (t = n.tag, t === 13) {
					if (t = yt(n), t !== null) {
						e.blockedOn = t, rn(e.priority, function() {
							tn(n);
						});
						return;
					}
				} else if (t === 3 && n.stateNode.current.memoizedState.isDehydrated) {
					e.blockedOn = n.tag === 3 ? n.stateNode.containerInfo : null;
					return;
				}
			}
		}
		e.blockedOn = null;
	}
	function vn(e) {
		if (e.blockedOn !== null) return !1;
		for (var t = e.targetContainers; 0 < t.length;) {
			var n = kn(e.domEventName, e.eventSystemFlags, t[0], e.nativeEvent);
			if (n === null) {
				n = e.nativeEvent;
				var r = new n.constructor(n.type, n);
				Ye = r, n.target.dispatchEvent(r), Ye = null;
			} else return t = Zi(n), t !== null && en(t), e.blockedOn = n, !1;
			t.shift();
		}
		return !0;
	}
	function yn(e, t, n) {
		vn(e) && n.delete(t);
	}
	function bn() {
		an = !1, sn !== null && vn(sn) && (sn = null), cn !== null && vn(cn) && (cn = null), ln !== null && vn(ln) && (ln = null), un.forEach(yn), dn.forEach(yn);
	}
	function xn(e, t) {
		e.blockedOn === t && (e.blockedOn = null, an || (an = !0, n.unstable_scheduleCallback(n.unstable_NormalPriority, bn)));
	}
	function Sn(e) {
		function t(t) {
			return xn(t, e);
		}
		if (0 < on.length) {
			xn(on[0], e);
			for (var n = 1; n < on.length; n++) {
				var r = on[n];
				r.blockedOn === e && (r.blockedOn = null);
			}
		}
		for (sn !== null && xn(sn, e), cn !== null && xn(cn, e), ln !== null && xn(ln, e), un.forEach(t), dn.forEach(t), n = 0; n < fn.length; n++) r = fn[n], r.blockedOn === e && (r.blockedOn = null);
		for (; 0 < fn.length && (n = fn[0], n.blockedOn === null);) _n(n), n.blockedOn === null && fn.shift();
	}
	var Cn = x.ReactCurrentBatchConfig, wn = !0;
	function Tn(e, t, n, r) {
		var i = k, a = Cn.transition;
		Cn.transition = null;
		try {
			k = 1, Dn(e, t, n, r);
		} finally {
			k = i, Cn.transition = a;
		}
	}
	function En(e, t, n, r) {
		var i = k, a = Cn.transition;
		Cn.transition = null;
		try {
			k = 4, Dn(e, t, n, r);
		} finally {
			k = i, Cn.transition = a;
		}
	}
	function Dn(e, t, n, r) {
		if (wn) {
			var i = kn(e, t, n, r);
			if (i === null) Si(e, t, r, On, n), mn(e, r);
			else if (gn(i, e, t, n, r)) r.stopPropagation();
			else if (mn(e, r), t & 4 && -1 < pn.indexOf(e)) {
				for (; i !== null;) {
					var a = Zi(i);
					if (a !== null && $t(a), a = kn(e, t, n, r), a === null && Si(e, t, r, On, n), a === i) break;
					i = a;
				}
				i !== null && r.stopPropagation();
			} else Si(e, t, r, null, n);
		}
	}
	var On = null;
	function kn(e, t, n, r) {
		if (On = null, e = Xe(r), e = Xi(e), e !== null) if (t = vt(e), t === null) e = null;
		else if (n = t.tag, n === 13) {
			if (e = yt(t), e !== null) return e;
			e = null;
		} else if (n === 3) {
			if (t.stateNode.current.memoizedState.isDehydrated) return t.tag === 3 ? t.stateNode.containerInfo : null;
			e = null;
		} else t !== e && (e = null);
		return On = e, null;
	}
	function An(e) {
		switch (e) {
			case "cancel":
			case "click":
			case "close":
			case "contextmenu":
			case "copy":
			case "cut":
			case "auxclick":
			case "dblclick":
			case "dragend":
			case "dragstart":
			case "drop":
			case "focusin":
			case "focusout":
			case "input":
			case "invalid":
			case "keydown":
			case "keypress":
			case "keyup":
			case "mousedown":
			case "mouseup":
			case "paste":
			case "pause":
			case "play":
			case "pointercancel":
			case "pointerdown":
			case "pointerup":
			case "ratechange":
			case "reset":
			case "resize":
			case "seeked":
			case "submit":
			case "touchcancel":
			case "touchend":
			case "touchstart":
			case "volumechange":
			case "change":
			case "selectionchange":
			case "textInput":
			case "compositionstart":
			case "compositionend":
			case "compositionupdate":
			case "beforeblur":
			case "afterblur":
			case "beforeinput":
			case "blur":
			case "fullscreenchange":
			case "focus":
			case "hashchange":
			case "popstate":
			case "select":
			case "selectstart": return 1;
			case "drag":
			case "dragenter":
			case "dragexit":
			case "dragleave":
			case "dragover":
			case "mousemove":
			case "mouseout":
			case "mouseover":
			case "pointermove":
			case "pointerout":
			case "pointerover":
			case "scroll":
			case "toggle":
			case "touchmove":
			case "wheel":
			case "mouseenter":
			case "mouseleave":
			case "pointerenter":
			case "pointerleave": return 4;
			case "message": switch (kt()) {
				case At: return 1;
				case jt: return 4;
				case Mt:
				case Nt: return 16;
				case D: return 536870912;
				default: return 16;
			}
			default: return 16;
		}
	}
	var jn = null, Mn = null, Nn = null;
	function Pn() {
		if (Nn) return Nn;
		var e, t = Mn, n = t.length, r, i = "value" in jn ? jn.value : jn.textContent, a = i.length;
		for (e = 0; e < n && t[e] === i[e]; e++);
		var o = n - e;
		for (r = 1; r <= o && t[n - r] === i[a - r]; r++);
		return Nn = i.slice(e, 1 < r ? 1 - r : void 0);
	}
	function Fn(e) {
		var t = e.keyCode;
		return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
	}
	function In() {
		return !0;
	}
	function Ln() {
		return !1;
	}
	function Rn(e) {
		function t(t, n, r, i, a) {
			for (var o in this._reactName = t, this._targetInst = r, this.type = n, this.nativeEvent = i, this.target = a, this.currentTarget = null, e) e.hasOwnProperty(o) && (t = e[o], this[o] = t ? t(i) : i[o]);
			return this.isDefaultPrevented = (i.defaultPrevented == null ? !1 === i.returnValue : i.defaultPrevented) ? In : Ln, this.isPropagationStopped = Ln, this;
		}
		return T(t.prototype, {
			preventDefault: function() {
				this.defaultPrevented = !0;
				var e = this.nativeEvent;
				e && (e.preventDefault ? e.preventDefault() : typeof e.returnValue != "unknown" && (e.returnValue = !1), this.isDefaultPrevented = In);
			},
			stopPropagation: function() {
				var e = this.nativeEvent;
				e && (e.stopPropagation ? e.stopPropagation() : typeof e.cancelBubble != "unknown" && (e.cancelBubble = !0), this.isPropagationStopped = In);
			},
			persist: function() {},
			isPersistent: In
		}), t;
	}
	var zn = {
		eventPhase: 0,
		bubbles: 0,
		cancelable: 0,
		timeStamp: function(e) {
			return e.timeStamp || Date.now();
		},
		defaultPrevented: 0,
		isTrusted: 0
	}, Bn = Rn(zn), Vn = T({}, zn, {
		view: 0,
		detail: 0
	}), Hn = Rn(Vn), Un, Wn, Gn, Kn = T({}, Vn, {
		screenX: 0,
		screenY: 0,
		clientX: 0,
		clientY: 0,
		pageX: 0,
		pageY: 0,
		ctrlKey: 0,
		shiftKey: 0,
		altKey: 0,
		metaKey: 0,
		getModifierState: rr,
		button: 0,
		buttons: 0,
		relatedTarget: function(e) {
			return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
		},
		movementX: function(e) {
			return "movementX" in e ? e.movementX : (e !== Gn && (Gn && e.type === "mousemove" ? (Un = e.screenX - Gn.screenX, Wn = e.screenY - Gn.screenY) : Wn = Un = 0, Gn = e), Un);
		},
		movementY: function(e) {
			return "movementY" in e ? e.movementY : Wn;
		}
	}), qn = Rn(Kn), Jn = Rn(T({}, Kn, { dataTransfer: 0 })), Yn = Rn(T({}, Vn, { relatedTarget: 0 })), Xn = Rn(T({}, zn, {
		animationName: 0,
		elapsedTime: 0,
		pseudoElement: 0
	})), Zn = Rn(T({}, zn, { clipboardData: function(e) {
		return "clipboardData" in e ? e.clipboardData : window.clipboardData;
	} })), Qn = Rn(T({}, zn, { data: 0 })), $n = {
		Esc: "Escape",
		Spacebar: " ",
		Left: "ArrowLeft",
		Up: "ArrowUp",
		Right: "ArrowRight",
		Down: "ArrowDown",
		Del: "Delete",
		Win: "OS",
		Menu: "ContextMenu",
		Apps: "ContextMenu",
		Scroll: "ScrollLock",
		MozPrintableKey: "Unidentified"
	}, er = {
		8: "Backspace",
		9: "Tab",
		12: "Clear",
		13: "Enter",
		16: "Shift",
		17: "Control",
		18: "Alt",
		19: "Pause",
		20: "CapsLock",
		27: "Escape",
		32: " ",
		33: "PageUp",
		34: "PageDown",
		35: "End",
		36: "Home",
		37: "ArrowLeft",
		38: "ArrowUp",
		39: "ArrowRight",
		40: "ArrowDown",
		45: "Insert",
		46: "Delete",
		112: "F1",
		113: "F2",
		114: "F3",
		115: "F4",
		116: "F5",
		117: "F6",
		118: "F7",
		119: "F8",
		120: "F9",
		121: "F10",
		122: "F11",
		123: "F12",
		144: "NumLock",
		145: "ScrollLock",
		224: "Meta"
	}, tr = {
		Alt: "altKey",
		Control: "ctrlKey",
		Meta: "metaKey",
		Shift: "shiftKey"
	};
	function nr(e) {
		var t = this.nativeEvent;
		return t.getModifierState ? t.getModifierState(e) : (e = tr[e]) ? !!t[e] : !1;
	}
	function rr() {
		return nr;
	}
	var ir = Rn(T({}, Vn, {
		key: function(e) {
			if (e.key) {
				var t = $n[e.key] || e.key;
				if (t !== "Unidentified") return t;
			}
			return e.type === "keypress" ? (e = Fn(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? er[e.keyCode] || "Unidentified" : "";
		},
		code: 0,
		location: 0,
		ctrlKey: 0,
		shiftKey: 0,
		altKey: 0,
		metaKey: 0,
		repeat: 0,
		locale: 0,
		getModifierState: rr,
		charCode: function(e) {
			return e.type === "keypress" ? Fn(e) : 0;
		},
		keyCode: function(e) {
			return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
		},
		which: function(e) {
			return e.type === "keypress" ? Fn(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
		}
	})), ar = Rn(T({}, Kn, {
		pointerId: 0,
		width: 0,
		height: 0,
		pressure: 0,
		tangentialPressure: 0,
		tiltX: 0,
		tiltY: 0,
		twist: 0,
		pointerType: 0,
		isPrimary: 0
	})), or = Rn(T({}, Vn, {
		touches: 0,
		targetTouches: 0,
		changedTouches: 0,
		altKey: 0,
		metaKey: 0,
		ctrlKey: 0,
		shiftKey: 0,
		getModifierState: rr
	})), sr = Rn(T({}, zn, {
		propertyName: 0,
		elapsedTime: 0,
		pseudoElement: 0
	})), cr = Rn(T({}, Kn, {
		deltaX: function(e) {
			return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
		},
		deltaY: function(e) {
			return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
		},
		deltaZ: 0,
		deltaMode: 0
	})), lr = [
		9,
		13,
		27,
		32
	], ur = c && "CompositionEvent" in window, dr = null;
	c && "documentMode" in document && (dr = document.documentMode);
	var fr = c && "TextEvent" in window && !dr, pr = c && (!ur || dr && 8 < dr && 11 >= dr), mr = " ", hr = !1;
	function gr(e, t) {
		switch (e) {
			case "keyup": return lr.indexOf(t.keyCode) !== -1;
			case "keydown": return t.keyCode !== 229;
			case "keypress":
			case "mousedown":
			case "focusout": return !0;
			default: return !1;
		}
	}
	function _r(e) {
		return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
	}
	var vr = !1;
	function yr(e, t) {
		switch (e) {
			case "compositionend": return _r(t);
			case "keypress": return t.which === 32 ? (hr = !0, mr) : null;
			case "textInput": return e = t.data, e === mr && hr ? null : e;
			default: return null;
		}
	}
	function br(e, t) {
		if (vr) return e === "compositionend" || !ur && gr(e, t) ? (e = Pn(), Nn = Mn = jn = null, vr = !1, e) : null;
		switch (e) {
			case "paste": return null;
			case "keypress":
				if (!(t.ctrlKey || t.altKey || t.metaKey) || t.ctrlKey && t.altKey) {
					if (t.char && 1 < t.char.length) return t.char;
					if (t.which) return String.fromCharCode(t.which);
				}
				return null;
			case "compositionend": return pr && t.locale !== "ko" ? null : t.data;
			default: return null;
		}
	}
	var xr = {
		color: !0,
		date: !0,
		datetime: !0,
		"datetime-local": !0,
		email: !0,
		month: !0,
		number: !0,
		password: !0,
		range: !0,
		search: !0,
		tel: !0,
		text: !0,
		time: !0,
		url: !0,
		week: !0
	};
	function Sr(e) {
		var t = e && e.nodeName && e.nodeName.toLowerCase();
		return t === "input" ? !!xr[e.type] : t === "textarea";
	}
	function Cr(e, t, n, r) {
		tt(r), t = wi(t, "onChange"), 0 < t.length && (n = new Bn("onChange", "change", null, n, r), e.push({
			event: n,
			listeners: t
		}));
	}
	var wr = null, Tr = null;
	function Er(e) {
		_i(e, 0);
	}
	function Dr(e) {
		if (Ce(Qi(e))) return e;
	}
	function Or(e, t) {
		if (e === "change") return t;
	}
	var kr = !1;
	if (c) {
		var Ar;
		if (c) {
			var jr = "oninput" in document;
			if (!jr) {
				var Mr = document.createElement("div");
				Mr.setAttribute("oninput", "return;"), jr = typeof Mr.oninput == "function";
			}
			Ar = jr;
		} else Ar = !1;
		kr = Ar && (!document.documentMode || 9 < document.documentMode);
	}
	function Nr() {
		wr && (wr.detachEvent("onpropertychange", Pr), Tr = wr = null);
	}
	function Pr(e) {
		if (e.propertyName === "value" && Dr(Tr)) {
			var t = [];
			Cr(t, Tr, e, Xe(e)), ot(Er, t);
		}
	}
	function Fr(e, t, n) {
		e === "focusin" ? (Nr(), wr = t, Tr = n, wr.attachEvent("onpropertychange", Pr)) : e === "focusout" && Nr();
	}
	function Ir(e) {
		if (e === "selectionchange" || e === "keyup" || e === "keydown") return Dr(Tr);
	}
	function Lr(e, t) {
		if (e === "click") return Dr(t);
	}
	function Rr(e, t) {
		if (e === "input" || e === "change") return Dr(t);
	}
	function zr(e, t) {
		return e === t && (e !== 0 || 1 / e == 1 / t) || e !== e && t !== t;
	}
	var Br = typeof Object.is == "function" ? Object.is : zr;
	function Vr(e, t) {
		if (Br(e, t)) return !0;
		if (typeof e != "object" || !e || typeof t != "object" || !t) return !1;
		var n = Object.keys(e), r = Object.keys(t);
		if (n.length !== r.length) return !1;
		for (r = 0; r < n.length; r++) {
			var i = n[r];
			if (!l.call(t, i) || !Br(e[i], t[i])) return !1;
		}
		return !0;
	}
	function Hr(e) {
		for (; e && e.firstChild;) e = e.firstChild;
		return e;
	}
	function Ur(e, t) {
		var n = Hr(e);
		e = 0;
		for (var r; n;) {
			if (n.nodeType === 3) {
				if (r = e + n.textContent.length, e <= t && r >= t) return {
					node: n,
					offset: t - e
				};
				e = r;
			}
			a: {
				for (; n;) {
					if (n.nextSibling) {
						n = n.nextSibling;
						break a;
					}
					n = n.parentNode;
				}
				n = void 0;
			}
			n = Hr(n);
		}
	}
	function Wr(e, t) {
		return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? Wr(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
	}
	function Gr() {
		for (var e = window, t = we(); t instanceof e.HTMLIFrameElement;) {
			try {
				var n = typeof t.contentWindow.location.href == "string";
			} catch {
				n = !1;
			}
			if (n) e = t.contentWindow;
			else break;
			t = we(e.document);
		}
		return t;
	}
	function Kr(e) {
		var t = e && e.nodeName && e.nodeName.toLowerCase();
		return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
	}
	function qr(e) {
		var t = Gr(), n = e.focusedElem, r = e.selectionRange;
		if (t !== n && n && n.ownerDocument && Wr(n.ownerDocument.documentElement, n)) {
			if (r !== null && Kr(n)) {
				if (t = r.start, e = r.end, e === void 0 && (e = t), "selectionStart" in n) n.selectionStart = t, n.selectionEnd = Math.min(e, n.value.length);
				else if (e = (t = n.ownerDocument || document) && t.defaultView || window, e.getSelection) {
					e = e.getSelection();
					var i = n.textContent.length, a = Math.min(r.start, i);
					r = r.end === void 0 ? a : Math.min(r.end, i), !e.extend && a > r && (i = r, r = a, a = i), i = Ur(n, a);
					var o = Ur(n, r);
					i && o && (e.rangeCount !== 1 || e.anchorNode !== i.node || e.anchorOffset !== i.offset || e.focusNode !== o.node || e.focusOffset !== o.offset) && (t = t.createRange(), t.setStart(i.node, i.offset), e.removeAllRanges(), a > r ? (e.addRange(t), e.extend(o.node, o.offset)) : (t.setEnd(o.node, o.offset), e.addRange(t)));
				}
			}
			for (t = [], e = n; e = e.parentNode;) e.nodeType === 1 && t.push({
				element: e,
				left: e.scrollLeft,
				top: e.scrollTop
			});
			for (typeof n.focus == "function" && n.focus(), n = 0; n < t.length; n++) e = t[n], e.element.scrollLeft = e.left, e.element.scrollTop = e.top;
		}
	}
	var Jr = c && "documentMode" in document && 11 >= document.documentMode, Yr = null, Xr = null, Zr = null, Qr = !1;
	function $r(e, t, n) {
		var r = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
		Qr || Yr == null || Yr !== we(r) || (r = Yr, "selectionStart" in r && Kr(r) ? r = {
			start: r.selectionStart,
			end: r.selectionEnd
		} : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = {
			anchorNode: r.anchorNode,
			anchorOffset: r.anchorOffset,
			focusNode: r.focusNode,
			focusOffset: r.focusOffset
		}), Zr && Vr(Zr, r) || (Zr = r, r = wi(Xr, "onSelect"), 0 < r.length && (t = new Bn("onSelect", "select", null, t, n), e.push({
			event: t,
			listeners: r
		}), t.target = Yr)));
	}
	function ei(e, t) {
		var n = {};
		return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit" + e] = "webkit" + t, n["Moz" + e] = "moz" + t, n;
	}
	var ti = {
		animationend: ei("Animation", "AnimationEnd"),
		animationiteration: ei("Animation", "AnimationIteration"),
		animationstart: ei("Animation", "AnimationStart"),
		transitionend: ei("Transition", "TransitionEnd")
	}, ni = {}, ri = {};
	c && (ri = document.createElement("div").style, "AnimationEvent" in window || (delete ti.animationend.animation, delete ti.animationiteration.animation, delete ti.animationstart.animation), "TransitionEvent" in window || delete ti.transitionend.transition);
	function ii(e) {
		if (ni[e]) return ni[e];
		if (!ti[e]) return e;
		var t = ti[e], n;
		for (n in t) if (t.hasOwnProperty(n) && n in ri) return ni[e] = t[n];
		return e;
	}
	var ai = ii("animationend"), oi = ii("animationiteration"), si = ii("animationstart"), ci = ii("transitionend"), li = /* @__PURE__ */ new Map(), ui = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
	function di(e, t) {
		li.set(e, t), o(t, [e]);
	}
	for (var fi = 0; fi < ui.length; fi++) {
		var pi = ui[fi];
		di(pi.toLowerCase(), "on" + (pi[0].toUpperCase() + pi.slice(1)));
	}
	di(ai, "onAnimationEnd"), di(oi, "onAnimationIteration"), di(si, "onAnimationStart"), di("dblclick", "onDoubleClick"), di("focusin", "onFocus"), di("focusout", "onBlur"), di(ci, "onTransitionEnd"), s("onMouseEnter", ["mouseout", "mouseover"]), s("onMouseLeave", ["mouseout", "mouseover"]), s("onPointerEnter", ["pointerout", "pointerover"]), s("onPointerLeave", ["pointerout", "pointerover"]), o("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" ")), o("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")), o("onBeforeInput", [
		"compositionend",
		"keypress",
		"textInput",
		"paste"
	]), o("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" ")), o("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" ")), o("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
	var mi = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), hi = new Set("cancel close invalid load scroll toggle".split(" ").concat(mi));
	function gi(e, t, n) {
		var r = e.type || "unknown-event";
		e.currentTarget = n, _t(r, t, void 0, e), e.currentTarget = null;
	}
	function _i(e, t) {
		t = (t & 4) != 0;
		for (var n = 0; n < e.length; n++) {
			var r = e[n], i = r.event;
			r = r.listeners;
			a: {
				var a = void 0;
				if (t) for (var o = r.length - 1; 0 <= o; o--) {
					var s = r[o], c = s.instance, l = s.currentTarget;
					if (s = s.listener, c !== a && i.isPropagationStopped()) break a;
					gi(i, s, l), a = c;
				}
				else for (o = 0; o < r.length; o++) {
					if (s = r[o], c = s.instance, l = s.currentTarget, s = s.listener, c !== a && i.isPropagationStopped()) break a;
					gi(i, s, l), a = c;
				}
			}
		}
		if (pt) throw e = mt, pt = !1, mt = null, e;
	}
	function A(e, t) {
		var n = t[qi];
		n === void 0 && (n = t[qi] = /* @__PURE__ */ new Set());
		var r = e + "__bubble";
		n.has(r) || (xi(t, e, 2, !1), n.add(r));
	}
	function vi(e, t, n) {
		var r = 0;
		t && (r |= 4), xi(n, e, r, t);
	}
	var yi = "_reactListening" + Math.random().toString(36).slice(2);
	function bi(e) {
		if (!e[yi]) {
			e[yi] = !0, i.forEach(function(t) {
				t !== "selectionchange" && (hi.has(t) || vi(t, !1, e), vi(t, !0, e));
			});
			var t = e.nodeType === 9 ? e : e.ownerDocument;
			t === null || t[yi] || (t[yi] = !0, vi("selectionchange", !1, t));
		}
	}
	function xi(e, t, n, r) {
		switch (An(t)) {
			case 1:
				var i = Tn;
				break;
			case 4:
				i = En;
				break;
			default: i = Dn;
		}
		n = i.bind(null, t, n, e), i = void 0, !ct || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (i = !0), r ? i === void 0 ? e.addEventListener(t, n, !0) : e.addEventListener(t, n, {
			capture: !0,
			passive: i
		}) : i === void 0 ? e.addEventListener(t, n, !1) : e.addEventListener(t, n, { passive: i });
	}
	function Si(e, t, n, r, i) {
		var a = r;
		if (!(t & 1) && !(t & 2) && r !== null) a: for (;;) {
			if (r === null) return;
			var o = r.tag;
			if (o === 3 || o === 4) {
				var s = r.stateNode.containerInfo;
				if (s === i || s.nodeType === 8 && s.parentNode === i) break;
				if (o === 4) for (o = r.return; o !== null;) {
					var c = o.tag;
					if ((c === 3 || c === 4) && (c = o.stateNode.containerInfo, c === i || c.nodeType === 8 && c.parentNode === i)) return;
					o = o.return;
				}
				for (; s !== null;) {
					if (o = Xi(s), o === null) return;
					if (c = o.tag, c === 5 || c === 6) {
						r = a = o;
						continue a;
					}
					s = s.parentNode;
				}
			}
			r = r.return;
		}
		ot(function() {
			var r = a, i = Xe(n), o = [];
			a: {
				var s = li.get(e);
				if (s !== void 0) {
					var c = Bn, l = e;
					switch (e) {
						case "keypress": if (Fn(n) === 0) break a;
						case "keydown":
						case "keyup":
							c = ir;
							break;
						case "focusin":
							l = "focus", c = Yn;
							break;
						case "focusout":
							l = "blur", c = Yn;
							break;
						case "beforeblur":
						case "afterblur":
							c = Yn;
							break;
						case "click": if (n.button === 2) break a;
						case "auxclick":
						case "dblclick":
						case "mousedown":
						case "mousemove":
						case "mouseup":
						case "mouseout":
						case "mouseover":
						case "contextmenu":
							c = qn;
							break;
						case "drag":
						case "dragend":
						case "dragenter":
						case "dragexit":
						case "dragleave":
						case "dragover":
						case "dragstart":
						case "drop":
							c = Jn;
							break;
						case "touchcancel":
						case "touchend":
						case "touchmove":
						case "touchstart":
							c = or;
							break;
						case ai:
						case oi:
						case si:
							c = Xn;
							break;
						case ci:
							c = sr;
							break;
						case "scroll":
							c = Hn;
							break;
						case "wheel":
							c = cr;
							break;
						case "copy":
						case "cut":
						case "paste":
							c = Zn;
							break;
						case "gotpointercapture":
						case "lostpointercapture":
						case "pointercancel":
						case "pointerdown":
						case "pointermove":
						case "pointerout":
						case "pointerover":
						case "pointerup": c = ar;
					}
					var u = (t & 4) != 0, d = !u && e === "scroll", f = u ? s === null ? null : s + "Capture" : s;
					u = [];
					for (var p = r, m; p !== null;) {
						m = p;
						var h = m.stateNode;
						if (m.tag === 5 && h !== null && (m = h, f !== null && (h = st(p, f), h != null && u.push(Ci(p, h, m)))), d) break;
						p = p.return;
					}
					0 < u.length && (s = new c(s, l, null, n, i), o.push({
						event: s,
						listeners: u
					}));
				}
			}
			if (!(t & 7)) {
				a: {
					if (s = e === "mouseover" || e === "pointerover", c = e === "mouseout" || e === "pointerout", s && n !== Ye && (l = n.relatedTarget || n.fromElement) && (Xi(l) || l[Ki])) break a;
					if ((c || s) && (s = i.window === i ? i : (s = i.ownerDocument) ? s.defaultView || s.parentWindow : window, c ? (l = n.relatedTarget || n.toElement, c = r, l = l ? Xi(l) : null, l !== null && (d = vt(l), l !== d || l.tag !== 5 && l.tag !== 6) && (l = null)) : (c = null, l = r), c !== l)) {
						if (u = qn, h = "onMouseLeave", f = "onMouseEnter", p = "mouse", (e === "pointerout" || e === "pointerover") && (u = ar, h = "onPointerLeave", f = "onPointerEnter", p = "pointer"), d = c == null ? s : Qi(c), m = l == null ? s : Qi(l), s = new u(h, p + "leave", c, n, i), s.target = d, s.relatedTarget = m, h = null, Xi(i) === r && (u = new u(f, p + "enter", l, n, i), u.target = m, u.relatedTarget = d, h = u), d = h, c && l) b: {
							for (u = c, f = l, p = 0, m = u; m; m = Ti(m)) p++;
							for (m = 0, h = f; h; h = Ti(h)) m++;
							for (; 0 < p - m;) u = Ti(u), p--;
							for (; 0 < m - p;) f = Ti(f), m--;
							for (; p--;) {
								if (u === f || f !== null && u === f.alternate) break b;
								u = Ti(u), f = Ti(f);
							}
							u = null;
						}
						else u = null;
						c !== null && Ei(o, s, c, u, !1), l !== null && d !== null && Ei(o, d, l, u, !0);
					}
				}
				a: {
					if (s = r ? Qi(r) : window, c = s.nodeName && s.nodeName.toLowerCase(), c === "select" || c === "input" && s.type === "file") var g = Or;
					else if (Sr(s)) if (kr) g = Rr;
					else {
						g = Ir;
						var _ = Fr;
					}
					else (c = s.nodeName) && c.toLowerCase() === "input" && (s.type === "checkbox" || s.type === "radio") && (g = Lr);
					if (g &&= g(e, r)) {
						Cr(o, g, n, i);
						break a;
					}
					_ && _(e, s, r), e === "focusout" && (_ = s._wrapperState) && _.controlled && s.type === "number" && Ae(s, "number", s.value);
				}
				switch (_ = r ? Qi(r) : window, e) {
					case "focusin":
						(Sr(_) || _.contentEditable === "true") && (Yr = _, Xr = r, Zr = null);
						break;
					case "focusout":
						Zr = Xr = Yr = null;
						break;
					case "mousedown":
						Qr = !0;
						break;
					case "contextmenu":
					case "mouseup":
					case "dragend":
						Qr = !1, $r(o, n, i);
						break;
					case "selectionchange": if (Jr) break;
					case "keydown":
					case "keyup": $r(o, n, i);
				}
				var v;
				if (ur) b: {
					switch (e) {
						case "compositionstart":
							var y = "onCompositionStart";
							break b;
						case "compositionend":
							y = "onCompositionEnd";
							break b;
						case "compositionupdate":
							y = "onCompositionUpdate";
							break b;
					}
					y = void 0;
				}
				else vr ? gr(e, n) && (y = "onCompositionEnd") : e === "keydown" && n.keyCode === 229 && (y = "onCompositionStart");
				y && (pr && n.locale !== "ko" && (vr || y !== "onCompositionStart" ? y === "onCompositionEnd" && vr && (v = Pn()) : (jn = i, Mn = "value" in jn ? jn.value : jn.textContent, vr = !0)), _ = wi(r, y), 0 < _.length && (y = new Qn(y, e, null, n, i), o.push({
					event: y,
					listeners: _
				}), v ? y.data = v : (v = _r(n), v !== null && (y.data = v)))), (v = fr ? yr(e, n) : br(e, n)) && (r = wi(r, "onBeforeInput"), 0 < r.length && (i = new Qn("onBeforeInput", "beforeinput", null, n, i), o.push({
					event: i,
					listeners: r
				}), i.data = v));
			}
			_i(o, t);
		});
	}
	function Ci(e, t, n) {
		return {
			instance: e,
			listener: t,
			currentTarget: n
		};
	}
	function wi(e, t) {
		for (var n = t + "Capture", r = []; e !== null;) {
			var i = e, a = i.stateNode;
			i.tag === 5 && a !== null && (i = a, a = st(e, n), a != null && r.unshift(Ci(e, a, i)), a = st(e, t), a != null && r.push(Ci(e, a, i))), e = e.return;
		}
		return r;
	}
	function Ti(e) {
		if (e === null) return null;
		do
			e = e.return;
		while (e && e.tag !== 5);
		return e || null;
	}
	function Ei(e, t, n, r, i) {
		for (var a = t._reactName, o = []; n !== null && n !== r;) {
			var s = n, c = s.alternate, l = s.stateNode;
			if (c !== null && c === r) break;
			s.tag === 5 && l !== null && (s = l, i ? (c = st(n, a), c != null && o.unshift(Ci(n, c, s))) : i || (c = st(n, a), c != null && o.push(Ci(n, c, s)))), n = n.return;
		}
		o.length !== 0 && e.push({
			event: t,
			listeners: o
		});
	}
	var Di = /\r\n?/g, Oi = /\u0000|\uFFFD/g;
	function ki(e) {
		return (typeof e == "string" ? e : "" + e).replace(Di, "\n").replace(Oi, "");
	}
	function Ai(e, t, n) {
		if (t = ki(t), ki(e) !== t && n) throw Error(r(425));
	}
	function ji() {}
	var Mi = null, Ni = null;
	function Pi(e, t) {
		return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
	}
	var Fi = typeof setTimeout == "function" ? setTimeout : void 0, Ii = typeof clearTimeout == "function" ? clearTimeout : void 0, Li = typeof Promise == "function" ? Promise : void 0, Ri = typeof queueMicrotask == "function" ? queueMicrotask : Li === void 0 ? Fi : function(e) {
		return Li.resolve(null).then(e).catch(zi);
	};
	function zi(e) {
		setTimeout(function() {
			throw e;
		});
	}
	function Bi(e, t) {
		var n = t, r = 0;
		do {
			var i = n.nextSibling;
			if (e.removeChild(n), i && i.nodeType === 8) if (n = i.data, n === "/$") {
				if (r === 0) {
					e.removeChild(i), Sn(t);
					return;
				}
				r--;
			} else n !== "$" && n !== "$?" && n !== "$!" || r++;
			n = i;
		} while (n);
		Sn(t);
	}
	function Vi(e) {
		for (; e != null; e = e.nextSibling) {
			var t = e.nodeType;
			if (t === 1 || t === 3) break;
			if (t === 8) {
				if (t = e.data, t === "$" || t === "$!" || t === "$?") break;
				if (t === "/$") return null;
			}
		}
		return e;
	}
	function Hi(e) {
		e = e.previousSibling;
		for (var t = 0; e;) {
			if (e.nodeType === 8) {
				var n = e.data;
				if (n === "$" || n === "$!" || n === "$?") {
					if (t === 0) return e;
					t--;
				} else n === "/$" && t++;
			}
			e = e.previousSibling;
		}
		return null;
	}
	var Ui = Math.random().toString(36).slice(2), Wi = "__reactFiber$" + Ui, Gi = "__reactProps$" + Ui, Ki = "__reactContainer$" + Ui, qi = "__reactEvents$" + Ui, Ji = "__reactListeners$" + Ui, Yi = "__reactHandles$" + Ui;
	function Xi(e) {
		var t = e[Wi];
		if (t) return t;
		for (var n = e.parentNode; n;) {
			if (t = n[Ki] || n[Wi]) {
				if (n = t.alternate, t.child !== null || n !== null && n.child !== null) for (e = Hi(e); e !== null;) {
					if (n = e[Wi]) return n;
					e = Hi(e);
				}
				return t;
			}
			e = n, n = e.parentNode;
		}
		return null;
	}
	function Zi(e) {
		return e = e[Wi] || e[Ki], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
	}
	function Qi(e) {
		if (e.tag === 5 || e.tag === 6) return e.stateNode;
		throw Error(r(33));
	}
	function $i(e) {
		return e[Gi] || null;
	}
	var ea = [], ta = -1;
	function na(e) {
		return { current: e };
	}
	function j(e) {
		0 > ta || (e.current = ea[ta], ea[ta] = null, ta--);
	}
	function M(e, t) {
		ta++, ea[ta] = e.current, e.current = t;
	}
	var ra = {}, N = na(ra), ia = na(!1), aa = ra;
	function oa(e, t) {
		var n = e.type.contextTypes;
		if (!n) return ra;
		var r = e.stateNode;
		if (r && r.__reactInternalMemoizedUnmaskedChildContext === t) return r.__reactInternalMemoizedMaskedChildContext;
		var i = {}, a;
		for (a in n) i[a] = t[a];
		return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = t, e.__reactInternalMemoizedMaskedChildContext = i), i;
	}
	function sa(e) {
		return e = e.childContextTypes, e != null;
	}
	function ca() {
		j(ia), j(N);
	}
	function la(e, t, n) {
		if (N.current !== ra) throw Error(r(168));
		M(N, t), M(ia, n);
	}
	function ua(e, t, n) {
		var i = e.stateNode;
		if (t = t.childContextTypes, typeof i.getChildContext != "function") return n;
		for (var a in i = i.getChildContext(), i) if (!(a in t)) throw Error(r(108, ve(e) || "Unknown", a));
		return T({}, n, i);
	}
	function da(e) {
		return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || ra, aa = N.current, M(N, e), M(ia, ia.current), !0;
	}
	function fa(e, t, n) {
		var i = e.stateNode;
		if (!i) throw Error(r(169));
		n ? (e = ua(e, t, aa), i.__reactInternalMemoizedMergedChildContext = e, j(ia), j(N), M(N, e)) : j(ia), M(ia, n);
	}
	var pa = null, ma = !1, ha = !1;
	function ga(e) {
		pa === null ? pa = [e] : pa.push(e);
	}
	function _a(e) {
		ma = !0, ga(e);
	}
	function va() {
		if (!ha && pa !== null) {
			ha = !0;
			var e = 0, t = k;
			try {
				var n = pa;
				for (k = 1; e < n.length; e++) {
					var r = n[e];
					do
						r = r(!0);
					while (r !== null);
				}
				pa = null, ma = !1;
			} catch (t) {
				throw pa !== null && (pa = pa.slice(e + 1)), wt(At, va), t;
			} finally {
				k = t, ha = !1;
			}
		}
		return null;
	}
	var ya = [], ba = 0, xa = null, Sa = 0, Ca = [], wa = 0, Ta = null, Ea = 1, Da = "";
	function Oa(e, t) {
		ya[ba++] = Sa, ya[ba++] = xa, xa = e, Sa = t;
	}
	function ka(e, t, n) {
		Ca[wa++] = Ea, Ca[wa++] = Da, Ca[wa++] = Ta, Ta = e;
		var r = Ea;
		e = Da;
		var i = 32 - O(r) - 1;
		r &= ~(1 << i), n += 1;
		var a = 32 - O(t) + i;
		if (30 < a) {
			var o = i - i % 5;
			a = (r & (1 << o) - 1).toString(32), r >>= o, i -= o, Ea = 1 << 32 - O(t) + i | n << i | r, Da = a + e;
		} else Ea = 1 << a | n << i | r, Da = e;
	}
	function Aa(e) {
		e.return !== null && (Oa(e, 1), ka(e, 1, 0));
	}
	function ja(e) {
		for (; e === xa;) xa = ya[--ba], ya[ba] = null, Sa = ya[--ba], ya[ba] = null;
		for (; e === Ta;) Ta = Ca[--wa], Ca[wa] = null, Da = Ca[--wa], Ca[wa] = null, Ea = Ca[--wa], Ca[wa] = null;
	}
	var Ma = null, Na = null, P = !1, Pa = null;
	function Fa(e, t) {
		var n = Yl(5, null, null, 0);
		n.elementType = "DELETED", n.stateNode = t, n.return = e, t = e.deletions, t === null ? (e.deletions = [n], e.flags |= 16) : t.push(n);
	}
	function Ia(e, t) {
		switch (e.tag) {
			case 5:
				var n = e.type;
				return t = t.nodeType !== 1 || n.toLowerCase() !== t.nodeName.toLowerCase() ? null : t, t === null ? !1 : (e.stateNode = t, Ma = e, Na = Vi(t.firstChild), !0);
			case 6: return t = e.pendingProps === "" || t.nodeType !== 3 ? null : t, t === null ? !1 : (e.stateNode = t, Ma = e, Na = null, !0);
			case 13: return t = t.nodeType === 8 ? t : null, t === null ? !1 : (n = Ta === null ? null : {
				id: Ea,
				overflow: Da
			}, e.memoizedState = {
				dehydrated: t,
				treeContext: n,
				retryLane: 1073741824
			}, n = Yl(18, null, null, 0), n.stateNode = t, n.return = e, e.child = n, Ma = e, Na = null, !0);
			default: return !1;
		}
	}
	function La(e) {
		return (e.mode & 1) != 0 && (e.flags & 128) == 0;
	}
	function Ra(e) {
		if (P) {
			var t = Na;
			if (t) {
				var n = t;
				if (!Ia(e, t)) {
					if (La(e)) throw Error(r(418));
					t = Vi(n.nextSibling);
					var i = Ma;
					t && Ia(e, t) ? Fa(i, n) : (e.flags = e.flags & -4097 | 2, P = !1, Ma = e);
				}
			} else {
				if (La(e)) throw Error(r(418));
				e.flags = e.flags & -4097 | 2, P = !1, Ma = e;
			}
		}
	}
	function za(e) {
		for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13;) e = e.return;
		Ma = e;
	}
	function Ba(e) {
		if (e !== Ma) return !1;
		if (!P) return za(e), P = !0, !1;
		var t;
		if ((t = e.tag !== 3) && !(t = e.tag !== 5) && (t = e.type, t = t !== "head" && t !== "body" && !Pi(e.type, e.memoizedProps)), t &&= Na) {
			if (La(e)) throw Va(), Error(r(418));
			for (; t;) Fa(e, t), t = Vi(t.nextSibling);
		}
		if (za(e), e.tag === 13) {
			if (e = e.memoizedState, e = e === null ? null : e.dehydrated, !e) throw Error(r(317));
			a: {
				for (e = e.nextSibling, t = 0; e;) {
					if (e.nodeType === 8) {
						var n = e.data;
						if (n === "/$") {
							if (t === 0) {
								Na = Vi(e.nextSibling);
								break a;
							}
							t--;
						} else n !== "$" && n !== "$!" && n !== "$?" || t++;
					}
					e = e.nextSibling;
				}
				Na = null;
			}
		} else Na = Ma ? Vi(e.stateNode.nextSibling) : null;
		return !0;
	}
	function Va() {
		for (var e = Na; e;) e = Vi(e.nextSibling);
	}
	function Ha() {
		Na = Ma = null, P = !1;
	}
	function Ua(e) {
		Pa === null ? Pa = [e] : Pa.push(e);
	}
	var Wa = x.ReactCurrentBatchConfig;
	function Ga(e, t, n) {
		if (e = n.ref, e !== null && typeof e != "function" && typeof e != "object") {
			if (n._owner) {
				if (n = n._owner, n) {
					if (n.tag !== 1) throw Error(r(309));
					var i = n.stateNode;
				}
				if (!i) throw Error(r(147, e));
				var a = i, o = "" + e;
				return t !== null && t.ref !== null && typeof t.ref == "function" && t.ref._stringRef === o ? t.ref : (t = function(e) {
					var t = a.refs;
					e === null ? delete t[o] : t[o] = e;
				}, t._stringRef = o, t);
			}
			if (typeof e != "string") throw Error(r(284));
			if (!n._owner) throw Error(r(290, e));
		}
		return e;
	}
	function Ka(e, t) {
		throw e = Object.prototype.toString.call(t), Error(r(31, e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e));
	}
	function qa(e) {
		var t = e._init;
		return t(e._payload);
	}
	function Ja(e) {
		function t(t, n) {
			if (e) {
				var r = t.deletions;
				r === null ? (t.deletions = [n], t.flags |= 16) : r.push(n);
			}
		}
		function n(n, r) {
			if (!e) return null;
			for (; r !== null;) t(n, r), r = r.sibling;
			return null;
		}
		function i(e, t) {
			for (e = /* @__PURE__ */ new Map(); t !== null;) t.key === null ? e.set(t.index, t) : e.set(t.key, t), t = t.sibling;
			return e;
		}
		function a(e, t) {
			return e = Ql(e, t), e.index = 0, e.sibling = null, e;
		}
		function o(t, n, r) {
			return t.index = r, e ? (r = t.alternate, r === null ? (t.flags |= 2, n) : (r = r.index, r < n ? (t.flags |= 2, n) : r)) : (t.flags |= 1048576, n);
		}
		function s(t) {
			return e && t.alternate === null && (t.flags |= 2), t;
		}
		function c(e, t, n, r) {
			return t === null || t.tag !== 6 ? (t = nu(n, e.mode, r), t.return = e, t) : (t = a(t, n), t.return = e, t);
		}
		function l(e, t, n, r) {
			var i = n.type;
			return i === S ? d(e, t, n.props.children, r, n.key) : t !== null && (t.elementType === i || typeof i == "object" && i && i.$$typeof === le && qa(i) === t.type) ? (r = a(t, n.props), r.ref = Ga(e, t, n), r.return = e, r) : (r = $l(n.type, n.key, n.props, null, e.mode, r), r.ref = Ga(e, t, n), r.return = e, r);
		}
		function u(e, t, n, r) {
			return t === null || t.tag !== 4 || t.stateNode.containerInfo !== n.containerInfo || t.stateNode.implementation !== n.implementation ? (t = ru(n, e.mode, r), t.return = e, t) : (t = a(t, n.children || []), t.return = e, t);
		}
		function d(e, t, n, r, i) {
			return t === null || t.tag !== 7 ? (t = eu(n, e.mode, r, i), t.return = e, t) : (t = a(t, n), t.return = e, t);
		}
		function f(e, t, n) {
			if (typeof t == "string" && t !== "" || typeof t == "number") return t = nu("" + t, e.mode, n), t.return = e, t;
			if (typeof t == "object" && t) {
				switch (t.$$typeof) {
					case ee: return n = $l(t.type, t.key, t.props, null, e.mode, n), n.ref = Ga(e, null, t), n.return = e, n;
					case te: return t = ru(t, e.mode, n), t.return = e, t;
					case le:
						var r = t._init;
						return f(e, r(t._payload), n);
				}
				if (je(t) || de(t)) return t = eu(t, e.mode, n, null), t.return = e, t;
				Ka(e, t);
			}
			return null;
		}
		function p(e, t, n, r) {
			var i = t === null ? null : t.key;
			if (typeof n == "string" && n !== "" || typeof n == "number") return i === null ? c(e, t, "" + n, r) : null;
			if (typeof n == "object" && n) {
				switch (n.$$typeof) {
					case ee: return n.key === i ? l(e, t, n, r) : null;
					case te: return n.key === i ? u(e, t, n, r) : null;
					case le: return i = n._init, p(e, t, i(n._payload), r);
				}
				if (je(n) || de(n)) return i === null ? d(e, t, n, r, null) : null;
				Ka(e, n);
			}
			return null;
		}
		function m(e, t, n, r, i) {
			if (typeof r == "string" && r !== "" || typeof r == "number") return e = e.get(n) || null, c(t, e, "" + r, i);
			if (typeof r == "object" && r) {
				switch (r.$$typeof) {
					case ee: return e = e.get(r.key === null ? n : r.key) || null, l(t, e, r, i);
					case te: return e = e.get(r.key === null ? n : r.key) || null, u(t, e, r, i);
					case le:
						var a = r._init;
						return m(e, t, n, a(r._payload), i);
				}
				if (je(r) || de(r)) return e = e.get(n) || null, d(t, e, r, i, null);
				Ka(t, r);
			}
			return null;
		}
		function h(r, a, s, c) {
			for (var l = null, u = null, d = a, h = a = 0, g = null; d !== null && h < s.length; h++) {
				d.index > h ? (g = d, d = null) : g = d.sibling;
				var _ = p(r, d, s[h], c);
				if (_ === null) {
					d === null && (d = g);
					break;
				}
				e && d && _.alternate === null && t(r, d), a = o(_, a, h), u === null ? l = _ : u.sibling = _, u = _, d = g;
			}
			if (h === s.length) return n(r, d), P && Oa(r, h), l;
			if (d === null) {
				for (; h < s.length; h++) d = f(r, s[h], c), d !== null && (a = o(d, a, h), u === null ? l = d : u.sibling = d, u = d);
				return P && Oa(r, h), l;
			}
			for (d = i(r, d); h < s.length; h++) g = m(d, r, h, s[h], c), g !== null && (e && g.alternate !== null && d.delete(g.key === null ? h : g.key), a = o(g, a, h), u === null ? l = g : u.sibling = g, u = g);
			return e && d.forEach(function(e) {
				return t(r, e);
			}), P && Oa(r, h), l;
		}
		function g(a, s, c, l) {
			var u = de(c);
			if (typeof u != "function") throw Error(r(150));
			if (c = u.call(c), c == null) throw Error(r(151));
			for (var d = u = null, h = s, g = s = 0, _ = null, v = c.next(); h !== null && !v.done; g++, v = c.next()) {
				h.index > g ? (_ = h, h = null) : _ = h.sibling;
				var y = p(a, h, v.value, l);
				if (y === null) {
					h === null && (h = _);
					break;
				}
				e && h && y.alternate === null && t(a, h), s = o(y, s, g), d === null ? u = y : d.sibling = y, d = y, h = _;
			}
			if (v.done) return n(a, h), P && Oa(a, g), u;
			if (h === null) {
				for (; !v.done; g++, v = c.next()) v = f(a, v.value, l), v !== null && (s = o(v, s, g), d === null ? u = v : d.sibling = v, d = v);
				return P && Oa(a, g), u;
			}
			for (h = i(a, h); !v.done; g++, v = c.next()) v = m(h, a, g, v.value, l), v !== null && (e && v.alternate !== null && h.delete(v.key === null ? g : v.key), s = o(v, s, g), d === null ? u = v : d.sibling = v, d = v);
			return e && h.forEach(function(e) {
				return t(a, e);
			}), P && Oa(a, g), u;
		}
		function _(e, r, i, o) {
			if (typeof i == "object" && i && i.type === S && i.key === null && (i = i.props.children), typeof i == "object" && i) {
				switch (i.$$typeof) {
					case ee:
						a: {
							for (var c = i.key, l = r; l !== null;) {
								if (l.key === c) {
									if (c = i.type, c === S) {
										if (l.tag === 7) {
											n(e, l.sibling), r = a(l, i.props.children), r.return = e, e = r;
											break a;
										}
									} else if (l.elementType === c || typeof c == "object" && c && c.$$typeof === le && qa(c) === l.type) {
										n(e, l.sibling), r = a(l, i.props), r.ref = Ga(e, l, i), r.return = e, e = r;
										break a;
									}
									n(e, l);
									break;
								} else t(e, l);
								l = l.sibling;
							}
							i.type === S ? (r = eu(i.props.children, e.mode, o, i.key), r.return = e, e = r) : (o = $l(i.type, i.key, i.props, null, e.mode, o), o.ref = Ga(e, r, i), o.return = e, e = o);
						}
						return s(e);
					case te:
						a: {
							for (l = i.key; r !== null;) {
								if (r.key === l) if (r.tag === 4 && r.stateNode.containerInfo === i.containerInfo && r.stateNode.implementation === i.implementation) {
									n(e, r.sibling), r = a(r, i.children || []), r.return = e, e = r;
									break a;
								} else {
									n(e, r);
									break;
								}
								else t(e, r);
								r = r.sibling;
							}
							r = ru(i, e.mode, o), r.return = e, e = r;
						}
						return s(e);
					case le: return l = i._init, _(e, r, l(i._payload), o);
				}
				if (je(i)) return h(e, r, i, o);
				if (de(i)) return g(e, r, i, o);
				Ka(e, i);
			}
			return typeof i == "string" && i !== "" || typeof i == "number" ? (i = "" + i, r !== null && r.tag === 6 ? (n(e, r.sibling), r = a(r, i), r.return = e, e = r) : (n(e, r), r = nu(i, e.mode, o), r.return = e, e = r), s(e)) : n(e, r);
		}
		return _;
	}
	var Ya = Ja(!0), Xa = Ja(!1), Za = na(null), Qa = null, $a = null, eo = null;
	function to() {
		eo = $a = Qa = null;
	}
	function no(e) {
		var t = Za.current;
		j(Za), e._currentValue = t;
	}
	function ro(e, t, n) {
		for (; e !== null;) {
			var r = e.alternate;
			if ((e.childLanes & t) === t ? r !== null && (r.childLanes & t) !== t && (r.childLanes |= t) : (e.childLanes |= t, r !== null && (r.childLanes |= t)), e === n) break;
			e = e.return;
		}
	}
	function io(e, t) {
		Qa = e, eo = $a = null, e = e.dependencies, e !== null && e.firstContext !== null && ((e.lanes & t) !== 0 && (Us = !0), e.firstContext = null);
	}
	function ao(e) {
		var t = e._currentValue;
		if (eo !== e) if (e = {
			context: e,
			memoizedValue: t,
			next: null
		}, $a === null) {
			if (Qa === null) throw Error(r(308));
			$a = e, Qa.dependencies = {
				lanes: 0,
				firstContext: e
			};
		} else $a = $a.next = e;
		return t;
	}
	var oo = null;
	function so(e) {
		oo === null ? oo = [e] : oo.push(e);
	}
	function co(e, t, n, r) {
		var i = t.interleaved;
		return i === null ? (n.next = n, so(t)) : (n.next = i.next, i.next = n), t.interleaved = n, lo(e, r);
	}
	function lo(e, t) {
		e.lanes |= t;
		var n = e.alternate;
		for (n !== null && (n.lanes |= t), n = e, e = e.return; e !== null;) e.childLanes |= t, n = e.alternate, n !== null && (n.childLanes |= t), n = e, e = e.return;
		return n.tag === 3 ? n.stateNode : null;
	}
	var uo = !1;
	function fo(e) {
		e.updateQueue = {
			baseState: e.memoizedState,
			firstBaseUpdate: null,
			lastBaseUpdate: null,
			shared: {
				pending: null,
				interleaved: null,
				lanes: 0
			},
			effects: null
		};
	}
	function po(e, t) {
		e = e.updateQueue, t.updateQueue === e && (t.updateQueue = {
			baseState: e.baseState,
			firstBaseUpdate: e.firstBaseUpdate,
			lastBaseUpdate: e.lastBaseUpdate,
			shared: e.shared,
			effects: e.effects
		});
	}
	function mo(e, t) {
		return {
			eventTime: e,
			lane: t,
			tag: 0,
			payload: null,
			callback: null,
			next: null
		};
	}
	function ho(e, t, n) {
		var r = e.updateQueue;
		if (r === null) return null;
		if (r = r.shared, W & 2) {
			var i = r.pending;
			return i === null ? t.next = t : (t.next = i.next, i.next = t), r.pending = t, lo(e, n);
		}
		return i = r.interleaved, i === null ? (t.next = t, so(r)) : (t.next = i.next, i.next = t), r.interleaved = t, lo(e, n);
	}
	function go(e, t, n) {
		if (t = t.updateQueue, t !== null && (t = t.shared, n & 4194240)) {
			var r = t.lanes;
			r &= e.pendingLanes, n |= r, t.lanes = n, Zt(e, n);
		}
	}
	function _o(e, t) {
		var n = e.updateQueue, r = e.alternate;
		if (r !== null && (r = r.updateQueue, n === r)) {
			var i = null, a = null;
			if (n = n.firstBaseUpdate, n !== null) {
				do {
					var o = {
						eventTime: n.eventTime,
						lane: n.lane,
						tag: n.tag,
						payload: n.payload,
						callback: n.callback,
						next: null
					};
					a === null ? i = a = o : a = a.next = o, n = n.next;
				} while (n !== null);
				a === null ? i = a = t : a = a.next = t;
			} else i = a = t;
			n = {
				baseState: r.baseState,
				firstBaseUpdate: i,
				lastBaseUpdate: a,
				shared: r.shared,
				effects: r.effects
			}, e.updateQueue = n;
			return;
		}
		e = n.lastBaseUpdate, e === null ? n.firstBaseUpdate = t : e.next = t, n.lastBaseUpdate = t;
	}
	function vo(e, t, n, r) {
		var i = e.updateQueue;
		uo = !1;
		var a = i.firstBaseUpdate, o = i.lastBaseUpdate, s = i.shared.pending;
		if (s !== null) {
			i.shared.pending = null;
			var c = s, l = c.next;
			c.next = null, o === null ? a = l : o.next = l, o = c;
			var u = e.alternate;
			u !== null && (u = u.updateQueue, s = u.lastBaseUpdate, s !== o && (s === null ? u.firstBaseUpdate = l : s.next = l, u.lastBaseUpdate = c));
		}
		if (a !== null) {
			var d = i.baseState;
			o = 0, u = l = c = null, s = a;
			do {
				var f = s.lane, p = s.eventTime;
				if ((r & f) === f) {
					u !== null && (u = u.next = {
						eventTime: p,
						lane: 0,
						tag: s.tag,
						payload: s.payload,
						callback: s.callback,
						next: null
					});
					a: {
						var m = e, h = s;
						switch (f = t, p = n, h.tag) {
							case 1:
								if (m = h.payload, typeof m == "function") {
									d = m.call(p, d, f);
									break a;
								}
								d = m;
								break a;
							case 3: m.flags = m.flags & -65537 | 128;
							case 0:
								if (m = h.payload, f = typeof m == "function" ? m.call(p, d, f) : m, f == null) break a;
								d = T({}, d, f);
								break a;
							case 2: uo = !0;
						}
					}
					s.callback !== null && s.lane !== 0 && (e.flags |= 64, f = i.effects, f === null ? i.effects = [s] : f.push(s));
				} else p = {
					eventTime: p,
					lane: f,
					tag: s.tag,
					payload: s.payload,
					callback: s.callback,
					next: null
				}, u === null ? (l = u = p, c = d) : u = u.next = p, o |= f;
				if (s = s.next, s === null) {
					if (s = i.shared.pending, s === null) break;
					f = s, s = f.next, f.next = null, i.lastBaseUpdate = f, i.shared.pending = null;
				}
			} while (1);
			if (u === null && (c = d), i.baseState = c, i.firstBaseUpdate = l, i.lastBaseUpdate = u, t = i.shared.interleaved, t !== null) {
				i = t;
				do
					o |= i.lane, i = i.next;
				while (i !== t);
			} else a === null && (i.shared.lanes = 0);
			Qc |= o, e.lanes = o, e.memoizedState = d;
		}
	}
	function yo(e, t, n) {
		if (e = t.effects, t.effects = null, e !== null) for (t = 0; t < e.length; t++) {
			var i = e[t], a = i.callback;
			if (a !== null) {
				if (i.callback = null, i = n, typeof a != "function") throw Error(r(191, a));
				a.call(i);
			}
		}
	}
	var bo = {}, xo = na(bo), So = na(bo), Co = na(bo);
	function wo(e) {
		if (e === bo) throw Error(r(174));
		return e;
	}
	function To(e, t) {
		switch (M(Co, t), M(So, e), M(xo, bo), e = t.nodeType, e) {
			case 9:
			case 11:
				t = (t = t.documentElement) ? t.namespaceURI : Re(null, "");
				break;
			default: e = e === 8 ? t.parentNode : t, t = e.namespaceURI || null, e = e.tagName, t = Re(t, e);
		}
		j(xo), M(xo, t);
	}
	function Eo() {
		j(xo), j(So), j(Co);
	}
	function Do(e) {
		wo(Co.current);
		var t = wo(xo.current), n = Re(t, e.type);
		t !== n && (M(So, e), M(xo, n));
	}
	function Oo(e) {
		So.current === e && (j(xo), j(So));
	}
	var F = na(0);
	function ko(e) {
		for (var t = e; t !== null;) {
			if (t.tag === 13) {
				var n = t.memoizedState;
				if (n !== null && (n = n.dehydrated, n === null || n.data === "$?" || n.data === "$!")) return t;
			} else if (t.tag === 19 && t.memoizedProps.revealOrder !== void 0) {
				if (t.flags & 128) return t;
			} else if (t.child !== null) {
				t.child.return = t, t = t.child;
				continue;
			}
			if (t === e) break;
			for (; t.sibling === null;) {
				if (t.return === null || t.return === e) return null;
				t = t.return;
			}
			t.sibling.return = t.return, t = t.sibling;
		}
		return null;
	}
	var Ao = [];
	function jo() {
		for (var e = 0; e < Ao.length; e++) Ao[e]._workInProgressVersionPrimary = null;
		Ao.length = 0;
	}
	var Mo = x.ReactCurrentDispatcher, No = x.ReactCurrentBatchConfig, Po = 0, I = null, L = null, R = null, Fo = !1, Io = !1, Lo = 0, Ro = 0;
	function z() {
		throw Error(r(321));
	}
	function zo(e, t) {
		if (t === null) return !1;
		for (var n = 0; n < t.length && n < e.length; n++) if (!Br(e[n], t[n])) return !1;
		return !0;
	}
	function Bo(e, t, n, i, a, o) {
		if (Po = o, I = t, t.memoizedState = null, t.updateQueue = null, t.lanes = 0, Mo.current = e === null || e.memoizedState === null ? Cs : ws, e = n(i, a), Io) {
			o = 0;
			do {
				if (Io = !1, Lo = 0, 25 <= o) throw Error(r(301));
				o += 1, R = L = null, t.updateQueue = null, Mo.current = Ts, e = n(i, a);
			} while (Io);
		}
		if (Mo.current = Ss, t = L !== null && L.next !== null, Po = 0, R = L = I = null, Fo = !1, t) throw Error(r(300));
		return e;
	}
	function Vo() {
		var e = Lo !== 0;
		return Lo = 0, e;
	}
	function Ho() {
		var e = {
			memoizedState: null,
			baseState: null,
			baseQueue: null,
			queue: null,
			next: null
		};
		return R === null ? I.memoizedState = R = e : R = R.next = e, R;
	}
	function Uo() {
		if (L === null) {
			var e = I.alternate;
			e = e === null ? null : e.memoizedState;
		} else e = L.next;
		var t = R === null ? I.memoizedState : R.next;
		if (t !== null) R = t, L = e;
		else {
			if (e === null) throw Error(r(310));
			L = e, e = {
				memoizedState: L.memoizedState,
				baseState: L.baseState,
				baseQueue: L.baseQueue,
				queue: L.queue,
				next: null
			}, R === null ? I.memoizedState = R = e : R = R.next = e;
		}
		return R;
	}
	function Wo(e, t) {
		return typeof t == "function" ? t(e) : t;
	}
	function Go(e) {
		var t = Uo(), n = t.queue;
		if (n === null) throw Error(r(311));
		n.lastRenderedReducer = e;
		var i = L, a = i.baseQueue, o = n.pending;
		if (o !== null) {
			if (a !== null) {
				var s = a.next;
				a.next = o.next, o.next = s;
			}
			i.baseQueue = a = o, n.pending = null;
		}
		if (a !== null) {
			o = a.next, i = i.baseState;
			var c = s = null, l = null, u = o;
			do {
				var d = u.lane;
				if ((Po & d) === d) l !== null && (l = l.next = {
					lane: 0,
					action: u.action,
					hasEagerState: u.hasEagerState,
					eagerState: u.eagerState,
					next: null
				}), i = u.hasEagerState ? u.eagerState : e(i, u.action);
				else {
					var f = {
						lane: d,
						action: u.action,
						hasEagerState: u.hasEagerState,
						eagerState: u.eagerState,
						next: null
					};
					l === null ? (c = l = f, s = i) : l = l.next = f, I.lanes |= d, Qc |= d;
				}
				u = u.next;
			} while (u !== null && u !== o);
			l === null ? s = i : l.next = c, Br(i, t.memoizedState) || (Us = !0), t.memoizedState = i, t.baseState = s, t.baseQueue = l, n.lastRenderedState = i;
		}
		if (e = n.interleaved, e !== null) {
			a = e;
			do
				o = a.lane, I.lanes |= o, Qc |= o, a = a.next;
			while (a !== e);
		} else a === null && (n.lanes = 0);
		return [t.memoizedState, n.dispatch];
	}
	function Ko(e) {
		var t = Uo(), n = t.queue;
		if (n === null) throw Error(r(311));
		n.lastRenderedReducer = e;
		var i = n.dispatch, a = n.pending, o = t.memoizedState;
		if (a !== null) {
			n.pending = null;
			var s = a = a.next;
			do
				o = e(o, s.action), s = s.next;
			while (s !== a);
			Br(o, t.memoizedState) || (Us = !0), t.memoizedState = o, t.baseQueue === null && (t.baseState = o), n.lastRenderedState = o;
		}
		return [o, i];
	}
	function qo() {}
	function Jo(e, t) {
		var n = I, i = Uo(), a = t(), o = !Br(i.memoizedState, a);
		if (o && (i.memoizedState = a, Us = !0), i = i.queue, os(Zo.bind(null, n, i, e), [e]), i.getSnapshot !== t || o || R !== null && R.memoizedState.tag & 1) {
			if (n.flags |= 2048, ts(9, Xo.bind(null, n, i, a, t), void 0, null), G === null) throw Error(r(349));
			Po & 30 || Yo(n, t, a);
		}
		return a;
	}
	function Yo(e, t, n) {
		e.flags |= 16384, e = {
			getSnapshot: t,
			value: n
		}, t = I.updateQueue, t === null ? (t = {
			lastEffect: null,
			stores: null
		}, I.updateQueue = t, t.stores = [e]) : (n = t.stores, n === null ? t.stores = [e] : n.push(e));
	}
	function Xo(e, t, n, r) {
		t.value = n, t.getSnapshot = r, Qo(t) && $o(e);
	}
	function Zo(e, t, n) {
		return n(function() {
			Qo(t) && $o(e);
		});
	}
	function Qo(e) {
		var t = e.getSnapshot;
		e = e.value;
		try {
			var n = t();
			return !Br(e, n);
		} catch {
			return !0;
		}
	}
	function $o(e) {
		var t = lo(e, 1);
		t !== null && vl(t, e, 1, -1);
	}
	function es(e) {
		var t = Ho();
		return typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e, e = {
			pending: null,
			interleaved: null,
			lanes: 0,
			dispatch: null,
			lastRenderedReducer: Wo,
			lastRenderedState: e
		}, t.queue = e, e = e.dispatch = vs.bind(null, I, e), [t.memoizedState, e];
	}
	function ts(e, t, n, r) {
		return e = {
			tag: e,
			create: t,
			destroy: n,
			deps: r,
			next: null
		}, t = I.updateQueue, t === null ? (t = {
			lastEffect: null,
			stores: null
		}, I.updateQueue = t, t.lastEffect = e.next = e) : (n = t.lastEffect, n === null ? t.lastEffect = e.next = e : (r = n.next, n.next = e, e.next = r, t.lastEffect = e)), e;
	}
	function ns() {
		return Uo().memoizedState;
	}
	function rs(e, t, n, r) {
		var i = Ho();
		I.flags |= e, i.memoizedState = ts(1 | t, n, void 0, r === void 0 ? null : r);
	}
	function is(e, t, n, r) {
		var i = Uo();
		r = r === void 0 ? null : r;
		var a = void 0;
		if (L !== null) {
			var o = L.memoizedState;
			if (a = o.destroy, r !== null && zo(r, o.deps)) {
				i.memoizedState = ts(t, n, a, r);
				return;
			}
		}
		I.flags |= e, i.memoizedState = ts(1 | t, n, a, r);
	}
	function as(e, t) {
		return rs(8390656, 8, e, t);
	}
	function os(e, t) {
		return is(2048, 8, e, t);
	}
	function ss(e, t) {
		return is(4, 2, e, t);
	}
	function cs(e, t) {
		return is(4, 4, e, t);
	}
	function ls(e, t) {
		if (typeof t == "function") return e = e(), t(e), function() {
			t(null);
		};
		if (t != null) return e = e(), t.current = e, function() {
			t.current = null;
		};
	}
	function us(e, t, n) {
		return n = n == null ? null : n.concat([e]), is(4, 4, ls.bind(null, t, e), n);
	}
	function ds() {}
	function fs(e, t) {
		var n = Uo();
		t = t === void 0 ? null : t;
		var r = n.memoizedState;
		return r !== null && t !== null && zo(t, r[1]) ? r[0] : (n.memoizedState = [e, t], e);
	}
	function ps(e, t) {
		var n = Uo();
		t = t === void 0 ? null : t;
		var r = n.memoizedState;
		return r !== null && t !== null && zo(t, r[1]) ? r[0] : (e = e(), n.memoizedState = [e, t], e);
	}
	function ms(e, t, n) {
		return Po & 21 ? (Br(n, t) || (n = qt(), I.lanes |= n, Qc |= n, e.baseState = !0), t) : (e.baseState && (e.baseState = !1, Us = !0), e.memoizedState = n);
	}
	function hs(e, t) {
		var n = k;
		k = n !== 0 && 4 > n ? n : 4, e(!0);
		var r = No.transition;
		No.transition = {};
		try {
			e(!1), t();
		} finally {
			k = n, No.transition = r;
		}
	}
	function gs() {
		return Uo().memoizedState;
	}
	function _s(e, t, n) {
		var r = _l(e);
		if (n = {
			lane: r,
			action: n,
			hasEagerState: !1,
			eagerState: null,
			next: null
		}, ys(e)) bs(t, n);
		else if (n = co(e, t, n, r), n !== null) {
			var i = gl();
			vl(n, e, r, i), xs(n, t, r);
		}
	}
	function vs(e, t, n) {
		var r = _l(e), i = {
			lane: r,
			action: n,
			hasEagerState: !1,
			eagerState: null,
			next: null
		};
		if (ys(e)) bs(t, i);
		else {
			var a = e.alternate;
			if (e.lanes === 0 && (a === null || a.lanes === 0) && (a = t.lastRenderedReducer, a !== null)) try {
				var o = t.lastRenderedState, s = a(o, n);
				if (i.hasEagerState = !0, i.eagerState = s, Br(s, o)) {
					var c = t.interleaved;
					c === null ? (i.next = i, so(t)) : (i.next = c.next, c.next = i), t.interleaved = i;
					return;
				}
			} catch {}
			n = co(e, t, i, r), n !== null && (i = gl(), vl(n, e, r, i), xs(n, t, r));
		}
	}
	function ys(e) {
		var t = e.alternate;
		return e === I || t !== null && t === I;
	}
	function bs(e, t) {
		Io = Fo = !0;
		var n = e.pending;
		n === null ? t.next = t : (t.next = n.next, n.next = t), e.pending = t;
	}
	function xs(e, t, n) {
		if (n & 4194240) {
			var r = t.lanes;
			r &= e.pendingLanes, n |= r, t.lanes = n, Zt(e, n);
		}
	}
	var Ss = {
		readContext: ao,
		useCallback: z,
		useContext: z,
		useEffect: z,
		useImperativeHandle: z,
		useInsertionEffect: z,
		useLayoutEffect: z,
		useMemo: z,
		useReducer: z,
		useRef: z,
		useState: z,
		useDebugValue: z,
		useDeferredValue: z,
		useTransition: z,
		useMutableSource: z,
		useSyncExternalStore: z,
		useId: z,
		unstable_isNewReconciler: !1
	}, Cs = {
		readContext: ao,
		useCallback: function(e, t) {
			return Ho().memoizedState = [e, t === void 0 ? null : t], e;
		},
		useContext: ao,
		useEffect: as,
		useImperativeHandle: function(e, t, n) {
			return n = n == null ? null : n.concat([e]), rs(4194308, 4, ls.bind(null, t, e), n);
		},
		useLayoutEffect: function(e, t) {
			return rs(4194308, 4, e, t);
		},
		useInsertionEffect: function(e, t) {
			return rs(4, 2, e, t);
		},
		useMemo: function(e, t) {
			var n = Ho();
			return t = t === void 0 ? null : t, e = e(), n.memoizedState = [e, t], e;
		},
		useReducer: function(e, t, n) {
			var r = Ho();
			return t = n === void 0 ? t : n(t), r.memoizedState = r.baseState = t, e = {
				pending: null,
				interleaved: null,
				lanes: 0,
				dispatch: null,
				lastRenderedReducer: e,
				lastRenderedState: t
			}, r.queue = e, e = e.dispatch = _s.bind(null, I, e), [r.memoizedState, e];
		},
		useRef: function(e) {
			var t = Ho();
			return e = { current: e }, t.memoizedState = e;
		},
		useState: es,
		useDebugValue: ds,
		useDeferredValue: function(e) {
			return Ho().memoizedState = e;
		},
		useTransition: function() {
			var e = es(!1), t = e[0];
			return e = hs.bind(null, e[1]), Ho().memoizedState = e, [t, e];
		},
		useMutableSource: function() {},
		useSyncExternalStore: function(e, t, n) {
			var i = I, a = Ho();
			if (P) {
				if (n === void 0) throw Error(r(407));
				n = n();
			} else {
				if (n = t(), G === null) throw Error(r(349));
				Po & 30 || Yo(i, t, n);
			}
			a.memoizedState = n;
			var o = {
				value: n,
				getSnapshot: t
			};
			return a.queue = o, as(Zo.bind(null, i, o, e), [e]), i.flags |= 2048, ts(9, Xo.bind(null, i, o, n, t), void 0, null), n;
		},
		useId: function() {
			var e = Ho(), t = G.identifierPrefix;
			if (P) {
				var n = Da, r = Ea;
				n = (r & ~(1 << 32 - O(r) - 1)).toString(32) + n, t = ":" + t + "R" + n, n = Lo++, 0 < n && (t += "H" + n.toString(32)), t += ":";
			} else n = Ro++, t = ":" + t + "r" + n.toString(32) + ":";
			return e.memoizedState = t;
		},
		unstable_isNewReconciler: !1
	}, ws = {
		readContext: ao,
		useCallback: fs,
		useContext: ao,
		useEffect: os,
		useImperativeHandle: us,
		useInsertionEffect: ss,
		useLayoutEffect: cs,
		useMemo: ps,
		useReducer: Go,
		useRef: ns,
		useState: function() {
			return Go(Wo);
		},
		useDebugValue: ds,
		useDeferredValue: function(e) {
			return ms(Uo(), L.memoizedState, e);
		},
		useTransition: function() {
			return [Go(Wo)[0], Uo().memoizedState];
		},
		useMutableSource: qo,
		useSyncExternalStore: Jo,
		useId: gs,
		unstable_isNewReconciler: !1
	}, Ts = {
		readContext: ao,
		useCallback: fs,
		useContext: ao,
		useEffect: os,
		useImperativeHandle: us,
		useInsertionEffect: ss,
		useLayoutEffect: cs,
		useMemo: ps,
		useReducer: Ko,
		useRef: ns,
		useState: function() {
			return Ko(Wo);
		},
		useDebugValue: ds,
		useDeferredValue: function(e) {
			var t = Uo();
			return L === null ? t.memoizedState = e : ms(t, L.memoizedState, e);
		},
		useTransition: function() {
			return [Ko(Wo)[0], Uo().memoizedState];
		},
		useMutableSource: qo,
		useSyncExternalStore: Jo,
		useId: gs,
		unstable_isNewReconciler: !1
	};
	function Es(e, t) {
		if (e && e.defaultProps) {
			for (var n in t = T({}, t), e = e.defaultProps, e) t[n] === void 0 && (t[n] = e[n]);
			return t;
		}
		return t;
	}
	function Ds(e, t, n, r) {
		t = e.memoizedState, n = n(r, t), n = n == null ? t : T({}, t, n), e.memoizedState = n, e.lanes === 0 && (e.updateQueue.baseState = n);
	}
	var Os = {
		isMounted: function(e) {
			return (e = e._reactInternals) ? vt(e) === e : !1;
		},
		enqueueSetState: function(e, t, n) {
			e = e._reactInternals;
			var r = gl(), i = _l(e), a = mo(r, i);
			a.payload = t, n != null && (a.callback = n), t = ho(e, a, i), t !== null && (vl(t, e, i, r), go(t, e, i));
		},
		enqueueReplaceState: function(e, t, n) {
			e = e._reactInternals;
			var r = gl(), i = _l(e), a = mo(r, i);
			a.tag = 1, a.payload = t, n != null && (a.callback = n), t = ho(e, a, i), t !== null && (vl(t, e, i, r), go(t, e, i));
		},
		enqueueForceUpdate: function(e, t) {
			e = e._reactInternals;
			var n = gl(), r = _l(e), i = mo(n, r);
			i.tag = 2, t != null && (i.callback = t), t = ho(e, i, r), t !== null && (vl(t, e, r, n), go(t, e, r));
		}
	};
	function ks(e, t, n, r, i, a, o) {
		return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, a, o) : t.prototype && t.prototype.isPureReactComponent ? !Vr(n, r) || !Vr(i, a) : !0;
	}
	function As(e, t, n) {
		var r = !1, i = ra, a = t.contextType;
		return typeof a == "object" && a ? a = ao(a) : (i = sa(t) ? aa : N.current, r = t.contextTypes, a = (r = r != null) ? oa(e, i) : ra), t = new t(n, a), e.memoizedState = t.state !== null && t.state !== void 0 ? t.state : null, t.updater = Os, e.stateNode = t, t._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = i, e.__reactInternalMemoizedMaskedChildContext = a), t;
	}
	function js(e, t, n, r) {
		e = t.state, typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(n, r), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(n, r), t.state !== e && Os.enqueueReplaceState(t, t.state, null);
	}
	function Ms(e, t, n, r) {
		var i = e.stateNode;
		i.props = n, i.state = e.memoizedState, i.refs = {}, fo(e);
		var a = t.contextType;
		typeof a == "object" && a ? i.context = ao(a) : (a = sa(t) ? aa : N.current, i.context = oa(e, a)), i.state = e.memoizedState, a = t.getDerivedStateFromProps, typeof a == "function" && (Ds(e, t, a, n), i.state = e.memoizedState), typeof t.getDerivedStateFromProps == "function" || typeof i.getSnapshotBeforeUpdate == "function" || typeof i.UNSAFE_componentWillMount != "function" && typeof i.componentWillMount != "function" || (t = i.state, typeof i.componentWillMount == "function" && i.componentWillMount(), typeof i.UNSAFE_componentWillMount == "function" && i.UNSAFE_componentWillMount(), t !== i.state && Os.enqueueReplaceState(i, i.state, null), vo(e, n, i, r), i.state = e.memoizedState), typeof i.componentDidMount == "function" && (e.flags |= 4194308);
	}
	function Ns(e, t) {
		try {
			var n = "", r = t;
			do
				n += ge(r), r = r.return;
			while (r);
			var i = n;
		} catch (e) {
			i = "\nError generating stack: " + e.message + "\n" + e.stack;
		}
		return {
			value: e,
			source: t,
			stack: i,
			digest: null
		};
	}
	function Ps(e, t, n) {
		return {
			value: e,
			source: null,
			stack: n ?? null,
			digest: t ?? null
		};
	}
	function Fs(e, t) {
		try {
			console.error(t.value);
		} catch (e) {
			setTimeout(function() {
				throw e;
			});
		}
	}
	var Is = typeof WeakMap == "function" ? WeakMap : Map;
	function Ls(e, t, n) {
		n = mo(-1, n), n.tag = 3, n.payload = { element: null };
		var r = t.value;
		return n.callback = function() {
			ol || (ol = !0, sl = r), Fs(e, t);
		}, n;
	}
	function Rs(e, t, n) {
		n = mo(-1, n), n.tag = 3;
		var r = e.type.getDerivedStateFromError;
		if (typeof r == "function") {
			var i = t.value;
			n.payload = function() {
				return r(i);
			}, n.callback = function() {
				Fs(e, t);
			};
		}
		var a = e.stateNode;
		return a !== null && typeof a.componentDidCatch == "function" && (n.callback = function() {
			Fs(e, t), typeof r != "function" && (cl === null ? cl = /* @__PURE__ */ new Set([this]) : cl.add(this));
			var n = t.stack;
			this.componentDidCatch(t.value, { componentStack: n === null ? "" : n });
		}), n;
	}
	function zs(e, t, n) {
		var r = e.pingCache;
		if (r === null) {
			r = e.pingCache = new Is();
			var i = /* @__PURE__ */ new Set();
			r.set(t, i);
		} else i = r.get(t), i === void 0 && (i = /* @__PURE__ */ new Set(), r.set(t, i));
		i.has(n) || (i.add(n), e = Hl.bind(null, e, t, n), t.then(e, e));
	}
	function Bs(e) {
		do {
			var t;
			if ((t = e.tag === 13) && (t = e.memoizedState, t = t === null || t.dehydrated !== null), t) return e;
			e = e.return;
		} while (e !== null);
		return null;
	}
	function Vs(e, t, n, r, i) {
		return e.mode & 1 ? (e.flags |= 65536, e.lanes = i, e) : (e === t ? e.flags |= 65536 : (e.flags |= 128, n.flags |= 131072, n.flags &= -52805, n.tag === 1 && (n.alternate === null ? n.tag = 17 : (t = mo(-1, 1), t.tag = 2, ho(n, t, 1))), n.lanes |= 1), e);
	}
	var Hs = x.ReactCurrentOwner, Us = !1;
	function Ws(e, t, n, r) {
		t.child = e === null ? Xa(t, null, n, r) : Ya(t, e.child, n, r);
	}
	function Gs(e, t, n, r, i) {
		n = n.render;
		var a = t.ref;
		return io(t, i), r = Bo(e, t, n, r, a, i), n = Vo(), e !== null && !Us ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~i, dc(e, t, i)) : (P && n && Aa(t), t.flags |= 1, Ws(e, t, r, i), t.child);
	}
	function Ks(e, t, n, r, i) {
		if (e === null) {
			var a = n.type;
			return typeof a == "function" && !Xl(a) && a.defaultProps === void 0 && n.compare === null && n.defaultProps === void 0 ? (t.tag = 15, t.type = a, qs(e, t, a, r, i)) : (e = $l(n.type, null, r, t, t.mode, i), e.ref = t.ref, e.return = t, t.child = e);
		}
		if (a = e.child, (e.lanes & i) === 0) {
			var o = a.memoizedProps;
			if (n = n.compare, n = n === null ? Vr : n, n(o, r) && e.ref === t.ref) return dc(e, t, i);
		}
		return t.flags |= 1, e = Ql(a, r), e.ref = t.ref, e.return = t, t.child = e;
	}
	function qs(e, t, n, r, i) {
		if (e !== null) {
			var a = e.memoizedProps;
			if (Vr(a, r) && e.ref === t.ref) if (Us = !1, t.pendingProps = r = a, (e.lanes & i) !== 0) e.flags & 131072 && (Us = !0);
			else return t.lanes = e.lanes, dc(e, t, i);
		}
		return Xs(e, t, n, r, i);
	}
	function Js(e, t, n) {
		var r = t.pendingProps, i = r.children, a = e === null ? null : e.memoizedState;
		if (r.mode === "hidden") if (!(t.mode & 1)) t.memoizedState = {
			baseLanes: 0,
			cachePool: null,
			transitions: null
		}, M(Xc, Yc), Yc |= n;
		else {
			if (!(n & 1073741824)) return e = a === null ? n : a.baseLanes | n, t.lanes = t.childLanes = 1073741824, t.memoizedState = {
				baseLanes: e,
				cachePool: null,
				transitions: null
			}, t.updateQueue = null, M(Xc, Yc), Yc |= e, null;
			t.memoizedState = {
				baseLanes: 0,
				cachePool: null,
				transitions: null
			}, r = a === null ? n : a.baseLanes, M(Xc, Yc), Yc |= r;
		}
		else a === null ? r = n : (r = a.baseLanes | n, t.memoizedState = null), M(Xc, Yc), Yc |= r;
		return Ws(e, t, i, n), t.child;
	}
	function Ys(e, t) {
		var n = t.ref;
		(e === null && n !== null || e !== null && e.ref !== n) && (t.flags |= 512, t.flags |= 2097152);
	}
	function Xs(e, t, n, r, i) {
		var a = sa(n) ? aa : N.current;
		return a = oa(t, a), io(t, i), n = Bo(e, t, n, r, a, i), r = Vo(), e !== null && !Us ? (t.updateQueue = e.updateQueue, t.flags &= -2053, e.lanes &= ~i, dc(e, t, i)) : (P && r && Aa(t), t.flags |= 1, Ws(e, t, n, i), t.child);
	}
	function Zs(e, t, n, r, i) {
		if (sa(n)) {
			var a = !0;
			da(t);
		} else a = !1;
		if (io(t, i), t.stateNode === null) uc(e, t), As(t, n, r), Ms(t, n, r, i), r = !0;
		else if (e === null) {
			var o = t.stateNode, s = t.memoizedProps;
			o.props = s;
			var c = o.context, l = n.contextType;
			typeof l == "object" && l ? l = ao(l) : (l = sa(n) ? aa : N.current, l = oa(t, l));
			var u = n.getDerivedStateFromProps, d = typeof u == "function" || typeof o.getSnapshotBeforeUpdate == "function";
			d || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (s !== r || c !== l) && js(t, o, r, l), uo = !1;
			var f = t.memoizedState;
			o.state = f, vo(t, r, o, i), c = t.memoizedState, s !== r || f !== c || ia.current || uo ? (typeof u == "function" && (Ds(t, n, u, r), c = t.memoizedState), (s = uo || ks(t, n, s, r, f, c, l)) ? (d || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount()), typeof o.componentDidMount == "function" && (t.flags |= 4194308)) : (typeof o.componentDidMount == "function" && (t.flags |= 4194308), t.memoizedProps = r, t.memoizedState = c), o.props = r, o.state = c, o.context = l, r = s) : (typeof o.componentDidMount == "function" && (t.flags |= 4194308), r = !1);
		} else {
			o = t.stateNode, po(e, t), s = t.memoizedProps, l = t.type === t.elementType ? s : Es(t.type, s), o.props = l, d = t.pendingProps, f = o.context, c = n.contextType, typeof c == "object" && c ? c = ao(c) : (c = sa(n) ? aa : N.current, c = oa(t, c));
			var p = n.getDerivedStateFromProps;
			(u = typeof p == "function" || typeof o.getSnapshotBeforeUpdate == "function") || typeof o.UNSAFE_componentWillReceiveProps != "function" && typeof o.componentWillReceiveProps != "function" || (s !== d || f !== c) && js(t, o, r, c), uo = !1, f = t.memoizedState, o.state = f, vo(t, r, o, i);
			var m = t.memoizedState;
			s !== d || f !== m || ia.current || uo ? (typeof p == "function" && (Ds(t, n, p, r), m = t.memoizedState), (l = uo || ks(t, n, l, r, f, m, c) || !1) ? (u || typeof o.UNSAFE_componentWillUpdate != "function" && typeof o.componentWillUpdate != "function" || (typeof o.componentWillUpdate == "function" && o.componentWillUpdate(r, m, c), typeof o.UNSAFE_componentWillUpdate == "function" && o.UNSAFE_componentWillUpdate(r, m, c)), typeof o.componentDidUpdate == "function" && (t.flags |= 4), typeof o.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof o.componentDidUpdate != "function" || s === e.memoizedProps && f === e.memoizedState || (t.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && f === e.memoizedState || (t.flags |= 1024), t.memoizedProps = r, t.memoizedState = m), o.props = r, o.state = m, o.context = c, r = l) : (typeof o.componentDidUpdate != "function" || s === e.memoizedProps && f === e.memoizedState || (t.flags |= 4), typeof o.getSnapshotBeforeUpdate != "function" || s === e.memoizedProps && f === e.memoizedState || (t.flags |= 1024), r = !1);
		}
		return Qs(e, t, n, r, a, i);
	}
	function Qs(e, t, n, r, i, a) {
		Ys(e, t);
		var o = (t.flags & 128) != 0;
		if (!r && !o) return i && fa(t, n, !1), dc(e, t, a);
		r = t.stateNode, Hs.current = t;
		var s = o && typeof n.getDerivedStateFromError != "function" ? null : r.render();
		return t.flags |= 1, e !== null && o ? (t.child = Ya(t, e.child, null, a), t.child = Ya(t, null, s, a)) : Ws(e, t, s, a), t.memoizedState = r.state, i && fa(t, n, !0), t.child;
	}
	function $s(e) {
		var t = e.stateNode;
		t.pendingContext ? la(e, t.pendingContext, t.pendingContext !== t.context) : t.context && la(e, t.context, !1), To(e, t.containerInfo);
	}
	function ec(e, t, n, r, i) {
		return Ha(), Ua(i), t.flags |= 256, Ws(e, t, n, r), t.child;
	}
	var tc = {
		dehydrated: null,
		treeContext: null,
		retryLane: 0
	};
	function nc(e) {
		return {
			baseLanes: e,
			cachePool: null,
			transitions: null
		};
	}
	function rc(e, t, n) {
		var r = t.pendingProps, i = F.current, a = !1, o = (t.flags & 128) != 0, s;
		if ((s = o) || (s = e !== null && e.memoizedState === null ? !1 : (i & 2) != 0), s ? (a = !0, t.flags &= -129) : (e === null || e.memoizedState !== null) && (i |= 1), M(F, i & 1), e === null) return Ra(t), e = t.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (t.mode & 1 ? e.data === "$!" ? t.lanes = 8 : t.lanes = 1073741824 : t.lanes = 1, null) : (o = r.children, e = r.fallback, a ? (r = t.mode, a = t.child, o = {
			mode: "hidden",
			children: o
		}, !(r & 1) && a !== null ? (a.childLanes = 0, a.pendingProps = o) : a = tu(o, r, 0, null), e = eu(e, r, n, null), a.return = t, e.return = t, a.sibling = e, t.child = a, t.child.memoizedState = nc(n), t.memoizedState = tc, e) : ic(t, o));
		if (i = e.memoizedState, i !== null && (s = i.dehydrated, s !== null)) return oc(e, t, o, r, s, i, n);
		if (a) {
			a = r.fallback, o = t.mode, i = e.child, s = i.sibling;
			var c = {
				mode: "hidden",
				children: r.children
			};
			return !(o & 1) && t.child !== i ? (r = t.child, r.childLanes = 0, r.pendingProps = c, t.deletions = null) : (r = Ql(i, c), r.subtreeFlags = i.subtreeFlags & 14680064), s === null ? (a = eu(a, o, n, null), a.flags |= 2) : a = Ql(s, a), a.return = t, r.return = t, r.sibling = a, t.child = r, r = a, a = t.child, o = e.child.memoizedState, o = o === null ? nc(n) : {
				baseLanes: o.baseLanes | n,
				cachePool: null,
				transitions: o.transitions
			}, a.memoizedState = o, a.childLanes = e.childLanes & ~n, t.memoizedState = tc, r;
		}
		return a = e.child, e = a.sibling, r = Ql(a, {
			mode: "visible",
			children: r.children
		}), !(t.mode & 1) && (r.lanes = n), r.return = t, r.sibling = null, e !== null && (n = t.deletions, n === null ? (t.deletions = [e], t.flags |= 16) : n.push(e)), t.child = r, t.memoizedState = null, r;
	}
	function ic(e, t) {
		return t = tu({
			mode: "visible",
			children: t
		}, e.mode, 0, null), t.return = e, e.child = t;
	}
	function ac(e, t, n, r) {
		return r !== null && Ua(r), Ya(t, e.child, null, n), e = ic(t, t.pendingProps.children), e.flags |= 2, t.memoizedState = null, e;
	}
	function oc(e, t, n, i, a, o, s) {
		if (n) return t.flags & 256 ? (t.flags &= -257, i = Ps(Error(r(422))), ac(e, t, s, i)) : t.memoizedState === null ? (o = i.fallback, a = t.mode, i = tu({
			mode: "visible",
			children: i.children
		}, a, 0, null), o = eu(o, a, s, null), o.flags |= 2, i.return = t, o.return = t, i.sibling = o, t.child = i, t.mode & 1 && Ya(t, e.child, null, s), t.child.memoizedState = nc(s), t.memoizedState = tc, o) : (t.child = e.child, t.flags |= 128, null);
		if (!(t.mode & 1)) return ac(e, t, s, null);
		if (a.data === "$!") {
			if (i = a.nextSibling && a.nextSibling.dataset, i) var c = i.dgst;
			return i = c, o = Error(r(419)), i = Ps(o, i, void 0), ac(e, t, s, i);
		}
		if (c = (s & e.childLanes) !== 0, Us || c) {
			if (i = G, i !== null) {
				switch (s & -s) {
					case 4:
						a = 2;
						break;
					case 16:
						a = 8;
						break;
					case 64:
					case 128:
					case 256:
					case 512:
					case 1024:
					case 2048:
					case 4096:
					case 8192:
					case 16384:
					case 32768:
					case 65536:
					case 131072:
					case 262144:
					case 524288:
					case 1048576:
					case 2097152:
					case 4194304:
					case 8388608:
					case 16777216:
					case 33554432:
					case 67108864:
						a = 32;
						break;
					case 536870912:
						a = 268435456;
						break;
					default: a = 0;
				}
				a = (a & (i.suspendedLanes | s)) === 0 ? a : 0, a !== 0 && a !== o.retryLane && (o.retryLane = a, lo(e, a), vl(i, e, a, -1));
			}
			return Ml(), i = Ps(Error(r(421))), ac(e, t, s, i);
		}
		return a.data === "$?" ? (t.flags |= 128, t.child = e.child, t = Wl.bind(null, e), a._reactRetry = t, null) : (e = o.treeContext, Na = Vi(a.nextSibling), Ma = t, P = !0, Pa = null, e !== null && (Ca[wa++] = Ea, Ca[wa++] = Da, Ca[wa++] = Ta, Ea = e.id, Da = e.overflow, Ta = t), t = ic(t, i.children), t.flags |= 4096, t);
	}
	function sc(e, t, n) {
		e.lanes |= t;
		var r = e.alternate;
		r !== null && (r.lanes |= t), ro(e.return, t, n);
	}
	function cc(e, t, n, r, i) {
		var a = e.memoizedState;
		a === null ? e.memoizedState = {
			isBackwards: t,
			rendering: null,
			renderingStartTime: 0,
			last: r,
			tail: n,
			tailMode: i
		} : (a.isBackwards = t, a.rendering = null, a.renderingStartTime = 0, a.last = r, a.tail = n, a.tailMode = i);
	}
	function lc(e, t, n) {
		var r = t.pendingProps, i = r.revealOrder, a = r.tail;
		if (Ws(e, t, r.children, n), r = F.current, r & 2) r = r & 1 | 2, t.flags |= 128;
		else {
			if (e !== null && e.flags & 128) a: for (e = t.child; e !== null;) {
				if (e.tag === 13) e.memoizedState !== null && sc(e, n, t);
				else if (e.tag === 19) sc(e, n, t);
				else if (e.child !== null) {
					e.child.return = e, e = e.child;
					continue;
				}
				if (e === t) break a;
				for (; e.sibling === null;) {
					if (e.return === null || e.return === t) break a;
					e = e.return;
				}
				e.sibling.return = e.return, e = e.sibling;
			}
			r &= 1;
		}
		if (M(F, r), !(t.mode & 1)) t.memoizedState = null;
		else switch (i) {
			case "forwards":
				for (n = t.child, i = null; n !== null;) e = n.alternate, e !== null && ko(e) === null && (i = n), n = n.sibling;
				n = i, n === null ? (i = t.child, t.child = null) : (i = n.sibling, n.sibling = null), cc(t, !1, i, n, a);
				break;
			case "backwards":
				for (n = null, i = t.child, t.child = null; i !== null;) {
					if (e = i.alternate, e !== null && ko(e) === null) {
						t.child = i;
						break;
					}
					e = i.sibling, i.sibling = n, n = i, i = e;
				}
				cc(t, !0, n, null, a);
				break;
			case "together":
				cc(t, !1, null, null, void 0);
				break;
			default: t.memoizedState = null;
		}
		return t.child;
	}
	function uc(e, t) {
		!(t.mode & 1) && e !== null && (e.alternate = null, t.alternate = null, t.flags |= 2);
	}
	function dc(e, t, n) {
		if (e !== null && (t.dependencies = e.dependencies), Qc |= t.lanes, (n & t.childLanes) === 0) return null;
		if (e !== null && t.child !== e.child) throw Error(r(153));
		if (t.child !== null) {
			for (e = t.child, n = Ql(e, e.pendingProps), t.child = n, n.return = t; e.sibling !== null;) e = e.sibling, n = n.sibling = Ql(e, e.pendingProps), n.return = t;
			n.sibling = null;
		}
		return t.child;
	}
	function fc(e, t, n) {
		switch (t.tag) {
			case 3:
				$s(t), Ha();
				break;
			case 5:
				Do(t);
				break;
			case 1:
				sa(t.type) && da(t);
				break;
			case 4:
				To(t, t.stateNode.containerInfo);
				break;
			case 10:
				var r = t.type._context, i = t.memoizedProps.value;
				M(Za, r._currentValue), r._currentValue = i;
				break;
			case 13:
				if (r = t.memoizedState, r !== null) return r.dehydrated === null ? (n & t.child.childLanes) === 0 ? (M(F, F.current & 1), e = dc(e, t, n), e === null ? null : e.sibling) : rc(e, t, n) : (M(F, F.current & 1), t.flags |= 128, null);
				M(F, F.current & 1);
				break;
			case 19:
				if (r = (n & t.childLanes) !== 0, e.flags & 128) {
					if (r) return lc(e, t, n);
					t.flags |= 128;
				}
				if (i = t.memoizedState, i !== null && (i.rendering = null, i.tail = null, i.lastEffect = null), M(F, F.current), r) break;
				return null;
			case 22:
			case 23: return t.lanes = 0, Js(e, t, n);
		}
		return dc(e, t, n);
	}
	var pc = function(e, t) {
		for (var n = t.child; n !== null;) {
			if (n.tag === 5 || n.tag === 6) e.appendChild(n.stateNode);
			else if (n.tag !== 4 && n.child !== null) {
				n.child.return = n, n = n.child;
				continue;
			}
			if (n === t) break;
			for (; n.sibling === null;) {
				if (n.return === null || n.return === t) return;
				n = n.return;
			}
			n.sibling.return = n.return, n = n.sibling;
		}
	}, mc = function(e, t, n, r) {
		var i = e.memoizedProps;
		if (i !== r) {
			e = t.stateNode, wo(xo.current);
			var o = null;
			switch (n) {
				case "input":
					i = Te(e, i), r = Te(e, r), o = [];
					break;
				case "select":
					i = T({}, i, { value: void 0 }), r = T({}, r, { value: void 0 }), o = [];
					break;
				case "textarea":
					i = Ne(e, i), r = Ne(e, r), o = [];
					break;
				default: typeof i.onClick != "function" && typeof r.onClick == "function" && (e.onclick = ji);
			}
			qe(n, r);
			var s;
			for (u in n = null, i) if (!r.hasOwnProperty(u) && i.hasOwnProperty(u) && i[u] != null) if (u === "style") {
				var c = i[u];
				for (s in c) c.hasOwnProperty(s) && (n ||= {}, n[s] = "");
			} else u !== "dangerouslySetInnerHTML" && u !== "children" && u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && u !== "autoFocus" && (a.hasOwnProperty(u) ? o ||= [] : (o ||= []).push(u, null));
			for (u in r) {
				var l = r[u];
				if (c = i?.[u], r.hasOwnProperty(u) && l !== c && (l != null || c != null)) if (u === "style") if (c) {
					for (s in c) !c.hasOwnProperty(s) || l && l.hasOwnProperty(s) || (n ||= {}, n[s] = "");
					for (s in l) l.hasOwnProperty(s) && c[s] !== l[s] && (n ||= {}, n[s] = l[s]);
				} else n || (o ||= [], o.push(u, n)), n = l;
				else u === "dangerouslySetInnerHTML" ? (l = l ? l.__html : void 0, c = c ? c.__html : void 0, l != null && c !== l && (o ||= []).push(u, l)) : u === "children" ? typeof l != "string" && typeof l != "number" || (o ||= []).push(u, "" + l) : u !== "suppressContentEditableWarning" && u !== "suppressHydrationWarning" && (a.hasOwnProperty(u) ? (l != null && u === "onScroll" && A("scroll", e), o || c === l || (o = [])) : (o ||= []).push(u, l));
			}
			n && (o ||= []).push("style", n);
			var u = o;
			(t.updateQueue = u) && (t.flags |= 4);
		}
	}, hc = function(e, t, n, r) {
		n !== r && (t.flags |= 4);
	};
	function gc(e, t) {
		if (!P) switch (e.tailMode) {
			case "hidden":
				t = e.tail;
				for (var n = null; t !== null;) t.alternate !== null && (n = t), t = t.sibling;
				n === null ? e.tail = null : n.sibling = null;
				break;
			case "collapsed":
				n = e.tail;
				for (var r = null; n !== null;) n.alternate !== null && (r = n), n = n.sibling;
				r === null ? t || e.tail === null ? e.tail = null : e.tail.sibling = null : r.sibling = null;
		}
	}
	function B(e) {
		var t = e.alternate !== null && e.alternate.child === e.child, n = 0, r = 0;
		if (t) for (var i = e.child; i !== null;) n |= i.lanes | i.childLanes, r |= i.subtreeFlags & 14680064, r |= i.flags & 14680064, i.return = e, i = i.sibling;
		else for (i = e.child; i !== null;) n |= i.lanes | i.childLanes, r |= i.subtreeFlags, r |= i.flags, i.return = e, i = i.sibling;
		return e.subtreeFlags |= r, e.childLanes = n, t;
	}
	function _c(e, t, n) {
		var i = t.pendingProps;
		switch (ja(t), t.tag) {
			case 2:
			case 16:
			case 15:
			case 0:
			case 11:
			case 7:
			case 8:
			case 12:
			case 9:
			case 14: return B(t), null;
			case 1: return sa(t.type) && ca(), B(t), null;
			case 3: return i = t.stateNode, Eo(), j(ia), j(N), jo(), i.pendingContext && (i.context = i.pendingContext, i.pendingContext = null), (e === null || e.child === null) && (Ba(t) ? t.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(t.flags & 256) || (t.flags |= 1024, Pa !== null && (Sl(Pa), Pa = null))), B(t), null;
			case 5:
				Oo(t);
				var o = wo(Co.current);
				if (n = t.type, e !== null && t.stateNode != null) mc(e, t, n, i, o), e.ref !== t.ref && (t.flags |= 512, t.flags |= 2097152);
				else {
					if (!i) {
						if (t.stateNode === null) throw Error(r(166));
						return B(t), null;
					}
					if (e = wo(xo.current), Ba(t)) {
						i = t.stateNode, n = t.type;
						var s = t.memoizedProps;
						switch (i[Wi] = t, i[Gi] = s, e = (t.mode & 1) != 0, n) {
							case "dialog":
								A("cancel", i), A("close", i);
								break;
							case "iframe":
							case "object":
							case "embed":
								A("load", i);
								break;
							case "video":
							case "audio":
								for (o = 0; o < mi.length; o++) A(mi[o], i);
								break;
							case "source":
								A("error", i);
								break;
							case "img":
							case "image":
							case "link":
								A("error", i), A("load", i);
								break;
							case "details":
								A("toggle", i);
								break;
							case "input":
								Ee(i, s), A("invalid", i);
								break;
							case "select":
								i._wrapperState = { wasMultiple: !!s.multiple }, A("invalid", i);
								break;
							case "textarea": Pe(i, s), A("invalid", i);
						}
						for (var c in qe(n, s), o = null, s) if (s.hasOwnProperty(c)) {
							var l = s[c];
							c === "children" ? typeof l == "string" ? i.textContent !== l && (!0 !== s.suppressHydrationWarning && Ai(i.textContent, l, e), o = ["children", l]) : typeof l == "number" && i.textContent !== "" + l && (!0 !== s.suppressHydrationWarning && Ai(i.textContent, l, e), o = ["children", "" + l]) : a.hasOwnProperty(c) && l != null && c === "onScroll" && A("scroll", i);
						}
						switch (n) {
							case "input":
								Se(i), ke(i, s, !0);
								break;
							case "textarea":
								Se(i), Ie(i);
								break;
							case "select":
							case "option": break;
							default: typeof s.onClick == "function" && (i.onclick = ji);
						}
						i = o, t.updateQueue = i, i !== null && (t.flags |= 4);
					} else {
						c = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = Le(n)), e === "http://www.w3.org/1999/xhtml" ? n === "script" ? (e = c.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof i.is == "string" ? e = c.createElement(n, { is: i.is }) : (e = c.createElement(n), n === "select" && (c = e, i.multiple ? c.multiple = !0 : i.size && (c.size = i.size))) : e = c.createElementNS(e, n), e[Wi] = t, e[Gi] = i, pc(e, t, !1, !1), t.stateNode = e;
						a: {
							switch (c = Je(n, i), n) {
								case "dialog":
									A("cancel", e), A("close", e), o = i;
									break;
								case "iframe":
								case "object":
								case "embed":
									A("load", e), o = i;
									break;
								case "video":
								case "audio":
									for (o = 0; o < mi.length; o++) A(mi[o], e);
									o = i;
									break;
								case "source":
									A("error", e), o = i;
									break;
								case "img":
								case "image":
								case "link":
									A("error", e), A("load", e), o = i;
									break;
								case "details":
									A("toggle", e), o = i;
									break;
								case "input":
									Ee(e, i), o = Te(e, i), A("invalid", e);
									break;
								case "option":
									o = i;
									break;
								case "select":
									e._wrapperState = { wasMultiple: !!i.multiple }, o = T({}, i, { value: void 0 }), A("invalid", e);
									break;
								case "textarea":
									Pe(e, i), o = Ne(e, i), A("invalid", e);
									break;
								default: o = i;
							}
							for (s in qe(n, o), l = o, l) if (l.hasOwnProperty(s)) {
								var u = l[s];
								s === "style" ? Ge(e, u) : s === "dangerouslySetInnerHTML" ? (u = u ? u.__html : void 0, u != null && Be(e, u)) : s === "children" ? typeof u == "string" ? (n !== "textarea" || u !== "") && Ve(e, u) : typeof u == "number" && Ve(e, "" + u) : s !== "suppressContentEditableWarning" && s !== "suppressHydrationWarning" && s !== "autoFocus" && (a.hasOwnProperty(s) ? u != null && s === "onScroll" && A("scroll", e) : u != null && b(e, s, u, c));
							}
							switch (n) {
								case "input":
									Se(e), ke(e, i, !1);
									break;
								case "textarea":
									Se(e), Ie(e);
									break;
								case "option":
									i.value != null && e.setAttribute("value", "" + ye(i.value));
									break;
								case "select":
									e.multiple = !!i.multiple, s = i.value, s == null ? i.defaultValue != null && Me(e, !!i.multiple, i.defaultValue, !0) : Me(e, !!i.multiple, s, !1);
									break;
								default: typeof o.onClick == "function" && (e.onclick = ji);
							}
							switch (n) {
								case "button":
								case "input":
								case "select":
								case "textarea":
									i = !!i.autoFocus;
									break a;
								case "img":
									i = !0;
									break a;
								default: i = !1;
							}
						}
						i && (t.flags |= 4);
					}
					t.ref !== null && (t.flags |= 512, t.flags |= 2097152);
				}
				return B(t), null;
			case 6:
				if (e && t.stateNode != null) hc(e, t, e.memoizedProps, i);
				else {
					if (typeof i != "string" && t.stateNode === null) throw Error(r(166));
					if (n = wo(Co.current), wo(xo.current), Ba(t)) {
						if (i = t.stateNode, n = t.memoizedProps, i[Wi] = t, (s = i.nodeValue !== n) && (e = Ma, e !== null)) switch (e.tag) {
							case 3:
								Ai(i.nodeValue, n, (e.mode & 1) != 0);
								break;
							case 5: !0 !== e.memoizedProps.suppressHydrationWarning && Ai(i.nodeValue, n, (e.mode & 1) != 0);
						}
						s && (t.flags |= 4);
					} else i = (n.nodeType === 9 ? n : n.ownerDocument).createTextNode(i), i[Wi] = t, t.stateNode = i;
				}
				return B(t), null;
			case 13:
				if (j(F), i = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
					if (P && Na !== null && t.mode & 1 && !(t.flags & 128)) Va(), Ha(), t.flags |= 98560, s = !1;
					else if (s = Ba(t), i !== null && i.dehydrated !== null) {
						if (e === null) {
							if (!s) throw Error(r(318));
							if (s = t.memoizedState, s = s === null ? null : s.dehydrated, !s) throw Error(r(317));
							s[Wi] = t;
						} else Ha(), !(t.flags & 128) && (t.memoizedState = null), t.flags |= 4;
						B(t), s = !1;
					} else Pa !== null && (Sl(Pa), Pa = null), s = !0;
					if (!s) return t.flags & 65536 ? t : null;
				}
				return t.flags & 128 ? (t.lanes = n, t) : (i = i !== null, i !== (e !== null && e.memoizedState !== null) && i && (t.child.flags |= 8192, t.mode & 1 && (e === null || F.current & 1 ? J === 0 && (J = 3) : Ml())), t.updateQueue !== null && (t.flags |= 4), B(t), null);
			case 4: return Eo(), e === null && bi(t.stateNode.containerInfo), B(t), null;
			case 10: return no(t.type._context), B(t), null;
			case 17: return sa(t.type) && ca(), B(t), null;
			case 19:
				if (j(F), s = t.memoizedState, s === null) return B(t), null;
				if (i = (t.flags & 128) != 0, c = s.rendering, c === null) if (i) gc(s, !1);
				else {
					if (J !== 0 || e !== null && e.flags & 128) for (e = t.child; e !== null;) {
						if (c = ko(e), c !== null) {
							for (t.flags |= 128, gc(s, !1), i = c.updateQueue, i !== null && (t.updateQueue = i, t.flags |= 4), t.subtreeFlags = 0, i = n, n = t.child; n !== null;) s = n, e = i, s.flags &= 14680066, c = s.alternate, c === null ? (s.childLanes = 0, s.lanes = e, s.child = null, s.subtreeFlags = 0, s.memoizedProps = null, s.memoizedState = null, s.updateQueue = null, s.dependencies = null, s.stateNode = null) : (s.childLanes = c.childLanes, s.lanes = c.lanes, s.child = c.child, s.subtreeFlags = 0, s.deletions = null, s.memoizedProps = c.memoizedProps, s.memoizedState = c.memoizedState, s.updateQueue = c.updateQueue, s.type = c.type, e = c.dependencies, s.dependencies = e === null ? null : {
								lanes: e.lanes,
								firstContext: e.firstContext
							}), n = n.sibling;
							return M(F, F.current & 1 | 2), t.child;
						}
						e = e.sibling;
					}
					s.tail !== null && E() > il && (t.flags |= 128, i = !0, gc(s, !1), t.lanes = 4194304);
				}
				else {
					if (!i) if (e = ko(c), e !== null) {
						if (t.flags |= 128, i = !0, n = e.updateQueue, n !== null && (t.updateQueue = n, t.flags |= 4), gc(s, !0), s.tail === null && s.tailMode === "hidden" && !c.alternate && !P) return B(t), null;
					} else 2 * E() - s.renderingStartTime > il && n !== 1073741824 && (t.flags |= 128, i = !0, gc(s, !1), t.lanes = 4194304);
					s.isBackwards ? (c.sibling = t.child, t.child = c) : (n = s.last, n === null ? t.child = c : n.sibling = c, s.last = c);
				}
				return s.tail === null ? (B(t), null) : (t = s.tail, s.rendering = t, s.tail = t.sibling, s.renderingStartTime = E(), t.sibling = null, n = F.current, M(F, i ? n & 1 | 2 : n & 1), t);
			case 22:
			case 23: return Ol(), i = t.memoizedState !== null, e !== null && e.memoizedState !== null !== i && (t.flags |= 8192), i && t.mode & 1 ? Yc & 1073741824 && (B(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : B(t), null;
			case 24: return null;
			case 25: return null;
		}
		throw Error(r(156, t.tag));
	}
	function vc(e, t) {
		switch (ja(t), t.tag) {
			case 1: return sa(t.type) && ca(), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
			case 3: return Eo(), j(ia), j(N), jo(), e = t.flags, e & 65536 && !(e & 128) ? (t.flags = e & -65537 | 128, t) : null;
			case 5: return Oo(t), null;
			case 13:
				if (j(F), e = t.memoizedState, e !== null && e.dehydrated !== null) {
					if (t.alternate === null) throw Error(r(340));
					Ha();
				}
				return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, t) : null;
			case 19: return j(F), null;
			case 4: return Eo(), null;
			case 10: return no(t.type._context), null;
			case 22:
			case 23: return Ol(), null;
			case 24: return null;
			default: return null;
		}
	}
	var yc = !1, V = !1, bc = typeof WeakSet == "function" ? WeakSet : Set, H = null;
	function xc(e, t) {
		var n = e.ref;
		if (n !== null) if (typeof n == "function") try {
			n(null);
		} catch (n) {
			Y(e, t, n);
		}
		else n.current = null;
	}
	function Sc(e, t, n) {
		try {
			n();
		} catch (n) {
			Y(e, t, n);
		}
	}
	var Cc = !1;
	function wc(e, t) {
		if (Mi = wn, e = Gr(), Kr(e)) {
			if ("selectionStart" in e) var n = {
				start: e.selectionStart,
				end: e.selectionEnd
			};
			else a: {
				n = (n = e.ownerDocument) && n.defaultView || window;
				var i = n.getSelection && n.getSelection();
				if (i && i.rangeCount !== 0) {
					n = i.anchorNode;
					var a = i.anchorOffset, o = i.focusNode;
					i = i.focusOffset;
					try {
						n.nodeType, o.nodeType;
					} catch {
						n = null;
						break a;
					}
					var s = 0, c = -1, l = -1, u = 0, d = 0, f = e, p = null;
					b: for (;;) {
						for (var m; f !== n || a !== 0 && f.nodeType !== 3 || (c = s + a), f !== o || i !== 0 && f.nodeType !== 3 || (l = s + i), f.nodeType === 3 && (s += f.nodeValue.length), (m = f.firstChild) !== null;) p = f, f = m;
						for (;;) {
							if (f === e) break b;
							if (p === n && ++u === a && (c = s), p === o && ++d === i && (l = s), (m = f.nextSibling) !== null) break;
							f = p, p = f.parentNode;
						}
						f = m;
					}
					n = c === -1 || l === -1 ? null : {
						start: c,
						end: l
					};
				} else n = null;
			}
			n ||= {
				start: 0,
				end: 0
			};
		} else n = null;
		for (Ni = {
			focusedElem: e,
			selectionRange: n
		}, wn = !1, H = t; H !== null;) if (t = H, e = t.child, t.subtreeFlags & 1028 && e !== null) e.return = t, H = e;
		else for (; H !== null;) {
			t = H;
			try {
				var h = t.alternate;
				if (t.flags & 1024) switch (t.tag) {
					case 0:
					case 11:
					case 15: break;
					case 1:
						if (h !== null) {
							var g = h.memoizedProps, _ = h.memoizedState, v = t.stateNode;
							v.__reactInternalSnapshotBeforeUpdate = v.getSnapshotBeforeUpdate(t.elementType === t.type ? g : Es(t.type, g), _);
						}
						break;
					case 3:
						var y = t.stateNode.containerInfo;
						y.nodeType === 1 ? y.textContent = "" : y.nodeType === 9 && y.documentElement && y.removeChild(y.documentElement);
						break;
					case 5:
					case 6:
					case 4:
					case 17: break;
					default: throw Error(r(163));
				}
			} catch (e) {
				Y(t, t.return, e);
			}
			if (e = t.sibling, e !== null) {
				e.return = t.return, H = e;
				break;
			}
			H = t.return;
		}
		return h = Cc, Cc = !1, h;
	}
	function Tc(e, t, n) {
		var r = t.updateQueue;
		if (r = r === null ? null : r.lastEffect, r !== null) {
			var i = r = r.next;
			do {
				if ((i.tag & e) === e) {
					var a = i.destroy;
					i.destroy = void 0, a !== void 0 && Sc(t, n, a);
				}
				i = i.next;
			} while (i !== r);
		}
	}
	function Ec(e, t) {
		if (t = t.updateQueue, t = t === null ? null : t.lastEffect, t !== null) {
			var n = t = t.next;
			do {
				if ((n.tag & e) === e) {
					var r = n.create;
					n.destroy = r();
				}
				n = n.next;
			} while (n !== t);
		}
	}
	function Dc(e) {
		var t = e.ref;
		if (t !== null) {
			var n = e.stateNode;
			switch (e.tag) {
				case 5:
					e = n;
					break;
				default: e = n;
			}
			typeof t == "function" ? t(e) : t.current = e;
		}
	}
	function Oc(e) {
		var t = e.alternate;
		t !== null && (e.alternate = null, Oc(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && (delete t[Wi], delete t[Gi], delete t[qi], delete t[Ji], delete t[Yi])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
	}
	function kc(e) {
		return e.tag === 5 || e.tag === 3 || e.tag === 4;
	}
	function Ac(e) {
		a: for (;;) {
			for (; e.sibling === null;) {
				if (e.return === null || kc(e.return)) return null;
				e = e.return;
			}
			for (e.sibling.return = e.return, e = e.sibling; e.tag !== 5 && e.tag !== 6 && e.tag !== 18;) {
				if (e.flags & 2 || e.child === null || e.tag === 4) continue a;
				e.child.return = e, e = e.child;
			}
			if (!(e.flags & 2)) return e.stateNode;
		}
	}
	function jc(e, t, n) {
		var r = e.tag;
		if (r === 5 || r === 6) e = e.stateNode, t ? n.nodeType === 8 ? n.parentNode.insertBefore(e, t) : n.insertBefore(e, t) : (n.nodeType === 8 ? (t = n.parentNode, t.insertBefore(e, n)) : (t = n, t.appendChild(e)), n = n._reactRootContainer, n != null || t.onclick !== null || (t.onclick = ji));
		else if (r !== 4 && (e = e.child, e !== null)) for (jc(e, t, n), e = e.sibling; e !== null;) jc(e, t, n), e = e.sibling;
	}
	function Mc(e, t, n) {
		var r = e.tag;
		if (r === 5 || r === 6) e = e.stateNode, t ? n.insertBefore(e, t) : n.appendChild(e);
		else if (r !== 4 && (e = e.child, e !== null)) for (Mc(e, t, n), e = e.sibling; e !== null;) Mc(e, t, n), e = e.sibling;
	}
	var U = null, Nc = !1;
	function Pc(e, t, n) {
		for (n = n.child; n !== null;) Fc(e, t, n), n = n.sibling;
	}
	function Fc(e, t, n) {
		if (Ft && typeof Ft.onCommitFiberUnmount == "function") try {
			Ft.onCommitFiberUnmount(Pt, n);
		} catch {}
		switch (n.tag) {
			case 5: V || xc(n, t);
			case 6:
				var r = U, i = Nc;
				U = null, Pc(e, t, n), U = r, Nc = i, U !== null && (Nc ? (e = U, n = n.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(n) : e.removeChild(n)) : U.removeChild(n.stateNode));
				break;
			case 18:
				U !== null && (Nc ? (e = U, n = n.stateNode, e.nodeType === 8 ? Bi(e.parentNode, n) : e.nodeType === 1 && Bi(e, n), Sn(e)) : Bi(U, n.stateNode));
				break;
			case 4:
				r = U, i = Nc, U = n.stateNode.containerInfo, Nc = !0, Pc(e, t, n), U = r, Nc = i;
				break;
			case 0:
			case 11:
			case 14:
			case 15:
				if (!V && (r = n.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
					i = r = r.next;
					do {
						var a = i, o = a.destroy;
						a = a.tag, o !== void 0 && (a & 2 || a & 4) && Sc(n, t, o), i = i.next;
					} while (i !== r);
				}
				Pc(e, t, n);
				break;
			case 1:
				if (!V && (xc(n, t), r = n.stateNode, typeof r.componentWillUnmount == "function")) try {
					r.props = n.memoizedProps, r.state = n.memoizedState, r.componentWillUnmount();
				} catch (e) {
					Y(n, t, e);
				}
				Pc(e, t, n);
				break;
			case 21:
				Pc(e, t, n);
				break;
			case 22:
				n.mode & 1 ? (V = (r = V) || n.memoizedState !== null, Pc(e, t, n), V = r) : Pc(e, t, n);
				break;
			default: Pc(e, t, n);
		}
	}
	function Ic(e) {
		var t = e.updateQueue;
		if (t !== null) {
			e.updateQueue = null;
			var n = e.stateNode;
			n === null && (n = e.stateNode = new bc()), t.forEach(function(t) {
				var r = Gl.bind(null, e, t);
				n.has(t) || (n.add(t), t.then(r, r));
			});
		}
	}
	function Lc(e, t) {
		var n = t.deletions;
		if (n !== null) for (var i = 0; i < n.length; i++) {
			var a = n[i];
			try {
				var o = e, s = t, c = s;
				a: for (; c !== null;) {
					switch (c.tag) {
						case 5:
							U = c.stateNode, Nc = !1;
							break a;
						case 3:
							U = c.stateNode.containerInfo, Nc = !0;
							break a;
						case 4:
							U = c.stateNode.containerInfo, Nc = !0;
							break a;
					}
					c = c.return;
				}
				if (U === null) throw Error(r(160));
				Fc(o, s, a), U = null, Nc = !1;
				var l = a.alternate;
				l !== null && (l.return = null), a.return = null;
			} catch (e) {
				Y(a, t, e);
			}
		}
		if (t.subtreeFlags & 12854) for (t = t.child; t !== null;) Rc(t, e), t = t.sibling;
	}
	function Rc(e, t) {
		var n = e.alternate, i = e.flags;
		switch (e.tag) {
			case 0:
			case 11:
			case 14:
			case 15:
				if (Lc(t, e), zc(e), i & 4) {
					try {
						Tc(3, e, e.return), Ec(3, e);
					} catch (t) {
						Y(e, e.return, t);
					}
					try {
						Tc(5, e, e.return);
					} catch (t) {
						Y(e, e.return, t);
					}
				}
				break;
			case 1:
				Lc(t, e), zc(e), i & 512 && n !== null && xc(n, n.return);
				break;
			case 5:
				if (Lc(t, e), zc(e), i & 512 && n !== null && xc(n, n.return), e.flags & 32) {
					var a = e.stateNode;
					try {
						Ve(a, "");
					} catch (t) {
						Y(e, e.return, t);
					}
				}
				if (i & 4 && (a = e.stateNode, a != null)) {
					var o = e.memoizedProps, s = n === null ? o : n.memoizedProps, c = e.type, l = e.updateQueue;
					if (e.updateQueue = null, l !== null) try {
						c === "input" && o.type === "radio" && o.name != null && De(a, o), Je(c, s);
						var u = Je(c, o);
						for (s = 0; s < l.length; s += 2) {
							var d = l[s], f = l[s + 1];
							d === "style" ? Ge(a, f) : d === "dangerouslySetInnerHTML" ? Be(a, f) : d === "children" ? Ve(a, f) : b(a, d, f, u);
						}
						switch (c) {
							case "input":
								Oe(a, o);
								break;
							case "textarea":
								Fe(a, o);
								break;
							case "select":
								var p = a._wrapperState.wasMultiple;
								a._wrapperState.wasMultiple = !!o.multiple;
								var m = o.value;
								m == null ? p !== !!o.multiple && (o.defaultValue == null ? Me(a, !!o.multiple, o.multiple ? [] : "", !1) : Me(a, !!o.multiple, o.defaultValue, !0)) : Me(a, !!o.multiple, m, !1);
						}
						a[Gi] = o;
					} catch (t) {
						Y(e, e.return, t);
					}
				}
				break;
			case 6:
				if (Lc(t, e), zc(e), i & 4) {
					if (e.stateNode === null) throw Error(r(162));
					a = e.stateNode, o = e.memoizedProps;
					try {
						a.nodeValue = o;
					} catch (t) {
						Y(e, e.return, t);
					}
				}
				break;
			case 3:
				if (Lc(t, e), zc(e), i & 4 && n !== null && n.memoizedState.isDehydrated) try {
					Sn(t.containerInfo);
				} catch (t) {
					Y(e, e.return, t);
				}
				break;
			case 4:
				Lc(t, e), zc(e);
				break;
			case 13:
				Lc(t, e), zc(e), a = e.child, a.flags & 8192 && (o = a.memoizedState !== null, a.stateNode.isHidden = o, !o || a.alternate !== null && a.alternate.memoizedState !== null || (rl = E())), i & 4 && Ic(e);
				break;
			case 22:
				if (d = n !== null && n.memoizedState !== null, e.mode & 1 ? (V = (u = V) || d, Lc(t, e), V = u) : Lc(t, e), zc(e), i & 8192) {
					if (u = e.memoizedState !== null, (e.stateNode.isHidden = u) && !d && e.mode & 1) for (H = e, d = e.child; d !== null;) {
						for (f = H = d; H !== null;) {
							switch (p = H, m = p.child, p.tag) {
								case 0:
								case 11:
								case 14:
								case 15:
									Tc(4, p, p.return);
									break;
								case 1:
									xc(p, p.return);
									var h = p.stateNode;
									if (typeof h.componentWillUnmount == "function") {
										i = p, n = p.return;
										try {
											t = i, h.props = t.memoizedProps, h.state = t.memoizedState, h.componentWillUnmount();
										} catch (e) {
											Y(i, n, e);
										}
									}
									break;
								case 5:
									xc(p, p.return);
									break;
								case 22: if (p.memoizedState !== null) {
									Uc(f);
									continue;
								}
							}
							m === null ? Uc(f) : (m.return = p, H = m);
						}
						d = d.sibling;
					}
					a: for (d = null, f = e;;) {
						if (f.tag === 5) {
							if (d === null) {
								d = f;
								try {
									a = f.stateNode, u ? (o = a.style, typeof o.setProperty == "function" ? o.setProperty("display", "none", "important") : o.display = "none") : (c = f.stateNode, l = f.memoizedProps.style, s = l != null && l.hasOwnProperty("display") ? l.display : null, c.style.display = We("display", s));
								} catch (t) {
									Y(e, e.return, t);
								}
							}
						} else if (f.tag === 6) {
							if (d === null) try {
								f.stateNode.nodeValue = u ? "" : f.memoizedProps;
							} catch (t) {
								Y(e, e.return, t);
							}
						} else if ((f.tag !== 22 && f.tag !== 23 || f.memoizedState === null || f === e) && f.child !== null) {
							f.child.return = f, f = f.child;
							continue;
						}
						if (f === e) break a;
						for (; f.sibling === null;) {
							if (f.return === null || f.return === e) break a;
							d === f && (d = null), f = f.return;
						}
						d === f && (d = null), f.sibling.return = f.return, f = f.sibling;
					}
				}
				break;
			case 19:
				Lc(t, e), zc(e), i & 4 && Ic(e);
				break;
			case 21: break;
			default: Lc(t, e), zc(e);
		}
	}
	function zc(e) {
		var t = e.flags;
		if (t & 2) {
			try {
				a: {
					for (var n = e.return; n !== null;) {
						if (kc(n)) {
							var i = n;
							break a;
						}
						n = n.return;
					}
					throw Error(r(160));
				}
				switch (i.tag) {
					case 5:
						var a = i.stateNode;
						i.flags & 32 && (Ve(a, ""), i.flags &= -33), Mc(e, Ac(e), a);
						break;
					case 3:
					case 4:
						var o = i.stateNode.containerInfo;
						jc(e, Ac(e), o);
						break;
					default: throw Error(r(161));
				}
			} catch (t) {
				Y(e, e.return, t);
			}
			e.flags &= -3;
		}
		t & 4096 && (e.flags &= -4097);
	}
	function Bc(e, t, n) {
		H = e, Vc(e, t, n);
	}
	function Vc(e, t, n) {
		for (var r = (e.mode & 1) != 0; H !== null;) {
			var i = H, a = i.child;
			if (i.tag === 22 && r) {
				var o = i.memoizedState !== null || yc;
				if (!o) {
					var s = i.alternate, c = s !== null && s.memoizedState !== null || V;
					s = yc;
					var l = V;
					if (yc = o, (V = c) && !l) for (H = i; H !== null;) o = H, c = o.child, o.tag === 22 && o.memoizedState !== null || c === null ? Wc(i) : (c.return = o, H = c);
					for (; a !== null;) H = a, Vc(a, t, n), a = a.sibling;
					H = i, yc = s, V = l;
				}
				Hc(e, t, n);
			} else i.subtreeFlags & 8772 && a !== null ? (a.return = i, H = a) : Hc(e, t, n);
		}
	}
	function Hc(e) {
		for (; H !== null;) {
			var t = H;
			if (t.flags & 8772) {
				var n = t.alternate;
				try {
					if (t.flags & 8772) switch (t.tag) {
						case 0:
						case 11:
						case 15:
							V || Ec(5, t);
							break;
						case 1:
							var i = t.stateNode;
							if (t.flags & 4 && !V) if (n === null) i.componentDidMount();
							else {
								var a = t.elementType === t.type ? n.memoizedProps : Es(t.type, n.memoizedProps);
								i.componentDidUpdate(a, n.memoizedState, i.__reactInternalSnapshotBeforeUpdate);
							}
							var o = t.updateQueue;
							o !== null && yo(t, o, i);
							break;
						case 3:
							var s = t.updateQueue;
							if (s !== null) {
								if (n = null, t.child !== null) switch (t.child.tag) {
									case 5:
										n = t.child.stateNode;
										break;
									case 1: n = t.child.stateNode;
								}
								yo(t, s, n);
							}
							break;
						case 5:
							var c = t.stateNode;
							if (n === null && t.flags & 4) {
								n = c;
								var l = t.memoizedProps;
								switch (t.type) {
									case "button":
									case "input":
									case "select":
									case "textarea":
										l.autoFocus && n.focus();
										break;
									case "img": l.src && (n.src = l.src);
								}
							}
							break;
						case 6: break;
						case 4: break;
						case 12: break;
						case 13:
							if (t.memoizedState === null) {
								var u = t.alternate;
								if (u !== null) {
									var d = u.memoizedState;
									if (d !== null) {
										var f = d.dehydrated;
										f !== null && Sn(f);
									}
								}
							}
							break;
						case 19:
						case 17:
						case 21:
						case 22:
						case 23:
						case 25: break;
						default: throw Error(r(163));
					}
					V || t.flags & 512 && Dc(t);
				} catch (e) {
					Y(t, t.return, e);
				}
			}
			if (t === e) {
				H = null;
				break;
			}
			if (n = t.sibling, n !== null) {
				n.return = t.return, H = n;
				break;
			}
			H = t.return;
		}
	}
	function Uc(e) {
		for (; H !== null;) {
			var t = H;
			if (t === e) {
				H = null;
				break;
			}
			var n = t.sibling;
			if (n !== null) {
				n.return = t.return, H = n;
				break;
			}
			H = t.return;
		}
	}
	function Wc(e) {
		for (; H !== null;) {
			var t = H;
			try {
				switch (t.tag) {
					case 0:
					case 11:
					case 15:
						var n = t.return;
						try {
							Ec(4, t);
						} catch (e) {
							Y(t, n, e);
						}
						break;
					case 1:
						var r = t.stateNode;
						if (typeof r.componentDidMount == "function") {
							var i = t.return;
							try {
								r.componentDidMount();
							} catch (e) {
								Y(t, i, e);
							}
						}
						var a = t.return;
						try {
							Dc(t);
						} catch (e) {
							Y(t, a, e);
						}
						break;
					case 5:
						var o = t.return;
						try {
							Dc(t);
						} catch (e) {
							Y(t, o, e);
						}
				}
			} catch (e) {
				Y(t, t.return, e);
			}
			if (t === e) {
				H = null;
				break;
			}
			var s = t.sibling;
			if (s !== null) {
				s.return = t.return, H = s;
				break;
			}
			H = t.return;
		}
	}
	var Gc = Math.ceil, Kc = x.ReactCurrentDispatcher, qc = x.ReactCurrentOwner, Jc = x.ReactCurrentBatchConfig, W = 0, G = null, K = null, q = 0, Yc = 0, Xc = na(0), J = 0, Zc = null, Qc = 0, $c = 0, el = 0, tl = null, nl = null, rl = 0, il = Infinity, al = null, ol = !1, sl = null, cl = null, ll = !1, ul = null, dl = 0, fl = 0, pl = null, ml = -1, hl = 0;
	function gl() {
		return W & 6 ? E() : ml === -1 ? ml = E() : ml;
	}
	function _l(e) {
		return e.mode & 1 ? W & 2 && q !== 0 ? q & -q : Wa.transition === null ? (e = k, e === 0 ? (e = window.event, e = e === void 0 ? 16 : An(e.type), e) : e) : (hl === 0 && (hl = qt()), hl) : 1;
	}
	function vl(e, t, n, i) {
		if (50 < fl) throw fl = 0, pl = null, Error(r(185));
		Yt(e, n, i), (!(W & 2) || e !== G) && (e === G && (!(W & 2) && ($c |= n), J === 4 && wl(e, q)), yl(e, i), n === 1 && W === 0 && !(t.mode & 1) && (il = E() + 500, ma && va()));
	}
	function yl(e, t) {
		var n = e.callbackNode;
		Gt(e, t);
		var r = Ut(e, e === G ? q : 0);
		if (r === 0) n !== null && Tt(n), e.callbackNode = null, e.callbackPriority = 0;
		else if (t = r & -r, e.callbackPriority !== t) {
			if (n != null && Tt(n), t === 1) e.tag === 0 ? _a(Tl.bind(null, e)) : ga(Tl.bind(null, e)), Ri(function() {
				!(W & 6) && va();
			}), n = null;
			else {
				switch (Qt(r)) {
					case 1:
						n = At;
						break;
					case 4:
						n = jt;
						break;
					case 16:
						n = Mt;
						break;
					case 536870912:
						n = D;
						break;
					default: n = Mt;
				}
				n = ql(n, bl.bind(null, e));
			}
			e.callbackPriority = t, e.callbackNode = n;
		}
	}
	function bl(e, t) {
		if (ml = -1, hl = 0, W & 6) throw Error(r(327));
		var n = e.callbackNode;
		if (Bl() && e.callbackNode !== n) return null;
		var i = Ut(e, e === G ? q : 0);
		if (i === 0) return null;
		if (i & 30 || (i & e.expiredLanes) !== 0 || t) t = Nl(e, i);
		else {
			t = i;
			var a = W;
			W |= 2;
			var o = jl();
			(G !== e || q !== t) && (al = null, il = E() + 500, kl(e, t));
			do
				try {
					Fl();
					break;
				} catch (t) {
					Al(e, t);
				}
			while (1);
			to(), Kc.current = o, W = a, K === null ? (G = null, q = 0, t = J) : t = 0;
		}
		if (t !== 0) {
			if (t === 2 && (a = Kt(e), a !== 0 && (i = a, t = xl(e, a))), t === 1) throw n = Zc, kl(e, 0), wl(e, i), yl(e, E()), n;
			if (t === 6) wl(e, i);
			else {
				if (a = e.current.alternate, !(i & 30) && !Cl(a) && (t = Nl(e, i), t === 2 && (o = Kt(e), o !== 0 && (i = o, t = xl(e, o))), t === 1)) throw n = Zc, kl(e, 0), wl(e, i), yl(e, E()), n;
				switch (e.finishedWork = a, e.finishedLanes = i, t) {
					case 0:
					case 1: throw Error(r(345));
					case 2:
						Rl(e, nl, al);
						break;
					case 3:
						if (wl(e, i), (i & 130023424) === i && (t = rl + 500 - E(), 10 < t)) {
							if (Ut(e, 0) !== 0) break;
							if (a = e.suspendedLanes, (a & i) !== i) {
								gl(), e.pingedLanes |= e.suspendedLanes & a;
								break;
							}
							e.timeoutHandle = Fi(Rl.bind(null, e, nl, al), t);
							break;
						}
						Rl(e, nl, al);
						break;
					case 4:
						if (wl(e, i), (i & 4194240) === i) break;
						for (t = e.eventTimes, a = -1; 0 < i;) {
							var s = 31 - O(i);
							o = 1 << s, s = t[s], s > a && (a = s), i &= ~o;
						}
						if (i = a, i = E() - i, i = (120 > i ? 120 : 480 > i ? 480 : 1080 > i ? 1080 : 1920 > i ? 1920 : 3e3 > i ? 3e3 : 4320 > i ? 4320 : 1960 * Gc(i / 1960)) - i, 10 < i) {
							e.timeoutHandle = Fi(Rl.bind(null, e, nl, al), i);
							break;
						}
						Rl(e, nl, al);
						break;
					case 5:
						Rl(e, nl, al);
						break;
					default: throw Error(r(329));
				}
			}
		}
		return yl(e, E()), e.callbackNode === n ? bl.bind(null, e) : null;
	}
	function xl(e, t) {
		var n = tl;
		return e.current.memoizedState.isDehydrated && (kl(e, t).flags |= 256), e = Nl(e, t), e !== 2 && (t = nl, nl = n, t !== null && Sl(t)), e;
	}
	function Sl(e) {
		nl === null ? nl = e : nl.push.apply(nl, e);
	}
	function Cl(e) {
		for (var t = e;;) {
			if (t.flags & 16384) {
				var n = t.updateQueue;
				if (n !== null && (n = n.stores, n !== null)) for (var r = 0; r < n.length; r++) {
					var i = n[r], a = i.getSnapshot;
					i = i.value;
					try {
						if (!Br(a(), i)) return !1;
					} catch {
						return !1;
					}
				}
			}
			if (n = t.child, t.subtreeFlags & 16384 && n !== null) n.return = t, t = n;
			else {
				if (t === e) break;
				for (; t.sibling === null;) {
					if (t.return === null || t.return === e) return !0;
					t = t.return;
				}
				t.sibling.return = t.return, t = t.sibling;
			}
		}
		return !0;
	}
	function wl(e, t) {
		for (t &= ~el, t &= ~$c, e.suspendedLanes |= t, e.pingedLanes &= ~t, e = e.expirationTimes; 0 < t;) {
			var n = 31 - O(t), r = 1 << n;
			e[n] = -1, t &= ~r;
		}
	}
	function Tl(e) {
		if (W & 6) throw Error(r(327));
		Bl();
		var t = Ut(e, 0);
		if (!(t & 1)) return yl(e, E()), null;
		var n = Nl(e, t);
		if (e.tag !== 0 && n === 2) {
			var i = Kt(e);
			i !== 0 && (t = i, n = xl(e, i));
		}
		if (n === 1) throw n = Zc, kl(e, 0), wl(e, t), yl(e, E()), n;
		if (n === 6) throw Error(r(345));
		return e.finishedWork = e.current.alternate, e.finishedLanes = t, Rl(e, nl, al), yl(e, E()), null;
	}
	function El(e, t) {
		var n = W;
		W |= 1;
		try {
			return e(t);
		} finally {
			W = n, W === 0 && (il = E() + 500, ma && va());
		}
	}
	function Dl(e) {
		ul !== null && ul.tag === 0 && !(W & 6) && Bl();
		var t = W;
		W |= 1;
		var n = Jc.transition, r = k;
		try {
			if (Jc.transition = null, k = 1, e) return e();
		} finally {
			k = r, Jc.transition = n, W = t, !(W & 6) && va();
		}
	}
	function Ol() {
		Yc = Xc.current, j(Xc);
	}
	function kl(e, t) {
		e.finishedWork = null, e.finishedLanes = 0;
		var n = e.timeoutHandle;
		if (n !== -1 && (e.timeoutHandle = -1, Ii(n)), K !== null) for (n = K.return; n !== null;) {
			var r = n;
			switch (ja(r), r.tag) {
				case 1:
					r = r.type.childContextTypes, r != null && ca();
					break;
				case 3:
					Eo(), j(ia), j(N), jo();
					break;
				case 5:
					Oo(r);
					break;
				case 4:
					Eo();
					break;
				case 13:
					j(F);
					break;
				case 19:
					j(F);
					break;
				case 10:
					no(r.type._context);
					break;
				case 22:
				case 23: Ol();
			}
			n = n.return;
		}
		if (G = e, K = e = Ql(e.current, null), q = Yc = t, J = 0, Zc = null, el = $c = Qc = 0, nl = tl = null, oo !== null) {
			for (t = 0; t < oo.length; t++) if (n = oo[t], r = n.interleaved, r !== null) {
				n.interleaved = null;
				var i = r.next, a = n.pending;
				if (a !== null) {
					var o = a.next;
					a.next = i, r.next = o;
				}
				n.pending = r;
			}
			oo = null;
		}
		return e;
	}
	function Al(e, t) {
		do {
			var n = K;
			try {
				if (to(), Mo.current = Ss, Fo) {
					for (var i = I.memoizedState; i !== null;) {
						var a = i.queue;
						a !== null && (a.pending = null), i = i.next;
					}
					Fo = !1;
				}
				if (Po = 0, R = L = I = null, Io = !1, Lo = 0, qc.current = null, n === null || n.return === null) {
					J = 1, Zc = t, K = null;
					break;
				}
				a: {
					var o = e, s = n.return, c = n, l = t;
					if (t = q, c.flags |= 32768, typeof l == "object" && l && typeof l.then == "function") {
						var u = l, d = c, f = d.tag;
						if (!(d.mode & 1) && (f === 0 || f === 11 || f === 15)) {
							var p = d.alternate;
							p ? (d.updateQueue = p.updateQueue, d.memoizedState = p.memoizedState, d.lanes = p.lanes) : (d.updateQueue = null, d.memoizedState = null);
						}
						var m = Bs(s);
						if (m !== null) {
							m.flags &= -257, Vs(m, s, c, o, t), m.mode & 1 && zs(o, u, t), t = m, l = u;
							var h = t.updateQueue;
							if (h === null) {
								var g = /* @__PURE__ */ new Set();
								g.add(l), t.updateQueue = g;
							} else h.add(l);
							break a;
						} else {
							if (!(t & 1)) {
								zs(o, u, t), Ml();
								break a;
							}
							l = Error(r(426));
						}
					} else if (P && c.mode & 1) {
						var _ = Bs(s);
						if (_ !== null) {
							!(_.flags & 65536) && (_.flags |= 256), Vs(_, s, c, o, t), Ua(Ns(l, c));
							break a;
						}
					}
					o = l = Ns(l, c), J !== 4 && (J = 2), tl === null ? tl = [o] : tl.push(o), o = s;
					do {
						switch (o.tag) {
							case 3:
								o.flags |= 65536, t &= -t, o.lanes |= t;
								var v = Ls(o, l, t);
								_o(o, v);
								break a;
							case 1:
								c = l;
								var y = o.type, b = o.stateNode;
								if (!(o.flags & 128) && (typeof y.getDerivedStateFromError == "function" || b !== null && typeof b.componentDidCatch == "function" && (cl === null || !cl.has(b)))) {
									o.flags |= 65536, t &= -t, o.lanes |= t;
									var x = Rs(o, c, t);
									_o(o, x);
									break a;
								}
						}
						o = o.return;
					} while (o !== null);
				}
				Ll(n);
			} catch (e) {
				t = e, K === n && n !== null && (K = n = n.return);
				continue;
			}
			break;
		} while (1);
	}
	function jl() {
		var e = Kc.current;
		return Kc.current = Ss, e === null ? Ss : e;
	}
	function Ml() {
		(J === 0 || J === 3 || J === 2) && (J = 4), G === null || !(Qc & 268435455) && !($c & 268435455) || wl(G, q);
	}
	function Nl(e, t) {
		var n = W;
		W |= 2;
		var i = jl();
		(G !== e || q !== t) && (al = null, kl(e, t));
		do
			try {
				Pl();
				break;
			} catch (t) {
				Al(e, t);
			}
		while (1);
		if (to(), W = n, Kc.current = i, K !== null) throw Error(r(261));
		return G = null, q = 0, J;
	}
	function Pl() {
		for (; K !== null;) Il(K);
	}
	function Fl() {
		for (; K !== null && !Et();) Il(K);
	}
	function Il(e) {
		var t = Kl(e.alternate, e, Yc);
		e.memoizedProps = e.pendingProps, t === null ? Ll(e) : K = t, qc.current = null;
	}
	function Ll(e) {
		var t = e;
		do {
			var n = t.alternate;
			if (e = t.return, t.flags & 32768) {
				if (n = vc(n, t), n !== null) {
					n.flags &= 32767, K = n;
					return;
				}
				if (e !== null) e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
				else {
					J = 6, K = null;
					return;
				}
			} else if (n = _c(n, t, Yc), n !== null) {
				K = n;
				return;
			}
			if (t = t.sibling, t !== null) {
				K = t;
				return;
			}
			K = t = e;
		} while (t !== null);
		J === 0 && (J = 5);
	}
	function Rl(e, t, n) {
		var r = k, i = Jc.transition;
		try {
			Jc.transition = null, k = 1, zl(e, t, n, r);
		} finally {
			Jc.transition = i, k = r;
		}
		return null;
	}
	function zl(e, t, n, i) {
		do
			Bl();
		while (ul !== null);
		if (W & 6) throw Error(r(327));
		n = e.finishedWork;
		var a = e.finishedLanes;
		if (n === null) return null;
		if (e.finishedWork = null, e.finishedLanes = 0, n === e.current) throw Error(r(177));
		e.callbackNode = null, e.callbackPriority = 0;
		var o = n.lanes | n.childLanes;
		if (Xt(e, o), e === G && (K = G = null, q = 0), !(n.subtreeFlags & 2064) && !(n.flags & 2064) || ll || (ll = !0, ql(Mt, function() {
			return Bl(), null;
		})), o = (n.flags & 15990) != 0, n.subtreeFlags & 15990 || o) {
			o = Jc.transition, Jc.transition = null;
			var s = k;
			k = 1;
			var c = W;
			W |= 4, qc.current = null, wc(e, n), Rc(n, e), qr(Ni), wn = !!Mi, Ni = Mi = null, e.current = n, Bc(n, e, a), Dt(), W = c, k = s, Jc.transition = o;
		} else e.current = n;
		if (ll && (ll = !1, ul = e, dl = a), o = e.pendingLanes, o === 0 && (cl = null), It(n.stateNode, i), yl(e, E()), t !== null) for (i = e.onRecoverableError, n = 0; n < t.length; n++) a = t[n], i(a.value, {
			componentStack: a.stack,
			digest: a.digest
		});
		if (ol) throw ol = !1, e = sl, sl = null, e;
		return dl & 1 && e.tag !== 0 && Bl(), o = e.pendingLanes, o & 1 ? e === pl ? fl++ : (fl = 0, pl = e) : fl = 0, va(), null;
	}
	function Bl() {
		if (ul !== null) {
			var e = Qt(dl), t = Jc.transition, n = k;
			try {
				if (Jc.transition = null, k = 16 > e ? 16 : e, ul === null) var i = !1;
				else {
					if (e = ul, ul = null, dl = 0, W & 6) throw Error(r(331));
					var a = W;
					for (W |= 4, H = e.current; H !== null;) {
						var o = H, s = o.child;
						if (H.flags & 16) {
							var c = o.deletions;
							if (c !== null) {
								for (var l = 0; l < c.length; l++) {
									var u = c[l];
									for (H = u; H !== null;) {
										var d = H;
										switch (d.tag) {
											case 0:
											case 11:
											case 15: Tc(8, d, o);
										}
										var f = d.child;
										if (f !== null) f.return = d, H = f;
										else for (; H !== null;) {
											d = H;
											var p = d.sibling, m = d.return;
											if (Oc(d), d === u) {
												H = null;
												break;
											}
											if (p !== null) {
												p.return = m, H = p;
												break;
											}
											H = m;
										}
									}
								}
								var h = o.alternate;
								if (h !== null) {
									var g = h.child;
									if (g !== null) {
										h.child = null;
										do {
											var _ = g.sibling;
											g.sibling = null, g = _;
										} while (g !== null);
									}
								}
								H = o;
							}
						}
						if (o.subtreeFlags & 2064 && s !== null) s.return = o, H = s;
						else b: for (; H !== null;) {
							if (o = H, o.flags & 2048) switch (o.tag) {
								case 0:
								case 11:
								case 15: Tc(9, o, o.return);
							}
							var v = o.sibling;
							if (v !== null) {
								v.return = o.return, H = v;
								break b;
							}
							H = o.return;
						}
					}
					var y = e.current;
					for (H = y; H !== null;) {
						s = H;
						var b = s.child;
						if (s.subtreeFlags & 2064 && b !== null) b.return = s, H = b;
						else b: for (s = y; H !== null;) {
							if (c = H, c.flags & 2048) try {
								switch (c.tag) {
									case 0:
									case 11:
									case 15: Ec(9, c);
								}
							} catch (e) {
								Y(c, c.return, e);
							}
							if (c === s) {
								H = null;
								break b;
							}
							var x = c.sibling;
							if (x !== null) {
								x.return = c.return, H = x;
								break b;
							}
							H = c.return;
						}
					}
					if (W = a, va(), Ft && typeof Ft.onPostCommitFiberRoot == "function") try {
						Ft.onPostCommitFiberRoot(Pt, e);
					} catch {}
					i = !0;
				}
				return i;
			} finally {
				k = n, Jc.transition = t;
			}
		}
		return !1;
	}
	function Vl(e, t, n) {
		t = Ns(n, t), t = Ls(e, t, 1), e = ho(e, t, 1), t = gl(), e !== null && (Yt(e, 1, t), yl(e, t));
	}
	function Y(e, t, n) {
		if (e.tag === 3) Vl(e, e, n);
		else for (; t !== null;) {
			if (t.tag === 3) {
				Vl(t, e, n);
				break;
			} else if (t.tag === 1) {
				var r = t.stateNode;
				if (typeof t.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (cl === null || !cl.has(r))) {
					e = Ns(n, e), e = Rs(t, e, 1), t = ho(t, e, 1), e = gl(), t !== null && (Yt(t, 1, e), yl(t, e));
					break;
				}
			}
			t = t.return;
		}
	}
	function Hl(e, t, n) {
		var r = e.pingCache;
		r !== null && r.delete(t), t = gl(), e.pingedLanes |= e.suspendedLanes & n, G === e && (q & n) === n && (J === 4 || J === 3 && (q & 130023424) === q && 500 > E() - rl ? kl(e, 0) : el |= n), yl(e, t);
	}
	function Ul(e, t) {
		t === 0 && (e.mode & 1 ? (t = Vt, Vt <<= 1, !(Vt & 130023424) && (Vt = 4194304)) : t = 1);
		var n = gl();
		e = lo(e, t), e !== null && (Yt(e, t, n), yl(e, n));
	}
	function Wl(e) {
		var t = e.memoizedState, n = 0;
		t !== null && (n = t.retryLane), Ul(e, n);
	}
	function Gl(e, t) {
		var n = 0;
		switch (e.tag) {
			case 13:
				var i = e.stateNode, a = e.memoizedState;
				a !== null && (n = a.retryLane);
				break;
			case 19:
				i = e.stateNode;
				break;
			default: throw Error(r(314));
		}
		i !== null && i.delete(t), Ul(e, n);
	}
	var Kl = function(e, t, n) {
		if (e !== null) if (e.memoizedProps !== t.pendingProps || ia.current) Us = !0;
		else {
			if ((e.lanes & n) === 0 && !(t.flags & 128)) return Us = !1, fc(e, t, n);
			Us = !!(e.flags & 131072);
		}
		else Us = !1, P && t.flags & 1048576 && ka(t, Sa, t.index);
		switch (t.lanes = 0, t.tag) {
			case 2:
				var i = t.type;
				uc(e, t), e = t.pendingProps;
				var a = oa(t, N.current);
				io(t, n), a = Bo(null, t, i, e, a, n);
				var o = Vo();
				return t.flags |= 1, typeof a == "object" && a && typeof a.render == "function" && a.$$typeof === void 0 ? (t.tag = 1, t.memoizedState = null, t.updateQueue = null, sa(i) ? (o = !0, da(t)) : o = !1, t.memoizedState = a.state !== null && a.state !== void 0 ? a.state : null, fo(t), a.updater = Os, t.stateNode = a, a._reactInternals = t, Ms(t, i, e, n), t = Qs(null, t, i, !0, o, n)) : (t.tag = 0, P && o && Aa(t), Ws(null, t, a, n), t = t.child), t;
			case 16:
				i = t.elementType;
				a: {
					switch (uc(e, t), e = t.pendingProps, a = i._init, i = a(i._payload), t.type = i, a = t.tag = Zl(i), e = Es(i, e), a) {
						case 0:
							t = Xs(null, t, i, e, n);
							break a;
						case 1:
							t = Zs(null, t, i, e, n);
							break a;
						case 11:
							t = Gs(null, t, i, e, n);
							break a;
						case 14:
							t = Ks(null, t, i, Es(i.type, e), n);
							break a;
					}
					throw Error(r(306, i, ""));
				}
				return t;
			case 0: return i = t.type, a = t.pendingProps, a = t.elementType === i ? a : Es(i, a), Xs(e, t, i, a, n);
			case 1: return i = t.type, a = t.pendingProps, a = t.elementType === i ? a : Es(i, a), Zs(e, t, i, a, n);
			case 3:
				a: {
					if ($s(t), e === null) throw Error(r(387));
					i = t.pendingProps, o = t.memoizedState, a = o.element, po(e, t), vo(t, i, null, n);
					var s = t.memoizedState;
					if (i = s.element, o.isDehydrated) if (o = {
						element: i,
						isDehydrated: !1,
						cache: s.cache,
						pendingSuspenseBoundaries: s.pendingSuspenseBoundaries,
						transitions: s.transitions
					}, t.updateQueue.baseState = o, t.memoizedState = o, t.flags & 256) {
						a = Ns(Error(r(423)), t), t = ec(e, t, i, n, a);
						break a;
					} else if (i !== a) {
						a = Ns(Error(r(424)), t), t = ec(e, t, i, n, a);
						break a;
					} else for (Na = Vi(t.stateNode.containerInfo.firstChild), Ma = t, P = !0, Pa = null, n = Xa(t, null, i, n), t.child = n; n;) n.flags = n.flags & -3 | 4096, n = n.sibling;
					else {
						if (Ha(), i === a) {
							t = dc(e, t, n);
							break a;
						}
						Ws(e, t, i, n);
					}
					t = t.child;
				}
				return t;
			case 5: return Do(t), e === null && Ra(t), i = t.type, a = t.pendingProps, o = e === null ? null : e.memoizedProps, s = a.children, Pi(i, a) ? s = null : o !== null && Pi(i, o) && (t.flags |= 32), Ys(e, t), Ws(e, t, s, n), t.child;
			case 6: return e === null && Ra(t), null;
			case 13: return rc(e, t, n);
			case 4: return To(t, t.stateNode.containerInfo), i = t.pendingProps, e === null ? t.child = Ya(t, null, i, n) : Ws(e, t, i, n), t.child;
			case 11: return i = t.type, a = t.pendingProps, a = t.elementType === i ? a : Es(i, a), Gs(e, t, i, a, n);
			case 7: return Ws(e, t, t.pendingProps, n), t.child;
			case 8: return Ws(e, t, t.pendingProps.children, n), t.child;
			case 12: return Ws(e, t, t.pendingProps.children, n), t.child;
			case 10:
				a: {
					if (i = t.type._context, a = t.pendingProps, o = t.memoizedProps, s = a.value, M(Za, i._currentValue), i._currentValue = s, o !== null) if (Br(o.value, s)) {
						if (o.children === a.children && !ia.current) {
							t = dc(e, t, n);
							break a;
						}
					} else for (o = t.child, o !== null && (o.return = t); o !== null;) {
						var c = o.dependencies;
						if (c !== null) {
							s = o.child;
							for (var l = c.firstContext; l !== null;) {
								if (l.context === i) {
									if (o.tag === 1) {
										l = mo(-1, n & -n), l.tag = 2;
										var u = o.updateQueue;
										if (u !== null) {
											u = u.shared;
											var d = u.pending;
											d === null ? l.next = l : (l.next = d.next, d.next = l), u.pending = l;
										}
									}
									o.lanes |= n, l = o.alternate, l !== null && (l.lanes |= n), ro(o.return, n, t), c.lanes |= n;
									break;
								}
								l = l.next;
							}
						} else if (o.tag === 10) s = o.type === t.type ? null : o.child;
						else if (o.tag === 18) {
							if (s = o.return, s === null) throw Error(r(341));
							s.lanes |= n, c = s.alternate, c !== null && (c.lanes |= n), ro(s, n, t), s = o.sibling;
						} else s = o.child;
						if (s !== null) s.return = o;
						else for (s = o; s !== null;) {
							if (s === t) {
								s = null;
								break;
							}
							if (o = s.sibling, o !== null) {
								o.return = s.return, s = o;
								break;
							}
							s = s.return;
						}
						o = s;
					}
					Ws(e, t, a.children, n), t = t.child;
				}
				return t;
			case 9: return a = t.type, i = t.pendingProps.children, io(t, n), a = ao(a), i = i(a), t.flags |= 1, Ws(e, t, i, n), t.child;
			case 14: return i = t.type, a = Es(i, t.pendingProps), a = Es(i.type, a), Ks(e, t, i, a, n);
			case 15: return qs(e, t, t.type, t.pendingProps, n);
			case 17: return i = t.type, a = t.pendingProps, a = t.elementType === i ? a : Es(i, a), uc(e, t), t.tag = 1, sa(i) ? (e = !0, da(t)) : e = !1, io(t, n), As(t, i, a), Ms(t, i, a, n), Qs(null, t, i, !0, e, n);
			case 19: return lc(e, t, n);
			case 22: return Js(e, t, n);
		}
		throw Error(r(156, t.tag));
	};
	function ql(e, t) {
		return wt(e, t);
	}
	function Jl(e, t, n, r) {
		this.tag = e, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
	}
	function Yl(e, t, n, r) {
		return new Jl(e, t, n, r);
	}
	function Xl(e) {
		return e = e.prototype, !(!e || !e.isReactComponent);
	}
	function Zl(e) {
		if (typeof e == "function") return +!!Xl(e);
		if (e != null) {
			if (e = e.$$typeof, e === ae) return 11;
			if (e === ce) return 14;
		}
		return 2;
	}
	function Ql(e, t) {
		var n = e.alternate;
		return n === null ? (n = Yl(e.tag, t, e.key, e.mode), n.elementType = e.elementType, n.type = e.type, n.stateNode = e.stateNode, n.alternate = e, e.alternate = n) : (n.pendingProps = t, n.type = e.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = e.flags & 14680064, n.childLanes = e.childLanes, n.lanes = e.lanes, n.child = e.child, n.memoizedProps = e.memoizedProps, n.memoizedState = e.memoizedState, n.updateQueue = e.updateQueue, t = e.dependencies, n.dependencies = t === null ? null : {
			lanes: t.lanes,
			firstContext: t.firstContext
		}, n.sibling = e.sibling, n.index = e.index, n.ref = e.ref, n;
	}
	function $l(e, t, n, i, a, o) {
		var s = 2;
		if (i = e, typeof e == "function") Xl(e) && (s = 1);
		else if (typeof e == "string") s = 5;
		else a: switch (e) {
			case S: return eu(n.children, a, o, t);
			case C:
				s = 8, a |= 8;
				break;
			case ne: return e = Yl(12, n, t, a | 2), e.elementType = ne, e.lanes = o, e;
			case oe: return e = Yl(13, n, t, a), e.elementType = oe, e.lanes = o, e;
			case se: return e = Yl(19, n, t, a), e.elementType = se, e.lanes = o, e;
			case w: return tu(n, a, o, t);
			default:
				if (typeof e == "object" && e) switch (e.$$typeof) {
					case re:
						s = 10;
						break a;
					case ie:
						s = 9;
						break a;
					case ae:
						s = 11;
						break a;
					case ce:
						s = 14;
						break a;
					case le:
						s = 16, i = null;
						break a;
				}
				throw Error(r(130, e == null ? e : typeof e, ""));
		}
		return t = Yl(s, n, t, a), t.elementType = e, t.type = i, t.lanes = o, t;
	}
	function eu(e, t, n, r) {
		return e = Yl(7, e, r, t), e.lanes = n, e;
	}
	function tu(e, t, n, r) {
		return e = Yl(22, e, r, t), e.elementType = w, e.lanes = n, e.stateNode = { isHidden: !1 }, e;
	}
	function nu(e, t, n) {
		return e = Yl(6, e, null, t), e.lanes = n, e;
	}
	function ru(e, t, n) {
		return t = Yl(4, e.children === null ? [] : e.children, e.key, t), t.lanes = n, t.stateNode = {
			containerInfo: e.containerInfo,
			pendingChildren: null,
			implementation: e.implementation
		}, t;
	}
	function iu(e, t, n, r, i) {
		this.tag = t, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = Jt(0), this.expirationTimes = Jt(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = Jt(0), this.identifierPrefix = r, this.onRecoverableError = i, this.mutableSourceEagerHydrationData = null;
	}
	function au(e, t, n, r, i, a, o, s, c) {
		return e = new iu(e, t, n, s, c), t === 1 ? (t = 1, !0 === a && (t |= 8)) : t = 0, a = Yl(3, null, null, t), e.current = a, a.stateNode = e, a.memoizedState = {
			element: r,
			isDehydrated: n,
			cache: null,
			transitions: null,
			pendingSuspenseBoundaries: null
		}, fo(a), e;
	}
	function ou(e, t, n) {
		var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
		return {
			$$typeof: te,
			key: r == null ? null : "" + r,
			children: e,
			containerInfo: t,
			implementation: n
		};
	}
	function su(e) {
		if (!e) return ra;
		e = e._reactInternals;
		a: {
			if (vt(e) !== e || e.tag !== 1) throw Error(r(170));
			var t = e;
			do {
				switch (t.tag) {
					case 3:
						t = t.stateNode.context;
						break a;
					case 1: if (sa(t.type)) {
						t = t.stateNode.__reactInternalMemoizedMergedChildContext;
						break a;
					}
				}
				t = t.return;
			} while (t !== null);
			throw Error(r(171));
		}
		if (e.tag === 1) {
			var n = e.type;
			if (sa(n)) return ua(e, n, t);
		}
		return t;
	}
	function cu(e, t, n, r, i, a, o, s, c) {
		return e = au(n, r, !0, e, i, a, o, s, c), e.context = su(null), n = e.current, r = gl(), i = _l(n), a = mo(r, i), a.callback = t ?? null, ho(n, a, i), e.current.lanes = i, Yt(e, i, r), yl(e, r), e;
	}
	function lu(e, t, n, r) {
		var i = t.current, a = gl(), o = _l(i);
		return n = su(n), t.context === null ? t.context = n : t.pendingContext = n, t = mo(a, o), t.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (t.callback = r), e = ho(i, t, o), e !== null && (vl(e, i, o, a), go(e, i, o)), o;
	}
	function uu(e) {
		if (e = e.current, !e.child) return null;
		switch (e.child.tag) {
			case 5: return e.child.stateNode;
			default: return e.child.stateNode;
		}
	}
	function du(e, t) {
		if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
			var n = e.retryLane;
			e.retryLane = n !== 0 && n < t ? n : t;
		}
	}
	function fu(e, t) {
		du(e, t), (e = e.alternate) && du(e, t);
	}
	function pu() {
		return null;
	}
	var mu = typeof reportError == "function" ? reportError : function(e) {
		console.error(e);
	};
	function hu(e) {
		this._internalRoot = e;
	}
	gu.prototype.render = hu.prototype.render = function(e) {
		var t = this._internalRoot;
		if (t === null) throw Error(r(409));
		lu(e, t, null, null);
	}, gu.prototype.unmount = hu.prototype.unmount = function() {
		var e = this._internalRoot;
		if (e !== null) {
			this._internalRoot = null;
			var t = e.containerInfo;
			Dl(function() {
				lu(null, e, null, null);
			}), t[Ki] = null;
		}
	};
	function gu(e) {
		this._internalRoot = e;
	}
	gu.prototype.unstable_scheduleHydration = function(e) {
		if (e) {
			var t = nn();
			e = {
				blockedOn: null,
				target: e,
				priority: t
			};
			for (var n = 0; n < fn.length && t !== 0 && t < fn[n].priority; n++);
			fn.splice(n, 0, e), n === 0 && _n(e);
		}
	};
	function _u(e) {
		return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
	}
	function vu(e) {
		return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
	}
	function yu() {}
	function bu(e, t, n, r, i) {
		if (i) {
			if (typeof r == "function") {
				var a = r;
				r = function() {
					var e = uu(o);
					a.call(e);
				};
			}
			var o = cu(t, r, e, 0, null, !1, !1, "", yu);
			return e._reactRootContainer = o, e[Ki] = o.current, bi(e.nodeType === 8 ? e.parentNode : e), Dl(), o;
		}
		for (; i = e.lastChild;) e.removeChild(i);
		if (typeof r == "function") {
			var s = r;
			r = function() {
				var e = uu(c);
				s.call(e);
			};
		}
		var c = au(e, 0, !1, null, null, !1, !1, "", yu);
		return e._reactRootContainer = c, e[Ki] = c.current, bi(e.nodeType === 8 ? e.parentNode : e), Dl(function() {
			lu(t, c, n, r);
		}), c;
	}
	function xu(e, t, n, r, i) {
		var a = n._reactRootContainer;
		if (a) {
			var o = a;
			if (typeof i == "function") {
				var s = i;
				i = function() {
					var e = uu(o);
					s.call(e);
				};
			}
			lu(t, o, e, i);
		} else o = bu(n, t, e, i, r);
		return uu(o);
	}
	$t = function(e) {
		switch (e.tag) {
			case 3:
				var t = e.stateNode;
				if (t.current.memoizedState.isDehydrated) {
					var n = Ht(t.pendingLanes);
					n !== 0 && (Zt(t, n | 1), yl(t, E()), !(W & 6) && (il = E() + 500, va()));
				}
				break;
			case 13: Dl(function() {
				var t = lo(e, 1);
				t !== null && vl(t, e, 1, gl());
			}), fu(e, 1);
		}
	}, en = function(e) {
		if (e.tag === 13) {
			var t = lo(e, 134217728);
			t !== null && vl(t, e, 134217728, gl()), fu(e, 134217728);
		}
	}, tn = function(e) {
		if (e.tag === 13) {
			var t = _l(e), n = lo(e, t);
			n !== null && vl(n, e, t, gl()), fu(e, t);
		}
	}, nn = function() {
		return k;
	}, rn = function(e, t) {
		var n = k;
		try {
			return k = e, t();
		} finally {
			k = n;
		}
	}, Ze = function(e, t, n) {
		switch (t) {
			case "input":
				if (Oe(e, n), t = n.name, n.type === "radio" && t != null) {
					for (n = e; n.parentNode;) n = n.parentNode;
					for (n = n.querySelectorAll("input[name=" + JSON.stringify("" + t) + "][type=\"radio\"]"), t = 0; t < n.length; t++) {
						var i = n[t];
						if (i !== e && i.form === e.form) {
							var a = $i(i);
							if (!a) throw Error(r(90));
							Ce(i), Oe(i, a);
						}
					}
				}
				break;
			case "textarea":
				Fe(e, n);
				break;
			case "select": t = n.value, t != null && Me(e, !!n.multiple, t, !1);
		}
	}, rt = El, it = Dl;
	var Su = {
		usingClientEntryPoint: !1,
		Events: [
			Zi,
			Qi,
			$i,
			tt,
			nt,
			El
		]
	}, Cu = {
		findFiberByHostInstance: Xi,
		bundleType: 0,
		version: "18.3.1",
		rendererPackageName: "react-dom"
	}, wu = {
		bundleType: Cu.bundleType,
		version: Cu.version,
		rendererPackageName: Cu.rendererPackageName,
		rendererConfig: Cu.rendererConfig,
		overrideHookState: null,
		overrideHookStateDeletePath: null,
		overrideHookStateRenamePath: null,
		overrideProps: null,
		overridePropsDeletePath: null,
		overridePropsRenamePath: null,
		setErrorHandler: null,
		setSuspenseHandler: null,
		scheduleUpdate: null,
		currentDispatcherRef: x.ReactCurrentDispatcher,
		findHostInstanceByFiber: function(e) {
			return e = St(e), e === null ? null : e.stateNode;
		},
		findFiberByHostInstance: Cu.findFiberByHostInstance || pu,
		findHostInstancesForRefresh: null,
		scheduleRefresh: null,
		scheduleRoot: null,
		setRefreshHandler: null,
		getCurrentFiber: null,
		reconcilerVersion: "18.3.1-next-f1338f8080-20240426"
	};
	if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
		var Tu = __REACT_DEVTOOLS_GLOBAL_HOOK__;
		if (!Tu.isDisabled && Tu.supportsFiber) try {
			Pt = Tu.inject(wu), Ft = Tu;
		} catch {}
	}
	e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Su, e.createPortal = function(e, t) {
		var n = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
		if (!_u(t)) throw Error(r(200));
		return ou(e, t, null, n);
	}, e.createRoot = function(e, t) {
		if (!_u(e)) throw Error(r(299));
		var n = !1, i = "", a = mu;
		return t != null && (!0 === t.unstable_strictMode && (n = !0), t.identifierPrefix !== void 0 && (i = t.identifierPrefix), t.onRecoverableError !== void 0 && (a = t.onRecoverableError)), t = au(e, 1, !1, null, null, n, !1, i, a), e[Ki] = t.current, bi(e.nodeType === 8 ? e.parentNode : e), new hu(t);
	}, e.findDOMNode = function(e) {
		if (e == null) return null;
		if (e.nodeType === 1) return e;
		var t = e._reactInternals;
		if (t === void 0) throw typeof e.render == "function" ? Error(r(188)) : (e = Object.keys(e).join(","), Error(r(268, e)));
		return e = St(t), e = e === null ? null : e.stateNode, e;
	}, e.flushSync = function(e) {
		return Dl(e);
	}, e.hydrate = function(e, t, n) {
		if (!vu(t)) throw Error(r(200));
		return xu(null, e, t, !0, n);
	}, e.hydrateRoot = function(e, t, n) {
		if (!_u(e)) throw Error(r(405));
		var i = n != null && n.hydratedSources || null, a = !1, o = "", s = mu;
		if (n != null && (!0 === n.unstable_strictMode && (a = !0), n.identifierPrefix !== void 0 && (o = n.identifierPrefix), n.onRecoverableError !== void 0 && (s = n.onRecoverableError)), t = cu(t, null, e, 1, n ?? null, a, !1, o, s), e[Ki] = t.current, bi(e), i) for (e = 0; e < i.length; e++) n = i[e], a = n._getVersion, a = a(n._source), t.mutableSourceEagerHydrationData == null ? t.mutableSourceEagerHydrationData = [n, a] : t.mutableSourceEagerHydrationData.push(n, a);
		return new gu(t);
	}, e.render = function(e, t, n) {
		if (!vu(t)) throw Error(r(200));
		return xu(null, e, t, !1, n);
	}, e.unmountComponentAtNode = function(e) {
		if (!vu(e)) throw Error(r(40));
		return e._reactRootContainer ? (Dl(function() {
			xu(null, null, e, !1, function() {
				e._reactRootContainer = null, e[Ki] = null;
			});
		}), !0) : !1;
	}, e.unstable_batchedUpdates = El, e.unstable_renderSubtreeIntoContainer = function(e, t, n, i) {
		if (!vu(n)) throw Error(r(200));
		if (e == null || e._reactInternals === void 0) throw Error(r(38));
		return xu(e, t, n, !1, i);
	}, e.version = "18.3.1-next-f1338f8080-20240426";
})), T0 = /* @__PURE__ */ s(((e, t) => {
	function n() {
		if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) try {
			__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(n);
		} catch (e) {
			console.error(e);
		}
	}
	n(), t.exports = w0();
})), E0 = (0, D.forwardRef)((e, t) => {
	let { alignText: n, className: r, fill: i, minimal: a, outlined: o, large: s, size: c = "medium", variant: l = "solid", vertical: u, ...d } = e, f = (0, $.default)(ge, {
		[x]: i,
		[ce]: u
	}, bt(n), Tt(c, { large: s }), Et(l, {
		minimal: a,
		outlined: o
	}), r);
	return (0, Q.jsx)("div", {
		...d,
		ref: t,
		className: f,
		children: e.children
	});
});
E0.displayName = `${O}.ButtonGroup`;
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/card/card.js
var D0 = (0, D.forwardRef)((e, t) => {
	let { className: n, elevation: r = f.ZERO, interactive: i = !1, selected: a, compact: o, ...s } = e;
	return (0, Q.jsx)("div", {
		className: (0, $.default)(n, be, xt(r), {
			[te]: i,
			[y]: o,
			[oe]: a
		}),
		ref: t,
		...s
	});
});
D0.displayName = `${O}.Card`;
//#endregion
//#region node_modules/react-dom/client.js
var O0 = /* @__PURE__ */ s(((e) => {
	var t = T0();
	e.createRoot = t.createRoot, e.hydrateRoot = t.hydrateRoot;
})), k0 = (0, D.forwardRef)((e, t) => {
	let { alignIndicator: n, children: r, className: i, indicatorChildren: a, inline: o, inputRef: s, label: c, labelElement: l, large: u, size: d = "medium", style: f, type: p, typeClassName: m, tagName: h = "label", ...g } = e;
	return (0, D.createElement)(h, {
		className: (0, $.default)(Me, m, {
			[b]: g.disabled,
			[ee]: o
		}, bt(n), Tt(d, { large: u }), i),
		ref: t,
		style: f
	}, (0, Q.jsx)("input", {
		className: Ne,
		...g,
		ref: s,
		type: p
	}), (0, Q.jsx)("span", {
		className: Pe,
		children: a
	}), c, l, r);
});
k0.displayName = `${O}.Control`;
var A0 = (0, D.forwardRef)((e, t) => {
	let { innerLabelChecked: n, innerLabel: r, ...i } = e, a = r || n ? [(0, Q.jsx)("div", {
		className: Fe,
		children: (0, Q.jsx)("div", {
			className: ze,
			children: n || r
		})
	}, "checked"), (0, Q.jsx)("div", {
		className: Fe,
		children: (0, Q.jsx)("div", {
			className: ze,
			children: r
		})
	}, "unchecked")] : null;
	return (0, Q.jsx)(k0, {
		...i,
		indicatorChildren: a,
		ref: t,
		type: "checkbox",
		typeClassName: Re
	});
});
A0.displayName = `${O}.Switch`;
var j0 = (0, D.forwardRef)((e, t) => (0, Q.jsx)(k0, {
	...e,
	ref: t,
	type: "radio",
	typeClassName: Le
}));
j0.displayName = `${O}.Radio`;
var M0 = (0, D.forwardRef)((e, t) => {
	let { defaultIndeterminate: n, indeterminate: r, onChange: i, ...a } = e, [o, s] = (0, D.useState)(r || n || !1), c = (0, D.useRef)(null), l = Xt(e.inputRef, c), u = (0, D.useCallback)((e) => {
		r === void 0 && s(e.target.indeterminate), i?.(e);
	}, [r, i]);
	return (0, D.useEffect)(() => {
		r !== void 0 && s(r);
	}, [r]), (0, D.useEffect)(() => {
		c.current != null && (c.current.indeterminate = o);
	}, [c, o]), (0, Q.jsx)(k0, {
		...a,
		inputRef: l,
		onChange: u,
		ref: t,
		type: "checkbox",
		typeClassName: Ie
	});
});
M0.displayName = `${O}.Checkbox`;
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/forms/asyncControllableInput.js
var N0 = class e extends Zt {
	static displayName = `${O}.AsyncControllableInput`;
	static COMPOSITION_END_DELAY = 10;
	state = {
		hasPendingUpdate: !1,
		isComposing: !1,
		nextValue: this.props.value,
		value: this.props.value
	};
	cancelPendingCompositionEnd = null;
	static getDerivedStateFromProps(e, t) {
		return t.isComposing || e.value === void 0 ? null : t.nextValue === t.value ? {
			hasPendingUpdate: !1,
			nextValue: e.value,
			value: e.value
		} : e.value === t.nextValue ? t.hasPendingUpdate ? {
			hasPendingUpdate: !1,
			value: e.value
		} : { value: t.nextValue } : e.value === t.value ? { hasPendingUpdate: !0 } : {
			hasPendingUpdate: !1,
			nextValue: e.value,
			value: e.value
		};
	}
	render() {
		let { isComposing: e, hasPendingUpdate: t, value: n, nextValue: r } = this.state, { inputRef: i, ...a } = this.props;
		return (0, Q.jsx)("input", {
			...a,
			ref: i,
			value: e || t ? r : n,
			onCompositionStart: this.handleCompositionStart,
			onCompositionEnd: this.handleCompositionEnd,
			onChange: this.handleChange
		});
	}
	handleCompositionStart = (e) => {
		this.cancelPendingCompositionEnd?.(), this.setState({ isComposing: !0 }), this.props.onCompositionStart?.(e);
	};
	handleCompositionEnd = (t) => {
		this.cancelPendingCompositionEnd = this.setTimeout(() => this.setState({ isComposing: !1 }), e.COMPOSITION_END_DELAY), this.props.onCompositionEnd?.(t);
	};
	handleChange = (e) => {
		let { value: t } = e.target;
		this.setState({ nextValue: t }), this.props.onChange?.(e);
	};
}, P0 = ["inputSize", "onValueChange"], F0 = class extends Zt {
	static displayName = `${O}.InputGroup`;
	state = {};
	leftElement = null;
	rightElement = null;
	refHandlers = {
		leftElement: (e) => this.leftElement = e,
		rightElement: (e) => this.rightElement = e
	};
	render() {
		let { asyncControl: e = !1, className: t, disabled: n, fill: r, inputClassName: i, inputRef: a, inputSize: o, intent: s, large: c, readOnly: l, round: u, size: d = "medium", small: f, tagName: p = "div" } = this.props, m = (0, $.default)(ke, Ct(s), {
			[b]: n,
			[ie]: l,
			[x]: r,
			[ae]: u
		}, Tt(d, {
			large: c,
			small: f
		}), t), h = {
			...this.props.style,
			paddingLeft: this.state.leftElementWidth,
			paddingRight: this.state.rightElementWidth
		}, g = {
			type: "text",
			...Rt(this.props, P0, !0),
			"aria-disabled": n,
			className: (0, $.default)(Oe, i),
			onChange: this.handleInputChange,
			size: o,
			style: h
		}, _ = e ? (0, Q.jsx)(N0, {
			...g,
			inputRef: a
		}) : (0, Q.jsx)("input", {
			...g,
			ref: a
		});
		return (0, D.createElement)(p, { className: m }, this.maybeRenderLeftElement(), _, this.maybeRenderRightElement());
	}
	componentDidMount() {
		this.updateInputWidth();
	}
	componentDidUpdate(e) {
		let { leftElement: t, rightElement: n } = this.props;
		(e.leftElement !== t || e.rightElement !== n) && this.updateInputWidth();
	}
	validateProps(e) {
		e.leftElement != null && e.leftIcon != null && console.warn(Mt);
	}
	handleInputChange = (e) => {
		let t = e.target.value;
		this.props.onChange?.(e), this.props.onValueChange?.(t, e.target);
	};
	maybeRenderLeftElement() {
		let { leftElement: e, leftIcon: t } = this.props;
		if (e != null) return (0, Q.jsx)("span", {
			className: Ae,
			ref: this.refHandlers.leftElement,
			children: e
		});
		if (t != null) return (0, Q.jsx)(r0, {
			icon: t,
			"aria-hidden": !0,
			tabIndex: -1
		});
	}
	maybeRenderRightElement() {
		let { rightElement: e } = this.props;
		if (e != null) return (0, Q.jsx)("span", {
			className: je,
			ref: this.refHandlers.rightElement,
			children: e
		});
	}
	updateInputWidth() {
		let { leftElementWidth: e, rightElementWidth: t } = this.state;
		if (this.leftElement != null) {
			let { clientWidth: t } = this.leftElement;
			(e === void 0 || Math.abs(t - e) > 2) && this.setState({ leftElementWidth: t });
		} else this.setState({ leftElementWidth: void 0 });
		if (this.rightElement != null) {
			let { clientWidth: e } = this.rightElement;
			(t === void 0 || Math.abs(e - t) > 2) && this.setState({ rightElementWidth: e });
		} else this.setState({ rightElementWidth: void 0 });
	}
}, I0;
(function(e) {
	e[e.STANDARD = 48] = "STANDARD", e[e.SMALL = 32] = "SMALL", e[e.EXTRA_SMALL = 20] = "EXTRA_SMALL";
})(I0 ||= {});
var L0 = (e) => {
	let { action: t, children: n, className: r, description: i, icon: a, iconMuted: o = !0, iconSize: s = I0.STANDARD, layout: c = "vertical", title: l } = e;
	return (0, Q.jsxs)("div", {
		className: (0, $.default)(Ye, `${Ye}-${c}`, r),
		children: [
			a == null ? void 0 : (0, Q.jsx)("div", {
				className: Xe,
				style: {
					fontSize: `${s}px`,
					lineHeight: `${s}px`
				},
				children: (0, Q.jsx)(r0, {
					className: (0, $.default)({ [yt]: o }),
					icon: a,
					size: s,
					"aria-hidden": !0,
					tabIndex: -1
				})
			}),
			l == null && i == null ? void 0 : (0, Q.jsxs)("div", {
				className: Ze,
				children: [l && (0, Q.jsx)(x0, { children: l }), i && Bt(i, "div")]
			}),
			t,
			n
		]
	});
};
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/tag/tagRemoveButton.js
L0.displayName = `${O}.NonIdealState`, A1();
var R0 = (e) => {
	let { className: t, large: n, onRemove: r, size: i, tabIndex: a } = e, o = n || i === "large" || t?.includes(S), s = (0, D.useCallback)((t) => {
		r?.(t, e);
	}, [r, e]);
	return (0, Q.jsx)("button", {
		"aria-label": "Remove tag",
		type: "button",
		className: ut,
		onClick: s,
		tabIndex: a,
		children: (0, Q.jsx)(n0, { size: o ? X.LARGE : X.STANDARD })
	});
};
R0.displayName = `${O}.TagRemoveButton`;
//#endregion
//#region node_modules/@blueprintjs/core/lib/esm/components/tag/tag.js
var z0 = (0, D.forwardRef)((e, t) => {
	let { children: n, className: r, endIcon: i, fill: a = !1, icon: o, intent: s, interactive: c, large: l = !1, minimal: u = !1, multiline: d, onRemove: f, rightIcon: p, round: m = !1, size: h = "medium", tabIndex: _ = 0, htmlTitle: v, ...y } = e, b = kt(f), ee = c ?? y.onClick != null, [S, C] = nn(ee, e, t, {
		defaultTabIndex: 0,
		disabledTabIndex: void 0
	}), re = (0, $.default)(lt, Ct(s), Tt(h, { large: l }), {
		[g]: S,
		[x]: a,
		[te]: ee,
		[ne]: u,
		[ae]: m
	}, r);
	return (0, Q.jsxs)("span", {
		...Rt(y),
		...C,
		className: re,
		role: ee ? "button" : void 0,
		children: [
			(0, Q.jsx)(r0, { icon: o }),
			!zt(n) && (0, Q.jsx)(h0, {
				className: x,
				ellipsize: !d,
				tagName: "span",
				title: v,
				children: n
			}),
			(0, Q.jsx)(r0, { icon: i ?? p }),
			b && (0, Q.jsx)(R0, { ...e })
		]
	});
});
z0.displayName = `${O}.Tag`;
//#endregion
//#region src/contracts.ts
var B0 = O0(), V0 = /^[a-f0-9]{64}$/, H0 = /^[a-f0-9]{32}$/;
function U0(e, t) {
	if (!G0(e)) throw Error("Foldweave returned an invalid preview object.");
	if (e.schema_version !== "folder-plan-preview.v1" || e.job_id !== t || !K0(e.job_id, H0) || !K0(e.source_commitment, V0) || !K0(e.compiled_candidate_fingerprint, V0) || !K0(e.preview_fingerprint, V0) || !Number.isInteger(e.expected_job_revision) || !Number.isInteger(e.proposal_revision) || !Array.isArray(e.current_tree_members) || !Array.isArray(e.proposed_tree_members) || !Array.isArray(e.member_changes) || !Array.isArray(e.supported_link_effects) || !G0(e.counts)) throw Error("Foldweave returned an incomplete preview contract.");
}
function W0(e, t) {
	if (!G0(e)) throw Error("Foldweave returned an invalid review status.");
	if (e.job_id !== t || !K0(e.job_id, H0) || e.lifecycle !== "reviewing" || !Number.isInteger(e.job_revision) || !Number.isInteger(e.proposal_revision) || !K0(e.candidate_fingerprint, V0) || !K0(e.preview_fingerprint, V0) || typeof e.output_parent != "string" || e.output_parent.length === 0 || typeof e.result_folder_name != "string" || e.result_folder_name.length === 0 || typeof e.revision_available != "boolean" || typeof e.revision_attempts_remaining != "number" || !Number.isInteger(e.revision_attempts_remaining) || e.revision_attempts_remaining < 0 || e.revision_attempts_remaining > 2 || e.revision_failure !== null && typeof e.revision_failure != "string") throw Error("Foldweave returned an incomplete review status.");
}
function G0(e) {
	return typeof e == "object" && !!e && !Array.isArray(e);
}
function K0(e, t) {
	return typeof e == "string" && t.test(e);
}
//#endregion
//#region src/review-island.tsx
var q0 = [
	{
		key: "moved",
		label: "Moved"
	},
	{
		key: "renamed",
		label: "Renamed"
	},
	{
		key: "link_updated",
		label: "Link updated"
	},
	{
		key: "protected",
		label: "Protected"
	},
	{
		key: "unchanged",
		label: "Unchanged"
	},
	{
		key: "empty_directory",
		label: "Empty directory"
	}
], J0 = {
	unchanged: "Unchanged",
	renamed: "Renamed",
	moved: "Moved",
	moved_and_renamed: "Moved + renamed",
	protected: "Protected",
	empty_directory: "Empty directory"
};
function Y0({ preview: e, status: t, journey: n, acceptPlan: r, revisePlan: i, keepPrevious: a, idempotencyKeyFactory: o = l2 }) {
	let [s, c] = (0, D.useState)("proposed"), [l, u] = (0, D.useState)(!0), [d, f] = (0, D.useState)(/* @__PURE__ */ new Set()), [p, m] = (0, D.useState)(""), [h, g] = (0, D.useState)(e.member_changes.find(a2)?.member_id ?? e.member_changes[0]?.member_id ?? null), [_, v] = (0, D.useState)(() => r2(e)), [y, b] = (0, D.useState)(""), [x, ee] = (0, D.useState)(!1), [te, S] = (0, D.useState)(null), [C, ne] = (0, D.useState)(!1), [re, ie] = (0, D.useState)(null), [ae, oe] = (0, D.useState)(null), se = (0, D.useRef)(e), ce = (0, D.useRef)(null), le = (0, D.useRef)(null), w = (0, D.useRef)(null), ue = (0, D.useRef)(null), de = (0, D.useRef)([]), T = (0, D.useMemo)(() => new Map(e.member_changes.map((e) => [e.member_id, e])), [e.member_changes]), fe = s === "current" ? e.current_tree_members : e.proposed_tree_members, pe = (0, D.useMemo)(() => fe.filter((e) => {
		let t = T.get(e.member_id);
		if (!t) return !1;
		let n = p.trim().toLocaleLowerCase();
		return n.length === 0 || t.current_relative_path.toLocaleLowerCase().includes(n) || t.proposed_relative_path.toLocaleLowerCase().includes(n) ? d.size > 0 ? [...d].some((e) => i2(t, e)) : !l || a2(t) : !1;
	}), [
		d,
		T,
		l,
		fe,
		p
	]), me = (0, D.useMemo)(() => e2(pe), [pe]), he = (0, D.useMemo)(() => n2(me, _), [_, me]), ge = h === null ? void 0 : T.get(h), _e = (0, D.useMemo)(() => ge === void 0 ? [] : e.supported_link_effects.filter((e) => e.source_member_id === ge.member_id || e.target_member_id === ge.member_id), [e.supported_link_effects, ge]);
	(0, D.useEffect)(() => {
		h !== null && pe.some((e) => e.member_id === h) || g(pe[0]?.member_id ?? null);
	}, [h, pe]), (0, D.useEffect)(() => {
		let t = se.current;
		if (t.preview_fingerprint === e.preview_fingerprint) return;
		let n = new Map(t.member_changes.map((e) => [e.member_id, e.proposed_relative_path])), r = e.member_changes.filter((e) => n.get(e.member_id) !== e.proposed_relative_path).length;
		oe(`${r} ${r === 1 ? "mapping" : "mappings"} changed from the previous proposal.`), se.current = e;
	}, [e]);
	let ve = (e) => {
		u(!1), f((t) => {
			let n = new Set(t);
			return n.has(e) ? n.delete(e) : n.add(e), n;
		});
	}, ye = (e, t, n) => {
		if (e.key === "ArrowDown" || e.key === "ArrowUp") {
			e.preventDefault();
			let n = e.key === "ArrowDown" ? t + 1 : t - 1;
			de.current[n]?.focus();
			return;
		}
		n.kind === "directory" && e.key === "ArrowRight" && (e.preventDefault(), v((e) => new Set(e).add(n.path))), n.kind === "directory" && e.key === "ArrowLeft" && (e.preventDefault(), v((e) => {
			let t = new Set(e);
			return t.delete(n.path), t;
		}));
	}, be = async () => {
		if (x || C || t.revision_failure !== null || e.counts.blocker_count > 0) return;
		ee(!0), S(null);
		let n = JSON.stringify([
			e.expected_job_revision,
			e.compiled_candidate_fingerprint,
			e.preview_fingerprint,
			t.output_parent,
			t.result_folder_name
		]), i = X0(ce, n, o);
		try {
			await r({
				candidate_fingerprint: e.compiled_candidate_fingerprint,
				expected_revision: e.expected_job_revision,
				idempotency_key: i,
				output_parent: t.output_parent,
				preview_fingerprint: e.preview_fingerprint,
				result_folder_name: t.result_folder_name
			}), ce.current = null;
		} catch (e) {
			S(e instanceof Error ? e.message : "Acceptance was blocked."), ee(!1);
		}
	}, xe = async () => {
		let n = y.trim();
		if (C || x || !t.revision_available || n.length === 0) return;
		ne(!0), ie(null);
		let r = JSON.stringify([
			e.expected_job_revision,
			e.compiled_candidate_fingerprint,
			e.preview_fingerprint,
			n
		]), a = X0(le, r, o);
		try {
			await i({
				candidate_fingerprint: e.compiled_candidate_fingerprint,
				expected_revision: e.expected_job_revision,
				idempotency_key: a,
				instruction: n,
				preview_fingerprint: e.preview_fingerprint
			}), le.current = null, b("");
		} catch (e) {
			ie(e instanceof Error ? e.message : "Revision was blocked.");
		} finally {
			ne(!1);
		}
	}, Se = async () => {
		if (C || t.revision_failure === null) return;
		ne(!0), ie(null);
		let n = JSON.stringify([
			e.expected_job_revision,
			e.compiled_candidate_fingerprint,
			e.preview_fingerprint
		]), r = X0(w, n, o);
		try {
			await a({
				candidate_fingerprint: e.compiled_candidate_fingerprint,
				expected_revision: e.expected_job_revision,
				idempotency_key: r,
				preview_fingerprint: e.preview_fingerprint
			}), w.current = null;
		} catch (e) {
			ie(e instanceof Error ? e.message : "The prior proposal could not be kept.");
		} finally {
			ne(!1);
		}
	}, Ce = n === "apply" ? "Your current folder" : "Original structure", we = n === "apply" ? "Shared proposal" : "Proposed structure";
	return /* @__PURE__ */ (0, Q.jsxs)("div", {
		className: "fw-review bp6-dark",
		children: [
			/* @__PURE__ */ (0, Q.jsxs)("section", {
				className: "fw-trust-strip",
				"aria-label": "Plan trust summary",
				children: [
					/* @__PURE__ */ (0, Q.jsx)(Z0, {
						icon: "lock",
						label: "Source unchanged",
						value: "No output yet"
					}),
					/* @__PURE__ */ (0, Q.jsx)(Z0, {
						icon: "tick-circle",
						label: "Complete accounting",
						value: `${e.counts.file_count} files`
					}),
					/* @__PURE__ */ (0, Q.jsx)(Z0, {
						icon: "shield",
						label: "Protected",
						value: `${e.counts.protected_count} fixed`
					}),
					/* @__PURE__ */ (0, Q.jsx)(Z0, {
						icon: "link",
						label: "Supported links",
						value: `${e.counts.link_updated_count} updates`
					}),
					/* @__PURE__ */ (0, Q.jsx)(Z0, {
						icon: "folder-new",
						label: "Output",
						value: "Created only after accept"
					})
				]
			}),
			/* @__PURE__ */ (0, Q.jsxs)("div", {
				className: "fw-toolbar",
				children: [
					/* @__PURE__ */ (0, Q.jsxs)(E0, {
						"aria-label": "Structure view",
						children: [/* @__PURE__ */ (0, Q.jsx)(g0, {
							"aria-pressed": s === "current",
							intent: s === "current" ? "primary" : "none",
							onClick: () => c("current"),
							children: Ce
						}), /* @__PURE__ */ (0, Q.jsx)(g0, {
							"aria-pressed": s === "proposed",
							intent: s === "proposed" ? "primary" : "none",
							onClick: () => c("proposed"),
							children: we
						})]
					}),
					/* @__PURE__ */ (0, Q.jsx)("div", { className: "fw-toolbar-spacer" }),
					/* @__PURE__ */ (0, Q.jsx)(F0, {
						"aria-label": "Search current and proposed paths",
						leftIcon: "search",
						onChange: (e) => m(e.currentTarget.value),
						placeholder: "Search paths",
						value: p
					}),
					/* @__PURE__ */ (0, Q.jsx)(M0, {
						checked: l,
						label: "Changed only",
						onChange: (e) => {
							u(e.currentTarget.checked), e.currentTarget.checked && f(/* @__PURE__ */ new Set());
						}
					})
				]
			}),
			/* @__PURE__ */ (0, Q.jsx)("div", {
				className: "fw-filter-row",
				role: "group",
				"aria-label": "Member filters",
				children: q0.map(({ key: e, label: t }) => /* @__PURE__ */ (0, Q.jsx)(M0, {
					checked: d.has(e),
					inline: !0,
					label: t,
					onChange: () => ve(e)
				}, e))
			}),
			/* @__PURE__ */ (0, Q.jsxs)("div", {
				className: "fw-main-grid",
				children: [/* @__PURE__ */ (0, Q.jsxs)(D0, {
					className: "fw-tree-panel",
					compact: !0,
					children: [/* @__PURE__ */ (0, Q.jsxs)("header", {
						className: "fw-panel-heading",
						children: [/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("span", {
							className: "fw-eyebrow",
							children: s === "current" ? "CURRENT" : "PROPOSED"
						}), /* @__PURE__ */ (0, Q.jsx)("h2", { children: s === "current" ? Ce : we })] }), /* @__PURE__ */ (0, Q.jsxs)(z0, {
							minimal: !0,
							children: [pe.length, " shown"]
						})]
					}), /* @__PURE__ */ (0, Q.jsx)("div", {
						className: "fw-tree",
						role: "tree",
						"aria-label": `${s === "current" ? Ce : we} folder tree`,
						children: he.length === 0 ? /* @__PURE__ */ (0, Q.jsx)("div", {
							className: "fw-empty-state",
							children: "No members match these filters."
						}) : he.map((e, t) => {
							let n = e.memberId === null ? void 0 : T.get(e.memberId), r = e.kind === "directory", i = _.has(e.path);
							return /* @__PURE__ */ (0, Q.jsxs)("button", {
								"aria-label": $0(e, n),
								"aria-expanded": r ? i : void 0,
								"aria-level": e.depth + 1,
								"aria-selected": e.memberId !== null && h === e.memberId,
								className: `fw-tree-row ${e.memberId !== null && h === e.memberId ? "is-selected" : ""}`,
								onClick: () => {
									r && v((t) => c2(t, e.path)), e.memberId !== null && g(e.memberId);
								},
								onKeyDown: (n) => ye(n, t, e),
								ref: (e) => {
									de.current[t] = e;
								},
								role: "treeitem",
								style: { "--fw-depth": e.depth },
								type: "button",
								children: [
									/* @__PURE__ */ (0, Q.jsx)("span", {
										className: "fw-disclosure",
										"aria-hidden": "true",
										children: r ? i ? "⌄" : "›" : ""
									}),
									/* @__PURE__ */ (0, Q.jsx)(r0, {
										icon: r ? "folder-close" : "document",
										"aria-hidden": "true"
									}),
									/* @__PURE__ */ (0, Q.jsx)("span", {
										className: "fw-tree-label",
										children: e.label
									}),
									n && /* @__PURE__ */ (0, Q.jsx)(Q0, { change: n })
								]
							}, e.key);
						})
					})]
				}), /* @__PURE__ */ (0, Q.jsx)(D0, {
					className: "fw-detail-panel",
					compact: !0,
					children: ge ? /* @__PURE__ */ (0, Q.jsxs)(Q.Fragment, { children: [
						/* @__PURE__ */ (0, Q.jsxs)("div", {
							className: "fw-detail-heading",
							children: [/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("span", {
								className: "fw-eyebrow",
								children: "SELECTED MEMBER"
							}), /* @__PURE__ */ (0, Q.jsx)("h2", { children: s === "current" ? ge.current_relative_path : ge.proposed_relative_path })] }), /* @__PURE__ */ (0, Q.jsx)(z0, {
								intent: s2(ge),
								children: J0[ge.change_classification]
							})]
						}),
						/* @__PURE__ */ (0, Q.jsxs)("dl", {
							className: "fw-details",
							children: [
								/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("dt", { children: "Current" }), /* @__PURE__ */ (0, Q.jsx)("dd", { children: ge.current_relative_path })] }),
								/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("dt", { children: "Proposed" }), /* @__PURE__ */ (0, Q.jsx)("dd", { children: ge.proposed_relative_path })] }),
								/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("dt", { children: "Authority" }), /* @__PURE__ */ (0, Q.jsx)("dd", { children: o2(ge) })] }),
								/* @__PURE__ */ (0, Q.jsxs)("div", { children: [/* @__PURE__ */ (0, Q.jsx)("dt", { children: "Reason" }), /* @__PURE__ */ (0, Q.jsx)("dd", { children: ge.rationale })] })
							]
						}),
						/* @__PURE__ */ (0, Q.jsxs)("section", {
							className: "fw-link-section",
							"aria-labelledby": "link-effects-title",
							children: [/* @__PURE__ */ (0, Q.jsx)("h3", {
								id: "link-effects-title",
								children: "Supported link effects"
							}), _e.length === 0 ? /* @__PURE__ */ (0, Q.jsx)("p", { children: "No supported links originate from this member." }) : /* @__PURE__ */ (0, Q.jsx)("ul", { children: _e.map((e) => /* @__PURE__ */ (0, Q.jsxs)("li", { children: [
								/* @__PURE__ */ (0, Q.jsx)(z0, {
									intent: e.status === "rewritten" ? "warning" : "success",
									minimal: !0,
									children: e.status === "rewritten" ? "Rewritten" : "Still valid"
								}),
								/* @__PURE__ */ (0, Q.jsx)("code", { children: e.original_destination }),
								/* @__PURE__ */ (0, Q.jsx)("span", {
									"aria-hidden": "true",
									children: "→"
								}),
								/* @__PURE__ */ (0, Q.jsx)("code", { children: e.proposed_destination })
							] }, e.reference_id)) })]
						})
					] }) : /* @__PURE__ */ (0, Q.jsx)("div", {
						className: "fw-empty-state",
						children: "Select a member to inspect its exact change."
					})
				})]
			}),
			/* @__PURE__ */ (0, Q.jsxs)("section", {
				className: "fw-decision-panel",
				"aria-labelledby": "decision-title",
				children: [
					/* @__PURE__ */ (0, Q.jsxs)("div", {
						className: "fw-accept-row",
						children: [/* @__PURE__ */ (0, Q.jsxs)("div", { children: [
							/* @__PURE__ */ (0, Q.jsx)("span", {
								className: "fw-eyebrow",
								children: "EXACT AUTHORIZATION"
							}),
							/* @__PURE__ */ (0, Q.jsx)("h2", {
								id: "decision-title",
								children: "Create a separate, verified copy"
							}),
							/* @__PURE__ */ (0, Q.jsx)("p", { children: "The source stays unchanged. Acceptance is bound to this exact preview." })
						] }), /* @__PURE__ */ (0, Q.jsx)(g0, {
							className: "fw-accept-button",
							disabled: e.counts.blocker_count > 0 || x || C || t.revision_failure !== null,
							intent: "success",
							loading: x,
							onClick: () => void be(),
							rightIcon: "arrow-right",
							children: "Accept this structure and create copy"
						})]
					}),
					te && /* @__PURE__ */ (0, Q.jsx)("div", {
						className: "fw-error",
						role: "alert",
						children: te
					}),
					ae && /* @__PURE__ */ (0, Q.jsx)("div", {
						className: "fw-revision-delta",
						role: "status",
						children: ae
					}),
					t.revision_failure && /* @__PURE__ */ (0, Q.jsxs)("div", {
						className: "fw-error",
						role: "alert",
						children: [
							/* @__PURE__ */ (0, Q.jsx)("strong", { children: "The replacement proposal did not pass Foldweave checks." }),
							/* @__PURE__ */ (0, Q.jsx)("span", { children: t.revision_failure }),
							/* @__PURE__ */ (0, Q.jsxs)("div", {
								className: "fw-revision-actions",
								children: [/* @__PURE__ */ (0, Q.jsx)(g0, {
									disabled: !t.revision_available || C,
									onClick: () => ue.current?.focus(),
									children: "Try another change"
								}), /* @__PURE__ */ (0, Q.jsx)(g0, {
									disabled: C,
									onClick: () => void Se(),
									children: "Keep previous proposal"
								})]
							})
						]
					}),
					re && /* @__PURE__ */ (0, Q.jsx)("div", {
						className: "fw-error",
						role: "alert",
						children: re
					}),
					/* @__PURE__ */ (0, Q.jsx)("div", { className: "fw-revision-divider" }),
					/* @__PURE__ */ (0, Q.jsx)("label", {
						className: "fw-revision-label",
						htmlFor: "foldweave-revision",
						children: "Describe a change to this proposal"
					}),
					/* @__PURE__ */ (0, Q.jsx)("textarea", {
						id: "foldweave-revision",
						onChange: (e) => b(e.currentTarget.value),
						placeholder: "For example: keep the meeting notes together, and move the final brief into Delivery.",
						ref: ue,
						rows: 3,
						value: y
					}),
					/* @__PURE__ */ (0, Q.jsxs)("div", {
						className: "fw-revision-footer",
						children: [/* @__PURE__ */ (0, Q.jsx)("span", { children: t.revision_available ? `${t.revision_attempts_remaining} revision ${t.revision_attempts_remaining === 1 ? "attempt" : "attempts"} remaining.` : "Start a new job to request another revision." }), /* @__PURE__ */ (0, Q.jsx)(g0, {
							disabled: !t.revision_available || y.trim().length === 0 || C || x,
							intent: "primary",
							loading: C,
							onClick: () => void xe(),
							rightIcon: "send-message",
							children: "Send changes"
						})]
					})
				]
			})
		]
	});
}
function X0(e, t, n) {
	if (e.current?.requestFingerprint === t) return e.current.idempotencyKey;
	let r = n();
	return e.current = {
		requestFingerprint: t,
		idempotencyKey: r
	}, r;
}
function Z0({ icon: e, label: t, value: n }) {
	return /* @__PURE__ */ (0, Q.jsxs)("div", {
		className: "fw-trust-item",
		children: [/* @__PURE__ */ (0, Q.jsx)(r0, {
			icon: e,
			"aria-hidden": "true"
		}), /* @__PURE__ */ (0, Q.jsxs)("span", { children: [/* @__PURE__ */ (0, Q.jsx)("strong", { children: t }), /* @__PURE__ */ (0, Q.jsx)("small", { children: n })] })]
	});
}
function Q0({ change: e }) {
	return /* @__PURE__ */ (0, Q.jsxs)("span", {
		className: "fw-status-signals",
		children: [
			e.protected && /* @__PURE__ */ (0, Q.jsx)("span", {
				className: "fw-signal is-protected",
				children: "Protected"
			}),
			e.link_updated && /* @__PURE__ */ (0, Q.jsx)("span", {
				className: "fw-signal is-link",
				children: "Link"
			}),
			!e.protected && e.change_classification !== "unchanged" && /* @__PURE__ */ (0, Q.jsx)("span", {
				className: `fw-signal is-${e.change_classification}`,
				children: J0[e.change_classification]
			}),
			e.change_classification === "unchanged" && /* @__PURE__ */ (0, Q.jsx)("span", {
				className: "fw-signal is-unchanged",
				children: "Unchanged"
			})
		]
	});
}
function $0(e, t) {
	if (!t) return e.label;
	let n = [J0[t.change_classification]];
	return t.link_updated && n.push("supported link updated"), `${e.label}, ${n.join(", ")}`;
}
function e2(e) {
	let t = {
		key: "root",
		label: "",
		path: "",
		depth: -1,
		kind: "directory",
		memberId: null,
		explicitEmptyDirectory: !1,
		children: []
	}, n = /* @__PURE__ */ new Map([["", t]]);
	for (let r of e) {
		let e = r.relative_path.split("/"), i = r.member_kind === "empty_directory" ? e.length : e.length - 1, a = t;
		for (let t = 0; t < i; t += 1) {
			let i = e.slice(0, t + 1).join("/"), o = n.get(i);
			o || (o = {
				key: `directory:${i}`,
				label: e[t],
				path: i,
				depth: t,
				kind: "directory",
				memberId: null,
				explicitEmptyDirectory: !1,
				children: []
			}, n.set(i, o), a.children.push(o)), r.member_kind === "empty_directory" && t === e.length - 1 && (o.memberId = r.member_id, o.explicitEmptyDirectory = !0), a = o;
		}
		r.member_kind === "regular_file" && a.children.push({
			key: `file:${r.member_id}`,
			label: e.at(-1) ?? r.relative_path,
			path: r.relative_path,
			depth: e.length - 1,
			kind: "file",
			memberId: r.member_id,
			explicitEmptyDirectory: !1,
			children: []
		});
	}
	return t2(t), t.children;
}
function t2(e) {
	e.children.sort((e, t) => e.kind === t.kind ? e.label.localeCompare(t.label) : e.kind === "directory" ? -1 : 1), e.children.forEach(t2);
}
function n2(e, t) {
	let n = [];
	for (let r of e) n.push(r), r.kind === "directory" && t.has(r.path) && n.push(...n2(r.children, t));
	return n;
}
function r2(e) {
	let t = /* @__PURE__ */ new Set();
	for (let n of e.member_changes.filter(a2)) for (let e of [n.current_relative_path, n.proposed_relative_path]) {
		let r = e.split("/"), i = n.member_kind === "empty_directory" ? r.length : r.length - 1;
		for (let e = 1; e <= i; e += 1) t.add(r.slice(0, e).join("/"));
	}
	return t;
}
function i2(e, t) {
	switch (t) {
		case "moved": return e.change_classification === "moved" || e.change_classification === "moved_and_renamed";
		case "renamed": return e.change_classification === "renamed" || e.change_classification === "moved_and_renamed";
		case "link_updated": return e.link_updated;
		case "protected": return e.protected;
		case "unchanged": return e.change_classification === "unchanged";
		case "empty_directory": return e.member_kind === "empty_directory";
	}
}
function a2(e) {
	return e.current_relative_path !== e.proposed_relative_path || e.link_updated;
}
function o2(e) {
	return e.authority_source === "change_file" ? "Imported Foldweave Change File" : e.authority_source === "gpt_plan" ? "Planning proposal, checked by deterministic code" : "Protected by deterministic policy";
}
function s2(e) {
	return e.protected || e.change_classification === "unchanged" ? "none" : e.link_updated ? "warning" : "primary";
}
function c2(e, t) {
	let n = new Set(e);
	return n.has(t) ? n.delete(t) : n.add(t), n;
}
function l2() {
	if (typeof crypto.randomUUID == "function") return crypto.randomUUID();
	let e = crypto.getRandomValues(/* @__PURE__ */ new Uint8Array(16));
	return Array.from(e, (e) => e.toString(16).padStart(2, "0")).join("");
}
function u2() {
	return /* @__PURE__ */ (0, Q.jsxs)("div", {
		className: "fw-loading",
		children: [/* @__PURE__ */ (0, Q.jsx)(d0, { size: 24 }), /* @__PURE__ */ (0, Q.jsx)("span", { children: "Loading the verified preview…" })]
	});
}
//#endregion
//#region src/main.tsx
function d2({ bootstrap: e }) {
	let [t, n] = (0, D.useState)(null), [r, i] = (0, D.useState)(null), [a, o] = (0, D.useState)(null);
	if ((0, D.useEffect)(() => {
		let t = new AbortController();
		return Promise.all([f2(`/api/jobs/${encodeURIComponent(e.jobId)}/preview`, t.signal), f2(`/api/jobs/${encodeURIComponent(e.jobId)}/status`, t.signal)]).then(([t, r]) => {
			if (U0(t, e.jobId), W0(r, e.jobId), t.expected_job_revision !== r.job_revision || t.compiled_candidate_fingerprint !== r.candidate_fingerprint || t.preview_fingerprint !== r.preview_fingerprint) throw Error("The visible preview no longer matches the durable job.");
			n(t), i(r);
		}).catch((e) => {
			t.signal.aborted || o(e instanceof Error ? e.message : "The preview could not be loaded.");
		}), () => t.abort();
	}, [e.jobId]), a) return /* @__PURE__ */ (0, Q.jsx)(L0, {
		icon: "error",
		title: "Review unavailable",
		description: a
	});
	if (!t || !r) return /* @__PURE__ */ (0, Q.jsx)(u2, {});
	let s = async (t) => {
		let n = await fetch(`/api/jobs/${encodeURIComponent(e.jobId)}/accept`, {
			method: "POST",
			credentials: "same-origin",
			headers: {
				"content-type": "application/json",
				"x-foldweave-csrf": e.csrfToken
			},
			body: JSON.stringify(t)
		}), r = await n.json();
		if (!n.ok) throw Error(p2(r));
		if (!m2(r) || r.lifecycle !== "verified" || typeof r.done_url != "string") throw Error("Foldweave did not return a verified result destination.");
		window.location.assign(r.done_url);
	}, c = async (e) => {
		await u("revision", e);
	}, l = async (e) => {
		await u("keep-proposal", e);
	}, u = async (t, r) => {
		let a = await fetch(`/api/jobs/${encodeURIComponent(e.jobId)}/${t}`, {
			method: "POST",
			credentials: "same-origin",
			headers: {
				"content-type": "application/json",
				"x-foldweave-csrf": e.csrfToken
			},
			body: JSON.stringify(r)
		}), o = await a.json();
		if (!a.ok) throw Error(p2(o));
		W0(o, e.jobId);
		let s = await f2(`/api/jobs/${encodeURIComponent(e.jobId)}/preview`, new AbortController().signal);
		if (U0(s, e.jobId), s.expected_job_revision !== o.job_revision || s.compiled_candidate_fingerprint !== o.candidate_fingerprint || s.preview_fingerprint !== o.preview_fingerprint) throw Error("The revised preview no longer matches the durable job.");
		n(s), i(o);
	};
	return /* @__PURE__ */ (0, Q.jsx)(Y0, {
		acceptPlan: s,
		journey: e.journey,
		keepPrevious: l,
		preview: t,
		revisePlan: c,
		status: r
	});
}
async function f2(e, t) {
	let n = await fetch(e, {
		credentials: "same-origin",
		headers: { accept: "application/json" },
		signal: t
	}), r = await n.json();
	if (!n.ok) throw Error(p2(r));
	return r;
}
function p2(e) {
	return m2(e) && typeof e.detail == "string" && e.detail.length > 0 ? e.detail : "Foldweave could not complete this request.";
}
function m2(e) {
	return typeof e == "object" && !!e && !Array.isArray(e);
}
function h2(e) {
	let { jobId: t, csrfToken: n, journey: r } = e.dataset;
	if (!t || !/^[a-f0-9]{32}$/.test(t)) throw Error("The review mount is missing its job identity.");
	if (!n || n.length < 16) throw Error("The review mount is missing its local authorization token.");
	if (r !== "organize" && r !== "apply") throw Error("The review mount has an unsupported journey.");
	return {
		jobId: t,
		csrfToken: n,
		journey: r
	};
}
var g2 = document.getElementById("foldweave-review-root");
if (g2) try {
	let e = h2(g2);
	(0, B0.createRoot)(g2).render(/* @__PURE__ */ (0, Q.jsx)(D.StrictMode, { children: /* @__PURE__ */ (0, Q.jsx)(d2, { bootstrap: e }) }));
} catch (e) {
	g2.textContent = e instanceof Error ? e.message : "Foldweave review could not start.";
}
//#endregion
