<template>
	<div class="mdc-theme--background" style="height: 100vh" id="app">
		<edit-screen></edit-screen>
	<div class="small">
		<rail-tabs/>
		<transition name="slide-horiz">
			<router-view/>
		</transition>
	</div>
    <mdc-layout-grid class="large">
    	<mdc-layout-cell class="phone-0" span="1">
    		<rail/>
		</mdc-layout-cell>
		<mdc-layout-cell class="span-0" phone="4">
			<rail-tabs/>
		</mdc-layout-cell>
		<mdc-layout-cell desktop="11" tablet="7" phone="4">
			<transition name="slide-vert">
				<router-view/>
			</transition>
		</mdc-layout-cell>
  	</mdc-layout-grid>
	</div>
</template>

<script>
import Rail from "@/components/Rail";
import RailTabs from "@/components/RailTabs";
import EditScreen from "@/components/EditScreen"


export default {
	name: "app",
	components: {
		Rail,
		RailTabs,
	  	EditScreen
	}
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Roboto|Roboto+Condensed");
@import url('https://fonts.googleapis.com/css?family=Eczar');

	.mdc-layout-grid__cell--span-1 {
		width: 72px;
	}

@media (max-width: 479px) {
	.phone-0 {
		display: none;
	}
	.large {
		display: none;
	}
}

@media (min-width: 479px) {
	.span-0 {
		display: none;
	}
	.small {
		display: none;
	}
}

.slide-horiz-enter-active, .slide-horiz-leave-active, .slide-vert-enter-active, .slide-vert-leave-active {
	transition: transform .5s;
}
.slide-horiz-enter, .slide-horiz-leave-to {
	transform: translateX(-100vw);
}

.slide-vert-enter, .slide-vert-leave-to {
	transform: translateY(-100vh);
}
</style>
