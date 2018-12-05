<template>
<div @click="go">
  <mdc-icon :icon="icon" :class="{unselected: !selected, flipY: link == 'scheduled'}"></mdc-icon>
	<span v-show="selected" class="name">{{link}}</span>
</div>
</template>

<script>
export default {
	name: "RailButton",
	props: ["link"],
	methods: {
		go() {
		  if (this.link === "overview"){
			this.$router.push("/")
			return
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
			return this.$route.path.split('/')[1] === this.link;
		}
	}
};
</script>

<style scoped>
.mdc-icon {
	color: white;
	font-size: 42px;
	width: 100%;
	text-align: center;
}


div {
	padding-top: 42px;
	text-align: center;
}

.name {
	font-family: "Roboto Condensed", serif;
	color: white;
}

.unselected {
	color: #adadb1;
	cursor: pointer;
}

	.flipY {
		transform: scaleY(-1)
	}
</style>
