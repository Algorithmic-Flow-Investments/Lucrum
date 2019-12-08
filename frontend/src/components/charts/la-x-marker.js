import object from 'laue/src/mixins/object'
import dashed from 'laue/src/mixins/dashed'


export default {
	name: 'LaXMarker',

	mixins: [object, dashed],

	props: {
		label: String,

		value: Number,

		placement: {
			type: String,
			default: 'end'
		}
	},

	computed: {
		point() {
			const {xRatio, canvas, len} = this.Plane
			let {y0, y1, x1} = canvas
			let x = x1 - (len - this.value) * xRatio
			if (this.value === null) y1 = y0;
			return {x1: x, y1: y0, x2: x, y2: y1}
		}
	},

	render(h) {
		const {point, curColor, curDashed, label, placement} = this

		return h(
			'g',

			[
				h('line', {
					attrs: point,
					style: {
						stroke: curColor,
						'stroke-dasharray': curDashed
					}
				}),
				label &&
				h(
					'text',
					{
						attrs: {
							fill: curColor,
							x:
								placement === 'end' ?
									point.x2 :
									placement === 'start' ?
										point.x1 :
										(point.x2 - point.x1) / 2 + point.x1,
							y: point.y1,
							dy: '-0.31em',
							'text-anchor': placement
						}
					},
					label
				)
			]
		)
	}
}
