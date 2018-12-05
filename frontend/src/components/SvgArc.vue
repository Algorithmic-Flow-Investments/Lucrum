<template>
	<path :d="d" :fill="colour" stroke="none" fill-rule="evenodd" />
</template>

<script>

  function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
	var angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;

	return {
	  x: centerX + (radius * Math.cos(angleInRadians)),
	  y: centerY + (radius * Math.sin(angleInRadians))
	};
  }

  export default {
	name: 'SvgArc',
	props: ['radius', 'start_angle', 'end_angle', 'thickness', 'colour'],
	computed: {
	  d () {
		var opts = {
		  cx: 200,
		  cy: 200,
		  radius: this.radius,
		  start_angle: this.start_angle,
		  end_angle: this.end_angle,
		  thickness: this.thickness
		};

		var start = polarToCartesian(opts.cx, opts.cy, opts.radius, opts.end_angle);
		var end = polarToCartesian(opts.cx, opts.cy, opts.radius, opts.start_angle);
		var largeArcFlag = opts.end_angle - opts.start_angle <= 180 ? "0" : "1";

		var cutout_radius = opts.radius - opts.thickness,
		  start2 = polarToCartesian(opts.cx, opts.cy, cutout_radius, opts.end_angle),
		  end2 = polarToCartesian(opts.cx, opts.cy, cutout_radius, opts.start_angle),
		  d = [
			"M", start.x, start.y,
			"A", opts.radius, opts.radius, 0, largeArcFlag, 0, end.x, end.y,
			"L", opts.cx, opts.cy,
			"Z",

			"M", start2.x, start2.y,
			"A", cutout_radius, cutout_radius, 0, largeArcFlag, 0, end2.x, end2.y,
			"L", opts.cx, opts.cy,
			"Z"
		  ].join(" ");

		return d
	  }
	},
	mounted () {


	}
  }
</script>

<style scoped>

</style>
