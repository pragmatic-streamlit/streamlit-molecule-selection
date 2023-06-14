import {Streamlit, StreamlitComponentBase, withStreamlitConnection} from "streamlit-component-lib";
import React, {ReactNode} from "react";
import {Mol2DSelector} from "./molecular";

interface State {}


class App extends StreamlitComponentBase<State> {

    componentDidMount(): void {
        Streamlit.setFrameHeight()
    }

    componentDidUpdate(): void {
        Streamlit.setFrameHeight()
    }
    
    forceResize(): void {
        Streamlit.setFrameHeight()
    }
    
    ref: any = null

    public render = (): ReactNode => {
        const content = this.props.args["content"]
        const ftype = this.props.args["ftype"]
        const preset_selections = this.props.args["preset_selections"]
        const nop_selection = this.props.args["nop_selection"]
        const min_allowed_atoms = this.props.args["min_allowed_atoms"]
        const max_allowed_atoms_percent = this.props.args["max_allowed_atoms_percent"]
        const height = this.props.args["height"]
        return (
            <div style={height? {height: height, overflow: "scroll"}:{}}>
            <Mol2DSelector
                smiles={ftype === 'smiles' ? content : ''}
                mol={ftype === 'mol' ? content : ''}
                onMol2DInstanceCreated={(instance, selectionWithHydrogen) => {
                    this.forceResize();
                    this.ref = instance
                }}
                onSelectionChanged={(selection, selectionWithHydrogen) => {
                    if (nop_selection){
                        return
                    }
                    const selectedAtomsSet = new Set(selection);
                    const status = document.getElementById('status');
                    if (selection.length < min_allowed_atoms) {
                        status && (status.innerText = `Select at least ${min_allowed_atoms} heavy atoms.`);
                        this.forceResize();
                        return;
                    }
                    if (
                        selection.length >= Math.floor(this.ref.model.mMol.getAllAtoms_0() * max_allowed_atoms_percent)
                    ) {
                        status && (status.innerText = `Select up to ${max_allowed_atoms_percent*100}% of heavy atoms.`);
                        this.forceResize();
                        return;
                    }
                    const queue = [selection[0]];
                    while (queue.length) {
                        const start = queue.shift() as number;
                        selectedAtomsSet.delete(start);
                        this.ref.model.mMol.mConnAtom[start]?.forEach((conn: number) => {
                            if (selectedAtomsSet.has(conn)) {
                                queue.push(conn);
                                selectedAtomsSet.delete(conn);
                            }
                        });
                    }
                    if (selectedAtomsSet.size) {
                        status && (status.innerText = "Selected atoms need to be connected.");
                        this.forceResize();
                        return;
                    }
                    status && (status.innerText = "Selected atoms successfully.");
                    this.forceResize();
                    Streamlit.setComponentValue({
                        selection,
                        selectionWithHydrogen,
                    })
                }}
                selection={preset_selections? preset_selections : []}
            />
            </div>
        )
    }
}
export default withStreamlitConnection(App)