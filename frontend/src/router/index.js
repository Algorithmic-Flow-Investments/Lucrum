import Vue from "vue";
import Router from "vue-router";
import Dashboard from "@/pages/Dashboard";
import Transactions from "@/pages/Transactions";
import Classification from "@/pages/Classification";
import Accounts from "@/pages/Accounts";

Vue.use(Router);

export default new Router({
	mode: "history",
	routes: [
		{
			path: "/",
			name: "Dashboard",
			component: Dashboard
		},
		{
			path: "/transactions",
			name: "Transactions",
			component: Transactions
		},
		{
			path: "/classification",
			name: "Classification",
			component: Classification
		},
		{
			path: "/accounts",
			name: "Accounts",
			component: Accounts
		}
	]
});
