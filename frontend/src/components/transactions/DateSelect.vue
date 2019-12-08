<template>
	<div>
		<b-tabs position="is-centered" v-model="tfIndex" @change="update()" id="range" expanded>
			<b-tab-item label="WEEK"> </b-tab-item>
			<b-tab-item label="MONTH"> </b-tab-item>
			<b-tab-item label="YEAR"> </b-tab-item>
		</b-tabs>
		<div class="dateSelect">
			<b-icon icon="chevron-left" @click.native="subDate" class="arrow"></b-icon>
			<span v-if="timeFrame == 'year'" class="timeFrame">{{ endDateSnapped.format("YYYY") }}</span>
			<span v-if="timeFrame == 'month'" class="timeFrame">{{ endDateSnapped.format("MMMM, YYYY") }}</span>
			<span v-if="timeFrame == 'week'" class="timeFrame">{{ startDate.format("D MMM") + " - " + endDateSnapped.format("D MMM YY") }}</span>
			<b-icon @click.native="addDate" icon="chevron-right" class="arrow" :class="{ disabled: now <= endDateSnapped }"></b-icon>
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
			tfIndex: 1,
			endDate: moment(),
			now: moment(),
			endDateSnapped: null,
			startDate: null,
			old: { min: moment(0), max: moment(0) }
		};
	},
	computed: {
		range() {
			return { min: this.startDate, max: this.endDateSnapped, frame: this.timeFrame, forward: this.endDateSnapped.isAfter(this.old.max)};
		},
		timeFrame() {
			switch (this.tfIndex) {
				case 0:
					return "week";
				case 1:
					return "month";
				case 2:
					return "year";
			}
			return "month";
		}
	},
	watch: {
		target() {
			this.endDate = this.target.clone();
			this.update();
		}
	},
	methods: {
		emit() {
			if (!this.range.min.isSame(this.old.min.getTime) && !this.range.max.isSame(this.old.max.getTime)){
				this.$emit("input", this.range);
				this.old.min = this.range.min.clone()
				this.old.max = this.range.max.clone()
				this.$router.push({ query: { date: this.endDateSnapped.format('YYYY-MM-DD') }})
			}
		},
		update() {
			this.setEndDateSnapped();
			this.setStartDate();
			this.emit();
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
				this.endDate.subtract(1, "weeks");
			}
			if (this.timeFrame == "month") {
				this.endDate.subtract(1, "months");
			}
			if (this.timeFrame == "year") {
				this.endDate.subtract(1, "years");
			}
			this.update();
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
		this.endDate = this.target.clone();
		this.update();
	}
};
</script>

<style scoped>
/deep/ .tab-content {
	display: none;
}

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
}

.arrow {
	color: #aeaeb1;
	line-height: 20px;
	vertical-align: top;
	cursor: pointer;
}

.arrow.disabled {
	opacity: 0.5;
	cursor: default;
}

	#range {
		width: 80%;
		margin: auto;
	}

</style>
