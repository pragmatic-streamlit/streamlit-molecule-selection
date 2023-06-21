
import os
from typing import List, Optional
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_DEVELOP_MODE = os.getenv('DEVELOP_MODE')

_RELEASE = not _DEVELOP_MODE

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("molstar_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit-molecule-selection",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit-molecule-selection", path=build_dir) # noqa


def st_molecule_selection(content, ftype: str = "smiles", *,
                          preset_selections: Optional[List[int]] = None,
                          nop_selection=False,
                          min_allowed_atoms: int = 5,
                          max_allowed_atoms_percent: float = 0.9,
                          height=None,
                          key = None): # noqa
    if ftype not in ('smiles', 'mol'):
        raise ValueError('ftype must be one of "smiles" or "mol"')
    params = {
        "content": content,
        "ftype": f'{ftype}',
        "height": height,
        "min_allowed_atoms": min_allowed_atoms,
        "max_allowed_atoms_percent": max_allowed_atoms_percent,
        "nop_selection": nop_selection,
        "preset_selections": preset_selections,
    }
    return _component_func(key=key, default=None, **params)


if (not _RELEASE) or os.getenv('SHOW_MOLECULE_SELECTION_DEMO'):
    import streamlit as st
    #st.write(st_molecule_selection('CC(C)CN(CC(C(CC1CCCCC1)NC(OC1C(CCO2)C2OC1)=O)O)S(C(CC1)CCC1N)(=O)=O', height=100))
    st.write(st_molecule_selection('CC(C)CN(CC(C(CC1CCCCC1)NC(OC1C(CCO2)C2OC1)=O)O)S(C(CC1)CCC1N)(=O)=O', nop_selection=True, 
                                   preset_selections=[0, 1, 2, 4, 5],
                                   key='2'))

    with open('examples/3d20_ligand.sdf') as f:
        st.write(st_molecule_selection(f.read(), ftype='mol', key='4'))

    # st_molstar_remote("https://files.rcsb.org/view/1LOL.cif", key='sds')
    # st_molstar('examples/complex.pdb', key='3')
    # st_molstar('examples/cluster_of_100.gro', key='5')
    # st_molstar('examples/md.gro',key='6')
    # st_molstar('examples/H2O.cif',key='7')
    # st_molstar('examples/complex.pdb', 'examples/complex.xtc', key='4')
