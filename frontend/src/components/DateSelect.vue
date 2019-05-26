<template>
	<div>
		<mdc-tab-bar @change="onSelected">
			<mdc-tab>Week</mdc-tab>
			<mdc-tab active>Month</mdc-tab>
			<mdc-tab>Year</mdc-tab>
		</mdc-tab-bar>
		<div class="dateSelect">
			<mdc-icon icon="chevron_left" @click.native="subDate" class="arrow"></mdc-icon>
			<span v-if="timeFrame == 'year'" class="timeFrame">{{ endDateSnapped.format("YYYY") }}</span>
			<span v-if="timeFrame == 'month'" class="timeFrame">{{ endDateSnapped.format("MMMM, YYYY") }}</span>
			<span v-if="timeFrame == 'week'" class="timeFrame">{{ startDate.format("D MMM") + " - " + endDateSnapped.format("D MMM YY") }}</span>
			<mdc-icon @click.native="addDate" icon="chevron_right" class="arrow" :class="{ disabled: now <= endDateSnapped }"></mdc-icon>
		</div>
	</div>
</template>

<script>
import moment from "moment";

export default {
	name: "DateSelect",
	props: ["value", "target"],
	data() {
		return {
			timeFrame: "month",
			endDate: moment(),
			now: moment(),
			endDateSnapped: null,
			startDate: null
		};
	},
	computed: {
		range() {
			return { min: this.startDate, max: this.endDateSnapped };
		}
	},
	watch: {
		target(){
			this.endDate = this.target.clone()
			this.update()
		}
	},
	methods: {
		emit() {
			this.$emit("input", this.range);
		},
		update(){
			this.setEndDateSnapped();
			this.setStartDate();
			this.emit();
		},
		onSelected(idx) {
			if (idx == 0) {
				this.timeFrame = "week";
			}
			if (idx == 1) {
				this.timeFrame = "month";
			}
			if (idx == 2) {
				this.timeFrame = "year";
			}
			this.update()
		},
		addDate() {
			if (this.now <= this.endDateSnapped) return;
			if (this.timeFrame == "week") {
				this.endDate.add("weeks", 1);
			}
			if (this.timeFrame == "month") {
				this.endDate.add("months", 1);
			}
			if (this.timeFrame == "year") {
				this.endDate.add("years", 1);
			}
			this.setEndDateSnapped();
			this.setStartDate();
			this.emit();
		},
		subDate() {
			if (this.timeFrame == "week") {
				this.endDate.subtract("weeks", 1);
			}
			if (this.timeFrame == "month") {
				this.endDate.subtract("months", 1);
			}
			if (this.timeFrame == "year") {
				this.endDate.subtract("years", 1);
			}
			this.update()
		},
		setEndDateSnapped() {
			if (this.timeFrame == "week") {
				this.endDateSnapped = this.endDate.clone().day(7);
			}
			if (this.timeFrame == "month") {
				this.endDateSnapped = this.endDate
					.clone()
					.add("months", 1)
					.date(0);
			}
			if (this.timeFrame == "year") {
				this.endDateSnapped = this.endDate
					.clone()
					.add("years", 1)
					.month(0)
					.date(0);
			}
		},
		setStartDate() {
			if (this.timeFrame == "week") {
				this.startDate = moment(this.endDate).day(1);
			}
			if (this.timeFrame == "month") {
				this.startDate = moment(this.endDate).date(1);
			}
			if (this.timeFrame == "year") {
				this.startDate = moment(this.endDate).dayOfYear(1);
			}
		}
	},
	created() {
		this.update()
	}
};
</script>

<style scoped>
.dateSelect {
	position: relative;
	left: 50%;
	-webkit-transform: translateX(-50%);
	margin-top: 10px;
	margin-bottom: 20px;
	width: fit-content;
}

.timeFrame {
	color: #aeaeb1;
	line-height: 20px;
	vertical-align: top;
	font-family: Roboto;
}

.arrow {
	color: #aeaeb1;
	line-height: 20px;
	vertical-align: top;
	cursor: pointer;
}

.arrow.disabled {
	opacity: 0;
	cursor: default;
}
</style>
