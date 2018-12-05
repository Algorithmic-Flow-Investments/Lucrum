import Vue from "vue";
import Router from "vue-router";
import Overview from "@/views/Overview";
import AccountsPage from "@/views/AccountsPage";
import TransactionsPage from "@/views/TransactionsPage";
import Budget from "@/views/Budget";
import Scheduled from "@/views/Scheduled";

Vue.use(Router);

export default new Router({
	mode: "history",
	routes: [
		{
			path: "/",
			name: "Overview",
			component: Overview
		},
		{
			path: "/accounts",
			name: "Accounts",
			component: AccountsPage
		},
		{
			path: "/transactions/:transactionId?/:edit?",
			name: "Transactions",
			component: TransactionsPage
		},
		{
			path: "/budget",
			name: "Budget",
			component: Budget
		},
		{
			path: "/scheduled",
			name: "Scheduled",
			component: Scheduled
		}
	]
});
