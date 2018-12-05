<template>
<div style="position: relative">
	<svg viewBox="0 0 400 400" width="400" height="400" style="width: 100%; height: 40vh">
		<svg-arc v-for="value in values" :key="value[0]" radius="200" :start_angle="value[1]" :end_angle="value[2]" :colour="value[0]" thickness="6"/>
	</svg>
	<div class="middle">
		<mdc-text typo='subtitle1' tag="span" adjust-margin>{{title}}</mdc-text>
		<br/>
		<br/>
		<mdc-text typo='headline3' tag="span" adjust-margin>{{subtitle}}</mdc-text>
		<br/>
		<br/>
		<mdc-icon icon="info_outline"></mdc-icon>
	</div>
</div>
</template>

<script>
  import SvgArc from "@/components/SvgArc";

  export default {
	name: 'CircleChart',
	props: ['values', 'title', 'subtitle'],
	components: {
	  SvgArc
	}
  }
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
		font-family: 'Eczar', serif;
		color: white;
	}

	.mdc-typography--subtitle1 {
		font-family: 'Roboto Condensed', sans-serif;
		color: white;
	}

	.mdc-icon.mdc-icon--material {
		color: #adadb1;
	}
</style>
