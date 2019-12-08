<template>
	<div style="position: relative">
		<svg viewBox="0 0 400 400" width="400" height="400" style="width: 100%; height: 40vh">
			<template v-for="sect in sections">
				<circle-arc :key="sect.title" :radius="radius" :start_angle="sect.start" :end_angle="sect.end" :colour="sect.colour" :thickness="thickness" />
				<circle-arc v-for="sect2 in sect.children" :key="sect2.title" :radius="radius - thickness - 5" :start_angle="sect2.start" :end_angle="sect2.end" :colour="sect2.colour" :thickness="thickness - 2" />
			</template>
		</svg>
		<div class="middle">
			<slot></slot>
		</div>
	</div>
</template>

<script>
import CircleArc from "@/components/charts/CircleArc";

export default {
	name: "Donut",
	props: ["data"],
	data () {
		return {
			thickness: 6,
			radius: 200
		}
	},
	computed: {
		sections() {
			let cumulative = 0;
			let excess = this.data.length * 5
			return this.data.map(item => {
				let segment_size = (item.value / this.total) * (360 - excess);
				let children_cumulative = cumulative;
				let children_excess = item.children.length * 2
				let children = item.children.map(child => {
					let child_segment_size = (child.value / item.value) * (segment_size - children_excess + 2)
					let child_sect = {'title': child.title, 'colour': child.colour, 'start': children_cumulative, 'end': (children_cumulative + child_segment_size)};
					children_cumulative += child_segment_size + 2;
					return child_sect
				})
				let sect = {'title': item.title, 'colour': item.colour, 'start': cumulative, 'end': (cumulative + segment_size), 'children': children};
				cumulative += segment_size + 5;
				return sect;
			})
		},
		total() {
			return this.data.reduce((total, item) => {
				return total + item.value
			}, 0);
		}
	},
	components: {
		CircleArc
	}
};
</script>

<style scoped>
.middle {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	text-align: center;
}
.mdc-typography--headline3 {
	font-family: "Eczar", serif;
	color: white;
}

.mdc-typography--subtitle1 {
	font-family: "Roboto Condensed", sans-serif;
	color: white;
}

.mdc-icon.mdc-icon--material {
	color: #adadb1;
}
</style>
