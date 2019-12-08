<template>
	<div id="app">
		<div class="columns">
			<navigation></navigation>
			<div class="column is-11">
				<router-view></router-view>
			</div>
			<loading/>
		</div>
	</div>
</template>

<script>
import navigation from "@/components/navigation/Navigation";
import Loading from "@/components/Loading";

export default {
	name: "app",
	components: {
		Loading,
		navigation
	}
};
</script>

<style lang="scss">
@import "assets/theme";
@import url('https://fonts.googleapis.com/css?family=Eczar&display=swap');
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed&display=swap');

#app {
	min-height: 100vh;
	padding: 12px;
}

body,
html {
	height: 100%;
	overflow-y: auto;
}

body {
	margin: 0;
	background-color: $background;
	color: $text;
	font-family: "Roboto Condensed", sans-serif;
}

.sect {
	background-color: $foreground;
	border-radius: 4px;
	padding: 20px;
	overflow-x: hidden;
}

	.money {
		font-family: "Eczar", serif;
	}

	.is-clickable {
		cursor: pointer;
	}

.sect::-webkit-scrollbar {
	width: .5em;
}

.sect::-webkit-scrollbar-track {
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
}

.sect::-webkit-scrollbar-thumb {
	background-color: darkgrey;
	outline: 1px solid slategrey;
}
</style>
