<template>
	<div @click="go">
		<mdc-icon :icon="icon" :class="{ unselected: !selected, flipY: link == 'scheduled' }"></mdc-icon>
		<!--transition name="slide-fade"-->
		<span :class="{ name: true, show: selected }">{{ link }}</span>
		<!--/transition-->
	</div>
</template>

<script>
export default {
	name: "TabButton",
	props: ["link"],
	methods: {
		go() {
			if (this.link === "overview") {
				this.$router.push("/");
				return;
			}
			this.$router.push("/" + this.link);
		}
	},
	computed: {
		icon() {
			switch (this.link) {
				case "overview":
					return "pie_chart";
				case "accounts":
					return "account_balance";
				case "budget":
					return "attach_money";
				case "transactions":
					return "list";
				case "scheduled":
					return "show_chart";
			}
		},
		selected() {
			if (this.$route.path === "/" && this.link === "overview") {
				return true;
			}
			return this.$route.path.split("/")[1] === this.link;
		}
	}
};
</script>

<style scoped>
div {
	display: inline-block;
	transition: all 0.5s;
}

.mdc-icon {
	color: white;
	font-size: 32px;
	text-align: center;
}

.name {
	font-family: "Roboto Condensed", serif;
	color: white;
	line-height: 32px;
	vertical-align: top;
	font-size: larger;
	padding-left: 10px;
	display: inline-block;
	transform: scaleX(0);
	max-width: 0;
	transition: color 0.5s;
	transform-origin: left;
}

@media (max-width: 320px) {
	.name {
		padding-left: 0;
	}
}

.show {
	max-width: 500px;
	transform: scaleX(1);
	transition: transform 0.5s, max-width 0.5s;
}

.unselected {
	color: #adadb1;
	cursor: pointer;
}

.flipY {
	transform: scaleY(-1);
}
</style>
