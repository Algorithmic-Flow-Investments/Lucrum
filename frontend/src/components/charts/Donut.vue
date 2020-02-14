<template>
	<div style="position: relative" @mouseover="graphHover" @mouseout="graphHover">
		<svg viewBox="0 0 400 400" width="400" height="400" style="width: 100%; height: 40vh; pointer-events: fill" @mouseover="segHover" @mouseout="segHover" @click="click">
			<template v-for="(sect, s1) in sections">
				<circle-arc :selected="selectedSeg && (selectedSeg.parent === sect.data.id)" :key="'o_' + s1" :id="sect.data.id + ',-1'" :radius="radius" :start_angle="sect.startAngle" :end_angle="sect.endAngle" :class="sect.cls" :thickness="tweenedThickness" />
				<circle-arc v-for="(sect2, s2) in sect.children" :selected="selectedSeg && (selectedSeg.child === sect2.data.id)"  :key="'i' + s1 + '_' + s2" :id="sect.data.id + ',' + sect2.data.id" :radius="radius - tweenedThickness - 7" :start_angle="sect2.startAngle" :end_angle="sect2.endAngle" :class="sect2.cls" :thickness="tweenedThickness - 2" />
			</template>
		</svg>
		<div v-if="!hoveredSeg && !selectedSeg" class="middle">
			<slot></slot>
		</div>
		<div v-else class="middle" ref="tooltip">
			<slot name="tooltip" :parent="selParent" :child="selChild"></slot>
		</div>
	</div>
</template>

<script>
import CircleArc from "@/components/charts/CircleArc";

class DonutSegment {
	constructor(data, value, cls, children, startAngle, endAngle) {
		this.data = data;
		this.value = value
		this.cls = cls
		this.children = children
		this.startAngle = startAngle;
		this.endAngle = endAngle;
	}

	setAngle(startAngle, endAngle) {
		return new DonutSegment(this.data, this.value, this.cls, this.children, startAngle, endAngle)
	}
}

export { DonutSegment }

export default {
	name: "Donut",
	props: {"value": Array, "thickness": {type: Number, default: 8}, "thicknessMod": {type: Number, default: 4}},
	data () {
		return {
			radius: 200,
			tweenedThickness: this.thickness,
			tween: null,
			hovered: false,
			selectedSeg: null,
			hoveredSeg: null
		}
	},
	methods: {
		graphHover(e) {
			this.hovered = e.type === "mouseover";
			if (!this.hovered){
				setTimeout(this.updateSize, 100)
			}
		},
		segHover(e) {
			if (e.target.dataset.id) {
				this.hoveredSeg = {
					parent: parseInt(e.target.dataset.id.split(",")[0]),
					child: parseInt(e.target.dataset.id.split(",")[1])
				}
				if (this.hoveredSeg.child === -1) {
					this.hoveredSeg.child = null
				}
			}
			else {
				this.hoveredSeg = null
			}
		},
		updateSize() {
			if (this.tween !== null) {
				return
			}
			let newThickness, jump
			if (this.hovered || this.selectedSeg) {
				newThickness = this.thickness * this.thicknessMod
				jump = 2
			}
			else {
				newThickness = this.thickness
				jump = -2
			}

			if (this.tweenedThickness === newThickness) {
				return
			}

			this.tween = setInterval(() => {
				if (Math.abs(this.tweenedThickness - newThickness) < 2) {
					this.tweenedThickness = newThickness;
					clearInterval(this.tween);
					this.tween = null;
					this.updateSize();
					return
				}
				this.tweenedThickness += jump
			}, 10)
		},
		click(e) {
			if (e.target.dataset.id) {
				this.selectedSeg = {
					parent: parseInt(e.target.dataset.id.split(",")[0]),
					child: parseInt(e.target.dataset.id.split(",")[1])
				};
				if (this.selectedSeg.child === -1) this.selectedSeg.child = null
				this.$emit('click', this.selectedSeg)
			}
			else {
				this.selectedSeg = null
				this.$emit('click', null)
			}
		}
	},
	computed: {
		sections() {
			let cumulative = 0;
			let gap = 5;
			let childGap = 2;
			let data = this.value.filter(item => item.value > 0)
			let excess = data.length * gap
			return data.map(item => {
				let segment_size = (item.value / this.total) * (360 - excess);
				let startAngle = cumulative;
				let endAngle = cumulative + segment_size;
				let segment = item.setAngle(startAngle, endAngle);

				let children_cumulative = cumulative;
				let children = item.children.filter(child => child.value > 0)
				let children_excess = (children.length - 1) * childGap;
				segment.children = children.map((child, c) => {
					let child_segment_size = (child.value / item.value) * (segment_size - children_excess);
					let childStartAngle = children_cumulative;
					let childEndAngle = children_cumulative + child_segment_size;
					let child_segment = child.setAngle(childStartAngle, childEndAngle);
					children_cumulative += child_segment_size + childGap;
					return child_segment
				})
				cumulative += segment_size + gap;
				return segment
			})
		},
		total() {
			return this.value.reduce((total, item) => {
				return total + item.value
			}, 0);
		},
		selParent() {
			if (this.selectedSeg) {
				return this.selectedSeg.parent
			}
			if (this.hoveredSeg) {
				return this.hoveredSeg.parent
			}
			return null
		},
		selChild() {
			if (this.selectedSeg) {
				return this.selectedSeg.child
			}
			if (this.hoveredSeg) {
				return this.hoveredSeg.child
			}
			return null
		}
	},
	components: {
		CircleArc
	},
};
</script>

<style scoped lang="scss">
	.middle {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	text-align: center;
}

	.tooltip-wrapper {
		position: absolute;
	}
</style>
