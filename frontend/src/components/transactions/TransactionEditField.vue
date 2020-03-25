<template>
	<div class="edit" @mouseover="hovered = true" @mouseleave="hovered = false">
		<i class="fas" :class="icon"></i>
		<span class="text">
			<span>{{ value }}</span>
			<span class="tooltip" :class="{hovered}">
				<span v-if="extra.inferred">Inferred: {{extra.inferred}}</span>
				<span v-if="extra.imported">Imported: {{extra.imported}}</span>
				<span v-if="extra.manual">Manual: {{extra.manual}}</span>
			</span>
		</span>
	</div>
</template>

<script>
	import Transaction from "@/Models/Transaction";

	export default {
		name: "TransactionEditField",
		props: {'icon': String, 'value': Object, 'extra': Object},
		data() {
			return {
				hovered: false
			}
		}
	};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

	.edit {
		display: flex;
		padding-bottom: 10px;
		cursor: pointer;
	}

	.edit .text {
		margin-left: 2px;
	}

	.edit i {
		line-height: inherit;
	}

	/* Tooltip text */
	.edit .tooltip {
		/*visibility: hidden;*/
		background-color: $background;
		color: #fff;
		text-align: center;
		padding: 5px;
		border-radius: 6px;
		position: absolute;
		z-index: 1;
		margin-left: 10px;
		transform: translateY(-50%);
		margin-top: 10px;
		width: fit-content;
		max-width: 60%;
	}

	.tooltip span {
		display: block;
	}

	.edit .tooltip::after {
		content: " ";
		position: absolute;
		top: 50%;
		right: 100%; /* To the left of the tooltip */
		margin-top: -5px;
		border-width: 5px;
		border-style: solid;
		border-color: transparent $background transparent transparent;
	}

	.tooltip {
		opacity: 0;
		transition: opacity .2s;
	}

	.tooltip.hovered {
		opacity: 1;
	}
</style>
