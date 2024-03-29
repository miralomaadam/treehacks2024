import reflex as rx
from sqlmodel import select

from .login import require_login
from treehacks2024.state import State
from treehacks2024.will_state import WillState
from treehacks2024.user import User
from ..components import navbar

import json

class WillPageState(rx.State):

    holographic_will_states = ["Alaska", "Arizona", "Arkansas", "California", "Colorado", "Hawaii", "Idaho", "Kentucky", "Louisiana", "Maine", "Michigan", "Mississippi", "Montana", "Nebraska", "Nevada", "New Jersey", "North Carolina", "North Dakota", "Oklahoma", "Pennsylvania", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "West Virginia", "Wyoming"]
    
    #TODO: load state from DB

    
    _executor: str = ""
    _alternate_executor: str = ""
    _display_executor: str = "Executor: , Alternate Executor: "
    _beneficiaries: str = ""
    _funeral_arrangements: str = ""
    _assets: str = ""
    _residuary_beneficiary: str = ""
    _will_template: str = ""

    @rx.var
    def get_executor(self):
        res = "Executor: " + self._executor
        return res
    
    @rx.var
    def get_alternate_executor(self):
        res = "Alternate Executor: " + self._alternate_executor
        return res
    
    @rx.var
    def get_beneficiaries(self):
        res = "Beneficiaries: "
        if self._beneficiaries:
            res += ", ".join(json.loads(self._beneficiaries))
        return res
    
    @rx.var
    def get_beneficiaries_list(self) -> list[str]:
        if not self._beneficiaries:
            return []
        return json.loads(self._beneficiaries)
    
    @rx.var
    def get_funeral_arrangements(self):
        return "Funeral Arrangements: " + self._funeral_arrangements
    
    @rx.var
    def get_assets(self):
        res = ""
        if self._assets:
            assets_list = json.loads(self._assets)
            for asset_info in assets_list:
                asset_name = asset_info.get("name", "")
                asset_beneficiary = asset_info.get("beneficiary", "")
                res += f", {asset_name} (Beneficiary: {asset_beneficiary})"
        return "Assets: " + res[1:] if res else "Assets:"

    @rx.var
    def get_residuary_beneficiary(self):
        return "Residuary Beneficiary: " + self._residuary_beneficiary
    
    @rx.var
    def get_will_template(self):
        return self._will_template
    
    @rx.var
    def get_display_executor(self):
        return self._display_executor


    # this doesn't work rn
    def can_do_holographic_will(self):
        # user = None
        user = State.authenticated_user
        # with rx.session() as session:
        #     user = session.exec(
        #         select(User).where(User.session_id == rx.get_state().session_id)
        #     ).one_or_none()
        
        if user is None:
            return False
        
        if user.state_name in self.holographic_will_states:
            return True

        return False
    
    def save_changes(self):
        #TODO: fix this
        return

        user = None
        with rx.session() as session:
            # user = session.exec(
            #     select(User).where(User.session_id == rx.get_state().session_id)
            # ).one_or_none()

            user = State.authenticated_user

            # print(user.username)

            willstate = session.exec(
                select(WillState).where(WillState.username == user.username)
            ).one_or_none()

            if not willstate:
                willstate = WillState() # if state doesn't yet exist
                willstate.username = user.username

            willstate.executor = self._executor
            willstate.alternate_executor = self._alternate_executor
            willstate.beneficiaries = self._beneficiaries
            willstate.funeral_arrangements = self._funeral_arrangements
            willstate.assets = self._assets
            willstate.residuary_beneficiary = self._residuary_beneficiary

            print("f")

            session.commit()


    def handle_submit_executor(self, form_data: dict):
        executor = form_data["executor"]
        alternate_executor = form_data["alternate_executor"]
        # Check if the new executor is the same as either the existing executor or alternate executor
        if executor == alternate_executor:
            alternate_executor = None
        # Check if the new alternate executor is the same as the existing executor
        if executor:
            self._executor = executor
            if self._executor == self._alternate_executor:
                self._alternate_executor = ""
        if alternate_executor and alternate_executor != self._executor:
            self._alternate_executor = alternate_executor
        self._display_executor = f"Executor: {self._executor}, Alternate Executor: {self._alternate_executor}"

    def handle_reset_executors(self):
        self._executor = ""
        self._alternate_executor = ""
        self._display_executor = "Executor: , Alternate Executor: "

    def add_beneficiary(self, form_data: dict):
        # maybe expand this to collect more information: residence, contanct info of beneficiary, maybe last 4 of SSN #
        beneficiary = form_data["beneficiary"]
        
        if not beneficiary or (self._beneficiaries != "" and beneficiary in json.loads(self._beneficiaries)):
            return

        beneficiaries = json.loads(self._beneficiaries) if self._beneficiaries else []
        beneficiaries.append(beneficiary)
        self._beneficiaries = json.dumps(beneficiaries)

    def delete_beneficiary(self, form_data: dict):
        beneficiary_to_delete = form_data.get("beneficiary_to_delete", "")

        if not beneficiary_to_delete:
            return

        # Remove the beneficiary from the list
        beneficiaries_list = json.loads(self._beneficiaries) if self._beneficiaries else []
        beneficiaries_list = [beneficiary for beneficiary in beneficiaries_list if beneficiary != beneficiary_to_delete]
        self._beneficiaries = json.dumps(beneficiaries_list)


    def set_funeral_arrangements(self, form_data: dict):
        funeral_arrangements = form_data["funeral_arrangements"]
        if not funeral_arrangements:
            return
        self._funeral_arrangements = funeral_arrangements

    def add_asset(self, form_data: dict):
        asset = form_data["asset"]
        beneficiary = form_data["asset_beneficiary"]
        
        if not asset or not beneficiary:
            return
        
        assets = json.loads(self._assets) if self._assets else []

        # Check if the asset/beneficiary pair already exists
        if any(entry.get("name") == asset and entry.get("beneficiary") == beneficiary for entry in assets):
            return

        assets.append({"name": asset, "beneficiary": beneficiary})
        self._assets = json.dumps(assets)

    def delete_asset(self, form_data: dict):
        asset_name_to_delete = form_data.get("asset_to_delete", "")
        beneficiary_to_delete = form_data.get("beneficiary_to_delete", "")

        if not asset_name_to_delete or not beneficiary_to_delete:
            return
        
        assets_list = json.loads(self._assets) if self._assets else []

        # Filter out the asset to delete based on both asset name and beneficiary
        assets_list = [asset for asset in assets_list if asset.get("name") != asset_name_to_delete or asset.get("beneficiary") != beneficiary_to_delete]

        # Update the assets attribute
        self._assets = json.dumps(assets_list)
    
    def reassign_asset(self, form_data: dict):
        asset_to_reassign = form_data.get("asset_to_reassign", "")
        old_beneficiary = form_data.get("old_beneficiary", "")
        new_beneficiary = form_data.get("new_beneficiary", "")

        if not asset_to_reassign or not old_beneficiary or not new_beneficiary:
            return

        assets_list = json.loads(self._assets) if self._assets else []

        # Find the asset to reassign and update its beneficiary
        for asset in assets_list:
            if asset.get("name") == asset_to_reassign and asset.get("beneficiary") == old_beneficiary:
                asset["beneficiary"] = new_beneficiary
                break  # Assuming each asset has a unique tuple, exit the loop once the asset is found

        # Update the assets attribute
        self._assets = json.dumps(assets_list)

    def set_residuary_beneficiary(self, form_data: dict):
        residuary_beneficiary = form_data["residuary_beneficiary"]
        if not residuary_beneficiary:
            return
        self._residuary_beneficiary = residuary_beneficiary

    def generate_will(self):
        will_template = f"Last Will and Testament of _____________________. "

        # Step 1: Executor and Alternate Executor
        if self._executor:
            will_template += f"I appoint {self._executor} as the Executor of my will. "
        else:
            will_template += "I have not appointed an Executor. "
        if self._alternate_executor:
            will_template += f"If {self._executor} is unable or unwilling to serve, I appoint {self._alternate_executor} as the Alternate Executor. "

        # Step 2: List of Beneficiaries
        beneficiaries_list = json.loads(self._beneficiaries) if self._beneficiaries else []
        if beneficiaries_list:
            will_template += "I bequeath the following to my beneficiaries:"
            acc = ""
            for beneficiary in beneficiaries_list:
                acc += f", {beneficiary}"
            will_template += acc[1:]
        else:
            will_template += "I have no specific beneficiaries listed. "

        # will_template += "\n"

        # Step 3: Funeral Arrangements
        if self._funeral_arrangements:
            will_template += f"I request the following funeral arrangements:\n{self._funeral_arrangements}\n\n"

        # Step 4: Distribute Assets
        assets_list = json.loads(self._assets) if self._assets else []
        if assets_list:
            will_template += "I distribute the following assets:"
            acc = ""
            for asset_info in assets_list:
                asset_name = asset_info.get("name", "")
                asset_beneficiary = asset_info.get("beneficiary", "")
                acc += f", {asset_name} to {asset_beneficiary}"
            will_template += acc[1:]
        else:
            will_template += "I have no specific assets listed for distribution. "

        # will_template += "\n"

        # Step 5: Residuary Beneficiary
        if self._residuary_beneficiary:
            will_template += f"I appoint {self._residuary_beneficiary} as the Residuary Beneficiary to receive any remaining assets not specifically mentioned in this will."

        # Additional Information or Custom Sections can be added here

        # Step 6: Closing Statement
        will_template += "In witness whereof, I have executed this will on this day."

        self._will_template = will_template



@rx.page(title="Write Will", image="/github.svg")
@require_login
def will() -> rx.Component:
    content = rx.fragment(
        rx.vstack(
            navbar("Write Your Will"),
            rx.spacer(padding="4em"),
            rx.vstack(
            rx.heading("Choose your executor", font_size="1em"),
            rx.text("Your executor is the person who will carry out your wishes after you pass away. "
                    "You should choose someone you trust to handle your affairs. "
                    "You may also consider choosing an alternate executor in case your first choice is unable to serve.", 
                    font_size=".8em"),

            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Executor",
                            name="executor",
                            # align="center",
                        ),
                        rx.input(
                            placeholder="Alternate Executor",
                            name="alternate_executor",
                            # align="center",
                        ),
                        rx.button("Submit", type="submit", 
                                #   align="center"
                                  ),
                    ),
                    on_submit=WillPageState.handle_submit_executor,
                    reset_on_submit=True,
                    # align="center",
                ),
                rx.text(WillPageState.get_executor, font_size=".8em"),
                rx.text(WillPageState.get_alternate_executor, font_size=".8em"),
                rx.button("Reset Executors", type="button", on_click=WillPageState.handle_reset_executors),
                # align="center",
            ),
            rx.spacer(),


            rx.heading("List your beneficiaries", font_size="1em"),
            rx.text("Your beneficiaries are the people who will receive your assets after you pass away. "
                    "In addition to people like your friends and family, you may also list charitable organizations as beneficiaries. "
                    "Your executor may be a beneficiary in your will but does not have to be a beneficiary."
                    "You can also list beneficiaries that you do not assign assets to. "
                    "This may be because they are listed in your residuary clause. "
                    "You might also do this because you do not want to give any assets to them; specifying that you do not wish to give someone any assets in your will can make it harder for them to contest it. " , 
                    font_size=".8em"),
            
            rx.vstack(
                rx.form(
                    rx.input(
                        placeholder="Beneficiary",
                        name="beneficiary",
                    ),
                    rx.button("Add Beneficiary", type="submit"),
                    on_submit=WillPageState.add_beneficiary,
                    reset_on_submit=True,
                ),
                rx.form(
                    rx.input(
                        placeholder="Beneficiary to Delete",
                        name="beneficiary_to_delete",
                    ),
                    rx.button("Delete Beneficiary", type="submit"),
                    on_submit=WillPageState.delete_beneficiary,
                    reset_on_submit=True,
                ),
                rx.text(WillPageState.get_beneficiaries, font_size=".8em"),
                # align="center",
            ),
            rx.spacer(),
            
            rx.heading("List funeral arrangements", font_size="1em"),
            rx.text("You can list your intended funeral arrangements here. "
                    "You may also consider creating a separate document with your funeral arrangements and letting your executor know where to find it.", 
                    font_size=".8em"),
            
            
            # funeral arrangements form
            rx.form(
                rx.input(
                    placeholder="Funeral Arrangements",
                    name="funeral_arrangements",
                ),
                rx.button("Set Funeral Arrangements", type="submit"),
                on_submit=WillPageState.set_funeral_arrangements,
                reset_on_submit=True,
            ),
            rx.text(WillPageState.get_funeral_arrangements, font_size=".8em"),
            rx.spacer(),

            rx.heading("Distribute your assets", font_size="1em"),
            rx.text("List your assets here. This is a list of things that you own that you want to be distributed to your beneficiaries. This can include money, property, pets, vehicles, and personal belongings or heirlooms. "
                    "You may also include things like online account passwords to be distributed as well. "
                    "Each asset must be distributed to a beneficiary. "
                    "Assets that cannot be distributed to your beneficiaries include things like life insurance benefits, retirement plans, assets owned under joint tenancy, and payable-on-death accounts and secutires. "
                    "The distribution of these assets must be done outside of your will: for example setting a beneficiary for your life insurane policy must be done under that policy.", 
                    font_size=".8em"),
            
            # put in a form to list assets and assign each to a beneficiary
            rx.vstack(
                rx.form(
                    rx.vstack(
                    rx.input(
                        placeholder="Asset",
                        name="asset",
                    ),
                    rx.select(
                        placeholder="Select Beneficiary",
                        name="asset_beneficiary",
                        label="Beneficiaries",
                        items=WillPageState.get_beneficiaries_list,  # Populate options from existing beneficiaries
                    ),
                    rx.button("Add Asset", type="submit"),
                    ),
                    on_submit=WillPageState.add_asset,
                    reset_on_submit=True,
                ),
                rx.form(
                    rx.input(
                        placeholder="Asset Name to Delete",
                        name="asset_to_delete",
                    ),
                    rx.input(
                        placeholder="Beneficiary to Delete",
                        name="beneficiary_to_delete",
                    ),
                    rx.button("Delete Asset", type="submit"),
                    on_submit=WillPageState.delete_asset,
                    reset_on_submit=True,
                ),
                rx.form(
                    rx.input(
                        placeholder="Asset Name to Reassign",
                        name="asset_to_reassign",
                    ),
                    rx.input(
                        placeholder="Old Beneficiary",
                        name="old_beneficiary",
                    ),
                    rx.input(
                        placeholder="New Beneficiary",
                        name="new_beneficiary",
                    ),
                    rx.button("Reassign Asset", type="submit"),
                    on_submit=WillPageState.reassign_asset,
                    reset_on_submit=True,
                ),
                rx.text(WillPageState.get_assets,
                        # align="center",
                        whitespace="pre-wrap", font_size=".8em"),
                # align="center",
            ),
            rx.spacer(),
            
            rx.heading("Create a residuary clause.", font_size="1em"),
            rx.text("A residuary clause details what should happen to any assets that were not specifically listed in your will. "
                    "Even if you don't think there are any assets you haven't listed, it is still a good idea to choose a beneficiary for your residuary clause. ",
                    font_size=".8em"),

            # specify residuary beneficiary
            rx.form(
                rx.input(
                    placeholder="Residuary Beneficiary",
                    name="residuary_beneficiary",
                ),
                rx.button("Set Residuary Beneficiary", type="submit"),
                on_submit=WillPageState.set_residuary_beneficiary,
                reset_on_submit=True,
            ),
            rx.text(WillPageState.get_residuary_beneficiary, font_size=".8em"),
            rx.spacer(),

            rx.heading("Generate will template", font_size="1em"),
            rx.text("Make sure you have chosen an executor, chosen at least one beneficiary, and listed at least one asset.",
                    font_size=".8em"),

            # add button to generate will template using previously specified info
            rx.button("Generate Example Will", type="button", on_click=WillPageState.generate_will),
            rx.text(WillPageState.get_will_template, font_size=".8em"),

            # doesn't do anything rn
            # rx.spacer(),
            # rx.button("Save Changes", type="button", on_click=WillPageState.save_changes),

            # can_do_holographic_will() doesn't work properly
            # also probably a bad idea to tell elderly people to DIY it
            # rx.spacer(),
            # rx.cond(
            #     WillPageState.can_do_holographic_will(),
            #     rx.vstack(
            #         rx.heading("Create a holographic will", font_size="1.5em"),
            #         rx.spacer(),
            #         rx.text("Your state recognizes holographic wills. You can create a holographic will by writing your will by hand and signing it. You do not need witnesses to sign your will. You should still consider consulting with a lawyer to ensure your will is written properly.", align="center"),
            #         align="center"
            #     )
            # ),
            # spacing="8",
            # padding_top="10%",
            padding_right="10%",
            # padding_left="20%",
            # align="center",
                padding="0 2em",
        ),
        ),
    )


    return content