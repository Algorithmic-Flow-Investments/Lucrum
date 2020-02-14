<template>
	<path :d="d" :fill="colour" fill-rule="evenodd" :data-id="id" :stroke="(selected) ? 'gold' : ''" :stroke-width="(selected) ? 2 : 1"></path>
</template>

<script>
function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
	var angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180.0;

	return {
		x: centerX + radius * Math.cos(angleInRadians),
		y: centerY + radius * Math.sin(angleInRadians)
	};
}

export default {
	name: "CircleArc",
	props: ["radius", "start_angle", "end_angle", "thickness", "colour", "id", "selected"],
	computed: {
		d() {
			const opts = {
				cx: 200,
				cy: 200,
				radius: this.radius,
				start_angle: this.start_angle,
				end_angle: this.end_angle,
				thickness: this.thickness
			};

			const start = polarToCartesian(opts.cx, opts.cy, opts.radius, opts.end_angle);
			const end = polarToCartesian(opts.cx, opts.cy, opts.radius, opts.start_angle);
			const largeArcFlag = opts.end_angle - opts.start_angle <= 180 ? "0" : "1";

			const cutout_radius = opts.radius - opts.thickness,
				start2 = polarToCartesian(opts.cx, opts.cy, cutout_radius, opts.end_angle),
				end2 = polarToCartesian(opts.cx, opts.cy, cutout_radius, opts.start_angle),
				d = [
					"M", start.x, start.y,
					"A", opts.radius, opts.radius, 0, largeArcFlag, 0, end.x, end.y,
					"L", end2.x, end2.y,

					"M", start.x, start.y,
					"L", start2.x, start2.y,


					"A", cutout_radius, cutout_radius, 0, largeArcFlag, 0, end2.x, end2.y
				].join(" ");

			return d;
		}
	},
	mounted() {}
};
</script>

<style scoped></style>
